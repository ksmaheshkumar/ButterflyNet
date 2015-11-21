import asyncio
import struct

from bfnet.Butterfly import AbstractButterfly
from bfnet.packets import Packet


class PacketButterfly(AbstractButterfly):
    """
    A packeted Butterfly uses a Queue of Packets instead of
    a StreamReader/StreamWriter.
    """
    unpacker = struct.Struct("!2shh")


    def __init__(self, handler, loop: asyncio.AbstractEventLoop, max_packets=0):
        """
        Create a new Packeted Butterfly.
        """
        # First, super call it.
        super().__init__(handler, loop)

        # Create a new Packet queue.
        self.packet_queue = asyncio.Queue(loop=self._loop)

    @property
    def handler(self):
        return self._handler

    def data_received(self, data: bytes):
        """
        Parses out the Packet header, to create an appropriate new
        Packet object.
        :param data: The data to parse in.
        """
        self.logger.debug("Recieved new packet, deconstructing...")
        if len(data) < 6:
            self.logger.error("Invalid packet recieved, dropping client.")
            self.stop()
            return
        # Decode the header.
        header = data[0:6]
        try:
            magic, version, id = self.unpacker.unpack(header)
        except struct.error as e:
            self.logger.error("Failure unpacking packet header: {}".format(e.args))
            self.stop()
            return
        # Check header.
        if magic != b"BF":
            self.logger.error("Recieved unknown packet with magic number {}".format(magic.decode()))
            self.stop()
            return
        self.logger.debug("Packet version {}, id {}".format(version, id))
        # Get the packet, if possible.
        if id in self._handler.packet_types:
            packet_type = self._handler.packet_types[id]
            assert isinstance(packet_type,
                self._handler.basic_packet_type), "Packet should be similar to the normal packet type"
            packet = packet_type(self)
            created = packet.create(data[6:])
            if created:
                self._loop.create_task(self.packet_queue.put(packet))
        else:
            self.logger.warning("Recieved unknown packet ID: {}".format(id))


    def read(self) -> Packet:
        """
        Get a new packet off the Queue.
        """
        return (yield from self.packet_queue.get())


    def write(self, pack: Packet):
        """
        Write a packet to the client.
        :param pack: The packet to write. This will automatically add a header.
        """
        header = self.unpacker.pack(b"BF" + pack.id.to_bytes(2, "big"))
        self._transport.write(header + pack.gen())
