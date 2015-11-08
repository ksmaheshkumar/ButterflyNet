import asyncio
# import bfnet.structures


# Python 3.4 compatibility code.
import logging
import types

import Butterfly


try:
    asyncio.ensure_future
except AttributeError:
    asyncio.ensure_future = asyncio.async


class Net(....__class__.__class__.__base__):  # you are ugly and should feel bad.
    """
    A Net is an object that catches :class:`Butterfly` connections that happen to wander in to your net.
    """


    def __init__(self, ip: str, port: int, loop: asyncio.AbstractEventLoop = None,
            server: asyncio.AbstractServer = None):
        """
        Create a new :class:`Net` object.

        This should not be called directly - instead use :func:`bfnet.structures.ButterflyHandler.create_server` to create a server.
        :param ip: The IP to bind on.
        :param port: The port to use.
        :param loop: The event loop to use.
        :param server: The asyncio server to use.
        """
        self.loop = loop
        self.port = port
        self.ip = ip
        self.handler = None
        self.server = server

        self.logger = logging.getLogger("ButterflyNet")

        self.logger.info("Net running on {}:{}.".format(ip, port))


    def _set_handler(self, handler):
        self.handler = handler

    @asyncio.coroutine
    def handle(self, butterfly: Butterfly):
        """
        Default handler.

        This, by default, distributes the incoming data around into handlers. After failing these, it will drop down to `default_data` handler.
        :param butterfly: The butterfly to use for handling.
        """
        # Enter an infinite loop.
        self.logger.debug("Dropped into handler for new client")
        while True:
            data = yield from butterfly.read()
            if not data:
                break
            else:
                self.logger.debug("Recieved data: {}".format(data))
                yield from self._default_handler(butterfly, data)

        self.logger.info("Client {}:{} disconnected.".format(*butterfly._writer.get_extra_info("peername")))

    def _default_handler(self, butterfly: Butterfly, data: bytes):
        """
        This is an example handler. It does nothing.
        :param butterfly: The butterfly object.
        :param data: The data to be passed in.
        :return: Nothing
        """
        self.logger.warning()

    def set_default_data_handler(self, handler: types.FunctionType):
        """
        Set a new default data handler - one to be dropped to if nothing else matches.

        By default this just passes.
        :param handler:
        :return:
        """
        self._default_handler = handler
