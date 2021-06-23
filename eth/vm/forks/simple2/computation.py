from eth.vm.forks.frontier.computation import (
    FRONTIER_PRECOMPILES
)
from eth.vm.forks.frontier.computation import (
    FrontierComputation,
)

from .opcodes import SIMPLE2_OPCODES

SIMPLE2_PRECOMPILES = FRONTIER_PRECOMPILES


class Simple2Computation(FrontierComputation):
    """
    A class for all execution computations in the ``Simple2`` fork.
    Inherits from :class:`~eth.vm.forks.constantinople.frontier.FrontierComputation`
    """
    # Override
    opcodes = SIMPLE2_OPCODES
    _precompiles = SIMPLE2_PRECOMPILES
