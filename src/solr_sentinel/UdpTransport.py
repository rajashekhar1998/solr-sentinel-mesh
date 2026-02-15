import asyncio
from typing import Optional


from src.solr_sentinel import PacketStructure

class UdpTransport(asyncio.DatagramProtocol):
    # It can be confusing because asyncio.DatagramProtocol works differently than standard Python classes.
    # You don't "call" its methods; the Operating System (via asyncio) calls them.

    # --- PART 1: SETUP ---
    def __init__(self, on_message):
        # This is the base setup
        # We store the callback function to talk to the rest of the app
        # Here callback function is the connecting component between network and the app[brain/business-logic]
        # And transport is the socket
        self.on_message_callback = on_message
        self.transport : Optional[asyncio.DatagramTransport] = None

    def connection_made(self, transport):
        # Asyncio calls this ONE TIME when the socket opens.
        # CAPTURE THE TRANSPORT! It is your only way to send data.
        self.transport = transport
        print("UDP Transport: Socket is open and listening. Ready to send/receive.")

    # --- PART 2: INPUT (Events from OS) ---
    def datagram_received(self, data: bytes, addr: tuple):
        # Asyncio calls this EVERY TIME a packet arrives.
        try:
            # 1. Decode (Bytes -> Str)
            decoded_data = data.decode("utf-8")

            # 2. Validate (Str -> Pydantic Object)
            packet = PacketStructure.model_validate_json(decoded_data)

            # 3. Hand off (Object -> Callback)
            self.on_message_callback(packet, addr)

        except Exception as e:
            # Handle bad data
            print(f"UDP datagram receiver error form {addr}: {e}")
            pass

    # --- PART 3: OUTPUT (Actions by us) ---
    def send_packet(self, packet_obj: PacketStructure, target_addr: tuple):
        """
        serialize, encode and send
        """
        # YOU call this when you want to send a PING or ACK.
        if self.transport:
            try:
                data_bytes = packet_obj.model_dump_json().encode("utf-8")
                self.transport.sendto(data_bytes, target_addr)
            except Exception as e:
                print(f"Error sending to {target_addr}: {e}")
        else:
            print("Transport is not ready dude")