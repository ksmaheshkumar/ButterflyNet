"""
Copyright (C) 2015 Isaac Dickinson

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import types

from bfnet.Net import Net


class PacketNet(Net):
    """
    A PacketNet is a special type of Net that works on Packets
    instead of data.
    """
    def __init__(self, ip, port, loop, server):
        super().__init__(ip, port, loop, server)
        # Set the real handler.
        self._real_handler = None

    def handle(self, butterfly):
        """
        Stub method that calls your REAL handler.

        This would normally be a coroutine, but a task will be created from
        the returned handler.
        """
        try:
            return self._real_handler(butterfly)
        except TypeError as e:
            raise TypeError("Packet handler has not been set.") from e

    def set_handler(self, func: types.GeneratorType):
        """
        Set the default Packet handler.

        This can be used as a decorator, or as a normal call.

        The handler MUST be a coroutine.

        This handler MUST be an infinite loop. Failure to do so will mean your packets will stop being
        handled after one packet arrives.
        :param func: The function to set as the handler.
        :return: Your function back.
        """
        self._real_handler = func
        return func
