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
    Simple3Transaction,
)


class Simple3Block(FrontierBlock):
    transaction_builder = Simple3Transaction  # type: ignore
    fields = [
        ('header', BlockHeader),
        ('transactions', CountableList(transaction_builder)),
        ('uncles', CountableList(BlockHeader))
    ]
