from typing import (
    Type,
)

from eth.rlp.blocks import BaseBlock
from eth.vm.forks.frontier import (
    FrontierVM,
)
from eth.vm.state import BaseState

from .blocks import Simple3Block
from .headers import (
    compute_simple3_difficulty,
    configure_simple3_header,
    create_simple3_header_from_parent,
)
from .state import Simple3State
from .validation import validate_simple3_transaction_against_header


class Simple3VM(FrontierVM):
    # fork name
    fork = 'simple3'

    # classes
    block_class: Type[BaseBlock] = Simple3Block
    _state_class: Type[BaseState] = Simple3State

    # Methods
    validate_transaction_against_header = validate_simple3_transaction_against_header
