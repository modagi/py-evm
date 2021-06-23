from eth_utils import (
    ValidationError,
)

from eth.abc import (
    BlockHeaderAPI,
    SignedTransactionAPI,
    StateAPI,
    VirtualMachineAPI,
)


def validate_simple3_transaction(state: StateAPI,
                                  transaction: SignedTransactionAPI) -> None:
    gas_cost = transaction.gas * transaction.gas_price
    sender_balance_eth = state.get_balance(transaction.sender)
    # TODO: get from abstract method in StateAPI
    '''
    sender_balance = state.get_fee_token_balance(transaction.sender)

    if sender_balance < gas_cost:
        raise ValidationError(
            f"Sender {transaction.sender!r} cannot afford txn gas "
            f"{gas_cost} with account balance {sender_balance}"
        )
    '''

    total_cost = transaction.value

    if sender_balance_eth < transaction.value:
        raise ValidationError("Sender account balance cannot afford txn")

    sender_nonce = state.get_nonce(transaction.sender)
    if sender_nonce != transaction.nonce:
        raise ValidationError(
            f"Invalid transaction nonce: Expected {sender_nonce}, but got {transaction.nonce}"
        )

def validate_simple3_transaction_against_header(_vm: VirtualMachineAPI,
                                                 base_header: BlockHeaderAPI,
                                                 transaction: SignedTransactionAPI) -> None:
    pass
