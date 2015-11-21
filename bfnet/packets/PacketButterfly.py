import asyncio
import struct
from bfnet.Butterfly import AbstractButterfly


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
            packet = packet_type(self)
            created = packet.create(data[6:])
            if created:
                self._loop.create_task(self.packet_queue.put(packet))
        else:
            self.logger.warning("Recieved unknown packet ID: {}".format(id))


    def connection_lost(self, exc):
        class FakeQueue(object):
            def get(self):
                return None

            @asyncio.coroutine
            def put(self):
                return

        self.packet_queue = FakeQueue()
        super().connection_lost(exc)


    def read(self):
        """
        Get a new packet off the Queue.
        """
        return (yield from self.packet_queue.get())


    def write(self, pack):
        """
        Write a packet to the client.
        :param pack: The packet to write. This will automatically add a header.
        """
        header = self.unpacker.pack(b"BF", 1, pack.id)
        print(header, pack.gen())
        self._transport.write(header + pack.gen())
