# -*- coding: utf-8 -*-
# author: Ethosa

import re

colors = {
    "white" : b"\xFF\xFF\xFF\xFF",
    "black" : b"\x00\x00\x00\xFF",
    "red" : b"\x00\x00\xFF\xFF",
    "green" : b"\x00\xFF\x00\xFF",
    "blue" : b"\xFF\x00\x00\xFF"
}

def ecolor(color=b"\xFF\xFF\xFF\xFF"):
    if isinstance(color, tuple) or isinstance(color, list):
        return (color[3] & 0xff) << 24 | (color[0] & 0xff) << 16 | (color[1] & 0xff) << 8 | (color[1] & 0xff).to_bytes(4, byteorder="little")
    elif isinstance(color, str):
        if color in colors:
            return colors[color]
        return (int(re.sub("#", "0x", color), 0)).to_bytes(4, byteorder="little")
    elif isinstance(color, int):
        return (color).to_bytes(4, byteorder="little")
    elif isinstance(color, bytes):
        return color
