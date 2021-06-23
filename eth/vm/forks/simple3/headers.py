from eth.vm.forks.frontier.headers import (
    configure_frontier_header,
    create_frontier_header_from_parent,
    compute_frontier_difficulty,
)


compute_simple3_difficulty = compute_frontier_difficulty
create_simple3_header_from_parent = create_frontier_header_from_parent
configure_simple3_header = configure_frontier_header
