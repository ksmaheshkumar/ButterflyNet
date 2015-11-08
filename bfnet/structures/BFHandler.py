import asyncio
import ssl

import _ssl
import types

from bfnet.Net import Net
from bfnet.Butterfly import Butterfly
import logging


class ButterflyHandler(object):
    """
    A ButterflyHandler is a class that describes what happens when a Butterfly is caught by a net.

    It has several methods that are automatically called at critical stages in the connection:
        - :func:`ButterflyHandler.on_connection`
        - :func:`ButterflyHandler.on_disconnect`

    These methods are called at the appropriate time, as their name describes.
    """
    instance = None


    def __init__(self, event_loop: asyncio.AbstractEventLoop, ssl_context: ssl.SSLContext = None,
            loglevel: int = logging.DEBUG, butterfly_factory=None, buffer_size: int = asyncio.streams._DEFAULT_LIMIT):
        """
        TODO: Add better constructor.
        :param event_loop: The :class:`asyncio.BaseEventLoop` to use for the server.
        :param ssl_context: The :class:`ssl.SSLContext` to use for the server.
        :param loglevel: The logging level to use.
        """
        self._event_loop = event_loop
        self._server = None
        if not ssl_context:
            # This looks very similar to the code for create_default_context
            # That's because it is the code
            # For some reason, create_default_context doesn't like me and won't work properly
            self._ssl = ssl.SSLContext(protocol=ssl.PROTOCOL_SSLv23)
            # SSLv2 considered harmful.
            self._ssl.options |= ssl.OP_NO_SSLv2

            # SSLv3 has problematic security and is only required for really old
            # clients such as IE6 on Windows XP
            self._ssl.options |= ssl.OP_NO_SSLv3
            self._ssl.load_default_certs(ssl.Purpose.SERVER_AUTH)
            self._ssl.options |= getattr(_ssl, "OP_NO_COMPRESSION", 0)
            self._ssl.set_ciphers(ssl._RESTRICTED_SERVER_CIPHERS)
            self._ssl.options |= getattr(_ssl, "OP_CIPHER_SERVER_PREFERENCE", 0)

        else:
            self._ssl = ssl_context

        self._bufsize = buffer_size

        self.net = None
        self.logger = logging.getLogger("ButterflyNet")
        self.logger.setLevel(loglevel)
        if self.logger.level >= logging.DEBUG:
            self._event_loop.set_debug(True)


    @asyncio.coroutine
    def _inbound_data_cb(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        """
        Internal callback used for an initial connection from the server.

        Do not touch.
        :param reader: The :class:`asyncio.StreamReader` object called back.
        :param writer: The :class:`asyncio.StreamWriter` object called back.
        :return: Nothing.
        """
        self.logger.info("Recieved new connection from {}:{}".format(*writer.get_extra_info("peername")))
        # Create a new butterfly.)
        our_butterfly = self.butterfly_factory(reader, writer)
        yield from self.on_connection(our_butterfly)
        yield from self.net.handle(our_butterfly)
        yield from self.on_disconnect(our_butterfly)


    @asyncio.coroutine
    def on_connection(self, butterfly: Butterfly):
        """
        Stub for an on_disconnect event.
        :param butterfly: The butterfly object created.
        :return:
        """
        ...


    @asyncio.coroutine
    def on_disconnect(self, butterfly: Butterfly):
        """
        Stub for an on_disconnect event.
        :param butterfly: The butterfly object created.
        :return:
        """
        ...


    def butterfly_factory(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> Butterfly:
        """
        This is the default factory for Butterfly objects.

        This will take in a reader and writer pair, and generate a butterfly object from it.

        If you need custom data or a custom class, override this method and use your own instead.
        :param reader: The :class:`asyncio.StreamReader` object called back.
        :param writer: The :class:`asyncio.StreamWriter` object called back.
        :return: A new :class:`Butterfly` object.
        """
        return Butterfly(reader, writer, self, self._bufsize)


    def _load_ssl(self, ssl_options: tuple):
        """
        Internal call used to load SSL parameters from the SSL option tuple.

        Do not touch.
        :param ssl_options: The SSL options to use.
        """
        self._ssl.load_cert_chain(certfile=ssl_options[0], keyfile=ssl_options[1], password=ssl_options[2])


    @classmethod
    def get_handler(cls, loop: asyncio.AbstractEventLoop = None, ssl_context: ssl.SSLContext = None,
            log_level: int = logging.INFO, butterfly_factory: types.FunctionType = None,
            buffer_size: int = asyncio.streams._DEFAULT_LIMIT):
        """
        Get the instance of the handler currently running.
        """
        if not cls.instance:
            cls.instance = cls(loop, ssl_context, log_level, butterfly_factory, buffer_size)
        return cls.instance


    @asyncio.coroutine
    def create_server(self, bind_options: tuple, ssl_options: tuple) -> Net:
        """
        Create a new server using the event loop specified.

        This method is a coroutine.
        :param bind_options: The IP and port to bind to on the server.
        :param ssl_options: A tuple of SSL options:
            - The certificate file to use
            - The private key to use
            - The private key password, or None if it does not have a password.
        :return: A :class:`bfnet.Net.Net` object.
        """

        # Load SSL.
        self._load_ssl(ssl_options)

        # Create a factory for streamreaders.
        def factory():
            reader = asyncio.StreamReader(limit=2 ** 16, loop=self._event_loop)
            protocol = asyncio.StreamReaderProtocol(reader, self._inbound_data_cb, loop=self._event_loop)
            return protocol


        # Create the server.
        host, port = bind_options
        self._server = yield from self._event_loop.create_server(factory, host=host, port=port, ssl=self._ssl)
        self.net = Net(ip=host, port=port, loop=self._event_loop, server=self._server)
        self.net._set_handler(self)
        return self.net
