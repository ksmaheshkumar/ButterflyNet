import asyncio
import logging


class Butterfly(object):
    """
    A butterfly represents a client object that has connected to your server.

    It exposes a bunch of useful properties:
        - The IP/Port of the connected client
        - The streamreader/streamwriter for the client

    This is just a base class. It is HIGHLY recommended you extend this class with your own methods.
    """
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter,
                    handler, bufsize):
        self._reader = reader
        self._writer = writer
        self.handler = handler
        self._bufsize = bufsize

    @asyncio.coroutine
    def read(self) -> bytes:
        """
        Read data off the stream.
        :return: Bytes containing the data read.
        """
        data = yield from self._reader.read(self._bufsize)
        return data

    @asyncio.coroutine
    def drain(self):
        yield from self._writer.drain()

    def write(self, data: bytes):
        """
        Write some data to the stream.
        :param data: The data to write.
        """
        self._writer.write(data)



