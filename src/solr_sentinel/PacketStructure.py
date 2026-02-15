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

packet = PacketStructure(
    type = MessageType.PING,
    host_address = "solr-1",
    time_stamp = datetime.now(datetime.UTC),
    status = NodeState.LOCAL
)

json_payload = packet.model_dump_json()



