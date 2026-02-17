import json
from unittest.mock import MagicMock

from src.solr_sentinel.UdpTransport import UdpTransport
from src.solr_sentinel.PacketStructure import PacketStructure

def test_datagram_received_parses_correctly():
    """
    create the callback?

    :return:
    """
    print("Starting test")
    mock_callback = MagicMock()

    transport_layer = UdpTransport(on_message=mock_callback)

    fake_json_data = {
        "type": "PING",
        "host_address": "test-node",
        "status": "LOCAL",
        "time_stamp": "2026-01-01T12:00:00"
    }
    fake_addr = ("127.0.0.1", 5000)
    fake_json_bytes = json.dumps(fake_json_data).encode("utf-8")

    transport_layer.datagram_received(fake_json_bytes, fake_addr)

    mock_callback.assert_called_once()

    args = mock_callback.call_args[0]
    packet_obj = args[0]
    addr_arg = args[1]

    assert addr_arg == fake_addr
    assert packet_obj.host_address == "test-node"
    print("\n Datagram receiver Test passed")

if __name__ == "__main__":
    test_datagram_received_parses_correctly()
