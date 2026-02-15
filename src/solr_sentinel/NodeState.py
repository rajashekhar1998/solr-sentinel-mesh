from enum import Enum


class NodeState(Enum):
    LOCAL = "LOCAL"
    SISTER = "SISTER"
    WEB = "WEB"
    ORPHAN = "ORPHAN"