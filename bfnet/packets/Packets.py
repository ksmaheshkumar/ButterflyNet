import struct


class BasePacket(object):
    """
    A BasePacket is the base class for all Packet types.

    This just creates a few stub methods.
    """

    # Define a default id.
    # Packet IDs are ALWAYS unsigned, so this will never meet.
    id = -1

    # Define a default endianness.
    # This is ">" for network endianness by default.
    _endianness = ">"

    def __init__(self, pbf):
        """
        Default init method.
        """
        self.butterfly = pbf

    def on_creation(self):
        """
        Called just after your packet object is created.
        """
        pass

    def create(self, data: bytes):
        """
        Create a new Packet.
        :param data: The data to use.
        :return: If the creation succeeded or not.
        """
        self.on_creation()


class Packet(BasePacket):
    """
    A standard Packet type.

    This extends from BasePacket, and adds useful details that you'll want to use.
    """

    def __init__(self, pbf):
        """
        Create a new Packet type.
        :return:
        """
        super().__init__(pbf)
        self._original_data = b""


    def create(self, data: bytes) -> bool:
        """
        Create a new Packet.
        :param data: The data to use.
            This data should have the PacketButterfly header stripped.
        :return: A boolean, True if we need no more processing, and False if we process ourself.
        """
        self._original_data = data
        self.unpack(data)
        return True

    def unpack(self, data: bytes) -> bool:
        """
        Unpack the data for the packet.
        :return: A boolean, if it was unpacked.
        """
        return True


    def gen(self) -> bytes:
        """
        Generate a new set of data to write to the connection.
        :return:
        """
