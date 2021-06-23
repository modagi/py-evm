from eth_keys.datatypes import PrivateKey
from eth_typing import Address

from eth.vm.forks.frontier.transactions import (
    FrontierTransaction,
    FrontierUnsignedTransaction,
)

from eth._utils.transactions import (
    create_transaction_signature,
)


class Simple2Transaction(FrontierTransaction):
    @classmethod
    def create_unsigned_transaction(cls,
                                    *,
                                    nonce: int,
                                    gas_price: int,
                                    gas: int,
                                    to: Address,
                                    value: int,
                                    data: bytes) -> 'Simple2UnsignedTransaction':
        return Simple2UnsignedTransaction(nonce, gas_price, gas, to, value, data)


class Simple2UnsignedTransaction(FrontierUnsignedTransaction):
    def as_signed_transaction(self,
                              private_key: PrivateKey,
                              chain_id: int = None) -> Simple2Transaction:
        v, r, s = create_transaction_signature(self, private_key, chain_id=chain_id)
        return Simple2Transaction(
            nonce=self.nonce,
            gas_price=self.gas_price,
            gas=self.gas,
            to=self.to,
            value=self.value,
            data=self.data,
            v=v,
            r=r,
            s=s,
        )