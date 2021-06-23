from typing import (
    Type,
)

from eth.rlp.blocks import BaseBlock
from eth.vm.forks.frontier import (
    FrontierVM,
)
from eth.vm.state import BaseState

from .blocks import Simple2Block
from .headers import (
    compute_simple2_difficulty,
    configure_simple2_header,
    create_simple2_header_from_parent,
)
from .state import Simple2State
from .validation import validate_simple2_transaction_against_header


class Simple2VM(FrontierVM):
    # fork name
    fork = 'simple2'

    # classes
    block_class: Type[BaseBlock] = Simple2Block
    _state_class: Type[BaseState] = Simple2State

    # Methods
    validate_transaction_against_header = validate_simple2_transaction_against_header
