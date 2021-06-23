import copy
from eth.vm.forks.frontier.opcodes import (
    FRONTIER_OPCODES,
)


SIMPLE2_OPCODES = copy.deepcopy(FRONTIER_OPCODES)
