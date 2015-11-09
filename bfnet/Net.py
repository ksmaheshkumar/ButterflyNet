import asyncio
# import bfnet.structures


# Python 3.4 compatibility code.
import logging
import types

import re

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
        self.bf_handler = None
        self.server = server

        self.handlers = []

        self.logger = logging.getLogger("ButterflyNet")

        self.logger.info("Net running on {}:{}.".format(ip, port))


    def _set_bf_handler(self, handler):
        self.bf_handler = handler


    @asyncio.coroutine
    def handle(self, butterfly: Butterfly):
        """
        Default handler.

        This, by default, distributes the incoming data around into handlers. After failing these, it will drop down to `default_data` handler.
        :param butterfly: The butterfly to use for handling.
        """
        # Enter an infinite loop.
        self.logger.debug("Dropped into default handler for new client")
        while True:
            data = yield from butterfly.read()
            if not data:
                break
            else:
                yield from self._default_handler(butterfly, data)

    @asyncio.coroutine
    def _default_handler(self, butterfly: Butterfly, data: bytes):
        """
        This is an example handler. It does nothing.
        :param butterfly: The butterfly object.
        :param data: The data to be passed in.
        :return: Nothing
        """
        self.logger.warning("Uncollected message! {}".format(data))

    @classmethod
    def set_default_data_handler(cls, handler: types.FunctionType):
        """
        Set a new default data handler - one to be dropped to if nothing else matches.

        By default this just passes.

        This is a *classmethod* - this will set it on the class instead of the instance.
        :param handler: Any callable to use as a handler.
        """
        cls._default_handler = handler


    # Begin helper decorators

    def regexp_match(self, regexp: str):
        # Real decorator here.
        def real_decorator(func: types.FunctionType):
            # Compile the regexp pattern.
            pattern = re.compile(regexp)

            # Create a match function.
            def match(data: bytes):
                # Match it - if it works, return the func. Else, return None.
                data = data.decode()
                if pattern.match(data):
                    return func
                else:
                    return None


            self.handlers.append(match)
            return func


        return real_decorator


    def prefix_match(self, prefix: str, start=None, end=None):
        def real_decorator(func: types.FunctionType):
            def match(data: bytes):
                data = data.decode()
                if data.startswith(prefix=prefix, start=start, end=end):
                    return func
                else:
                    return None


            self.handlers.append(match)
            return func
        return real_decorator
