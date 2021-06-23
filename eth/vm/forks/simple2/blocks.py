from rlp.sedes import (
    CountableList,
)
from eth.rlp.headers import (
    BlockHeader,
)
from eth.vm.forks.frontier.blocks import (
    FrontierBlock,
)

from eth.rlp.receipts import (
    Receipt,
)
from .transactions import (
    Simple2Transaction,
)


class Simple2Block(FrontierBlock):
    transaction_builder = Simple2Transaction  # type: ignore
    fields = [
        ('header', BlockHeader),
        ('transactions', CountableList(transaction_builder)),
        ('uncles', CountableList(BlockHeader))
    ]
