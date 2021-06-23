from typing import Type

from eth_hash.auto import keccak
from eth_utils import (
    encode_hex,
)
from eth.vm.forks.frontier.state import (
    FrontierTransactionExecutor,
    FrontierState
)

from eth.abc import (
    ComputationAPI,
    MessageAPI,
    SignedTransactionAPI,
    TransactionExecutorAPI,
)

from eth.vm.message import (
    Message,
)

from eth_typing import Address

from eth.constants import CREATE_CONTRACT_ADDRESS

from .constants import (
    FEE_TOKEN_ADDRESS,
    FEE_TOKEN_STORAGE_BALANCE
)

from .computation import Simple3Computation

from .validation import validate_simple3_transaction

class Simple3TransactionExecutor(FrontierTransactionExecutor):
    # TODO: should be abstract method in StateAPI
    # TODO: bytes -> Address type
    def get_fee_token_balance(self, address: bytes):
        address_bytes = b"\0"*12 + address
        balance_bytes = FEE_TOKEN_STORAGE_BALANCE

        token_storage_key = int.from_bytes(keccak(address_bytes + balance_bytes), byteorder='big')
        fee_token_balance = self.vm_state.get_storage(Address(FEE_TOKEN_ADDRESS), token_storage_key)

        return fee_token_balance

    def set_fee_token_balance(self, address: bytes, balance: int):
        address_bytes = b"\0"*12 + address
        balance_bytes = FEE_TOKEN_STORAGE_BALANCE

        token_storage_key = int.from_bytes(keccak(address_bytes + balance_bytes), byteorder='big')

        self.vm_state.set_storage(Address(FEE_TOKEN_ADDRESS), token_storage_key, balance)

    def add_fee_token_balance(self, address: bytes, amount: int):
        address_bytes = b"\0"*12 + address
        balance_bytes = FEE_TOKEN_STORAGE_BALANCE

        token_storage_key = int.from_bytes(keccak(address_bytes + balance_bytes), byteorder='big')
        fee_token_balance = self.vm_state.get_storage(Address(FEE_TOKEN_ADDRESS), token_storage_key)

        self.vm_state.set_storage(Address(FEE_TOKEN_ADDRESS), token_storage_key, fee_token_balance + amount)

    def sub_fee_token_balance(self, address: bytes, amount: int):
        address_bytes = b"\0"*12 + address
        balance_bytes = FEE_TOKEN_STORAGE_BALANCE

        token_storage_key = int.from_bytes(keccak(address_bytes + balance_bytes), byteorder='big')
        fee_token_balance = self.vm_state.get_storage(Address(FEE_TOKEN_ADDRESS), token_storage_key)

        self.vm_state.set_storage(Address(FEE_TOKEN_ADDRESS), token_storage_key, fee_token_balance - amount)

    def build_evm_message(self, transaction: SignedTransactionAPI) -> MessageAPI:
        gas_fee = transaction.gas * transaction.gas_price

        fee_token_balance = self.get_fee_token_balance(transaction.sender)
        if fee_token_balance < gas_fee:
            raise Exception(
                "not enough balance"
            )

        # Buy Gas
        print(f"gas_fee: {gas_fee}")
        print(f"balance1: {fee_token_balance}")
        self.sub_fee_token_balance(transaction.sender, gas_fee)
        fee_token_balance = self.get_fee_token_balance(transaction.sender)
        print(f"balance2: {fee_token_balance}")

        # Increment Nonce
        self.vm_state.increment_nonce(transaction.sender)

        # Setup VM Message
        message_gas = transaction.gas - transaction.intrinsic_gas

        if transaction.to == CREATE_CONTRACT_ADDRESS:
            contract_address = generate_contract_address(
                transaction.sender,
                self.vm_state.get_nonce(transaction.sender) - 1,
            )
            data = b''
            code = transaction.data
        else:
            contract_address = None
            data = transaction.data
            code = self.vm_state.get_code(transaction.to)

        self.vm_state.logger.debug2(
            (
                "TRANSACTION: sender: %s | to: %s | value: %s | gas: %s | "
                "gas-price: %s | s: %s | r: %s | y_parity: %s | data-hash: %s"
            ),
            encode_hex(transaction.sender),
            encode_hex(transaction.to),
            transaction.value,
            transaction.gas,
            transaction.gas_price,
            transaction.s,
            transaction.r,
            transaction.y_parity,
            encode_hex(keccak(transaction.data)),
        )

        message = Message(
            gas=message_gas,
            to=transaction.to,
            sender=transaction.sender,
            value=transaction.value,
            data=data,
            code=code,
            create_address=contract_address,
        )
        return message

    def finalize_computation(self,
                             transaction: SignedTransactionAPI,
                             computation: ComputationAPI) -> ComputationAPI:
        # Self Destruct Refunds
        num_deletions = len(computation.get_accounts_for_deletion())
        if num_deletions:
            computation.refund_gas(REFUND_SELFDESTRUCT * num_deletions)

        # Gas Refunds
        gas_remaining = computation.get_gas_remaining()
        gas_refunded = computation.get_gas_refund()
        gas_used = transaction.gas - gas_remaining
        gas_refund = min(gas_refunded, gas_used // 2)
        gas_refund_amount = (gas_refund + gas_remaining) * transaction.gas_price

        if gas_refund_amount:
            self.vm_state.logger.debug2(
                'TRANSACTION REFUND: %s -> %s',
                gas_refund_amount,
                encode_hex(computation.msg.sender),
            )

        self.add_fee_token_balance(computation.msg.sender, gas_refund_amount)

        # Miner Fees
        transaction_fee = \
            (transaction.gas - gas_remaining - gas_refund) * transaction.gas_price
        self.vm_state.logger.debug2(
            'TRANSACTION FEE: %s -> %s',
            transaction_fee,
            encode_hex(self.vm_state.coinbase),
        )

        fee_token_balance = self.get_fee_token_balance(self.vm_state.coinbase)

        self.add_fee_token_balance(self.vm_state.coinbase, transaction_fee)

        # Process Self Destructs
        for account, _ in computation.get_accounts_for_deletion():
            # TODO: need to figure out how we prevent multiple selfdestructs from
            # the same account and if this is the right place to put this.
            self.vm_state.logger.debug2('DELETING ACCOUNT: %s', encode_hex(account))

            # TODO: this balance setting is likely superflous and can be
            # removed since `delete_account` does this.
            self.vm_state.set_balance(account, 0)
            self.vm_state.delete_account(account)

        return computation

class Simple3State(FrontierState):
    computation_class = Simple3Computation
    transaction_executor_class: Type[TransactionExecutorAPI] = Simple3TransactionExecutor

    def validate_transaction(self, transaction: SignedTransactionAPI) -> None:
        validate_simple3_transaction(self, transaction)
