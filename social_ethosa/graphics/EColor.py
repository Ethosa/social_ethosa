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
        color = "#{:02x}{:02x}{:02x}{:02x}".format(color[3], color[0], color[1], color[2])
        if color in colors:
            return colors[color]
        return (int(re.sub("#", "0x", color), 0)).to_bytes(4, byteorder="little")
    elif isinstance(color, str):
        if color in colors:
            return colors[color]
        return (int(re.sub("#", "0x", color), 0)).to_bytes(4, byteorder="little")
    elif isinstance(color, int):
        return (color).to_bytes(4, byteorder="little")
    elif isinstance(color, bytes):
        return color
