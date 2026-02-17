from typing import Optional, Dict, Any

from pydantic import BaseModel
from datetime import datetime
from ipaddress import IPv4Address

from src.solr_sentinel.MessageType import MessageType
from src.solr_sentinel.NodeState import NodeState


class PacketStructure(BaseModel):
    type : MessageType
    host_address : str
    time_stamp : datetime
    status : NodeState

    class Config:
        use_enum_values = True



