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

"""
Misc utils for deep internal usage of Python.
"""
import struct


def infer_int_pack(arg) -> str:
    """
    Attempt to infer the correct struct format for an int.
    :param arg: The integer argument to infer.
    :return: A character for the struct string.
    """
    # Short
    if (-32768) <= arg <= 32767:
        return "h"
    # Int
    elif (-2147483648) <= arg <= 2147483647:
        return "i"
    # Long Long, I think
    elif (-18446744073709551616) <= arg <= 18446744073709551615:
        return "q"
    else:
        raise OverflowError("Number {} too big to fit into a struct normally".format(arg))


def _process_args(*args):
    a = []
    for arg in args:
        if isinstance(arg, str):
            for _ in arg:
                a.append(_)
        elif isinstance(arg, bytes):
            for _ in arg:
                a.append(_.to_bytes(1, "big"))
        else:
            a.append(arg)
    return tuple(a)


def auto_infer_struct_pack(*args, pack: bool=False) -> str:
    """
    This will automatically attempt to infer the struct pack/unpack format string
    from the types of your arguments.

    All integer values will be set as unsigned by default.

    :param pack: Should we automatically pack your data up?
    :param args: The items to infer from.
    :return: Either the string format string, or the packed bytes data.
    """
    # Set the fmt string
    fmt_string = "!"
    for arg in args:
        if type(arg) == int:
            # Complicated stuff here.
            fmt_string += infer_int_pack(arg)
        elif type(arg) == float:
            # Use a double.
            fmt_string += "d"
        elif type(arg) == str:
            # Use a char[] s
            fmt_string += "{}s".format(len(arg))
        elif type(arg) == bytes:
            # Use a normal 'c'
            fmt_string += "{}c".format(len(arg))
        elif type(arg) == bool:
            fmt_string += "?"
        else:
            raise ValueError("Type could not be determined - {}".format(type(arg)))
    if not pack:
        return fmt_string
    # Pack data.
    s = struct.pack(fmt_string, *_process_args(*args))
    return s
