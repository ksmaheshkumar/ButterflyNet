import asyncio
import logging
import ssl

from bfnet.BFHandler import ButterflyHandler
from .Packets import BasePacket
from .PacketButterfly import PacketButterfly
from .PacketNet import PacketNet


class PacketHandler(ButterflyHandler):
    """
    A PacketHandler is a type of Handler that allows you to send/recieve Packets instead
    of using raw data.

    It is a step above the normal ButterflyNet bytes layer, by instead using structures
    for easy OO-style networking information.
    """


    def __init__(self, event_loop: asyncio.AbstractEventLoop, ssl_context: ssl.SSLContext = None,
            loglevel: int = logging.DEBUG, buffer_size: int = asyncio.streams._DEFAULT_LIMIT):
        super().__init__(event_loop, ssl_context, loglevel, 0)

        # Define a new dict of Packet types.
        self.packet_types = {}
        # Define the basic packet type.
        self.basic_packet_type = BasePacket

        # Define the default Net type.
        self.default_net = PacketNet

    @asyncio.coroutine
    def on_connection(self, butterfly: PacketButterfly):
        """
        on_connection but with a different annotation.
        """
        super().on_connection(butterfly)

    @asyncio.coroutine
    def on_disconnect(self, butterfly: PacketButterfly):
        """
        on_disconnect but with a different annotation.
        """
        super().on_connection(butterfly)

    def butterfly_factory(self):
        """
        Creates a new PacketedButterfly instead of a normal Butterfly.
        :return: A new :class:`bfnet.packets.PacketButterfly`.
        """
        return PacketButterfly(self, self._event_loop)



