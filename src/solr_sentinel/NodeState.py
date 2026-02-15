from enum import Enum


class NodeState(Enum):
    LOCAL = 1
    SISTER = 2
    WEB = 3
    ORPHAN = 4