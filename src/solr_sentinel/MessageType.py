from enum import Enum


class MessageType(Enum):
    PING = "PING"
    ACK = "ACK"
    PING_REQ = "PING_REQ"