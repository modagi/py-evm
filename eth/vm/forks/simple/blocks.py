from rlp.sedes import (
    CountableList,
)
from eth.rlp.headers import (
    BlockHeader,
)
from eth.vm.forks.berlin.blocks import (
    BerlinBlock,
)

from eth.vm.forks.berlin.receipts import (
    BerlinReceiptBuilder,
)
from eth.vm.forks.berlin.transactions import (
    BerlinTransactionBuilder,
)


class SimpleBlock(BerlinBlock):
    transaction_builder = BerlinTransactionBuilder  # type: ignore
    receipt_builder = BerlinReceiptBuilder  # type: ignore
    fields = [
        ('header', BlockHeader),
        ('transactions', CountableList(transaction_builder)),
        ('uncles', CountableList(BlockHeader))
    ]
