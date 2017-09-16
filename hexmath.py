# -*- coding: utf-8 -*-
"""
Hexagonal Grid Generator
(c) Michael McDermott, for One Hudson
"""

import math

LTM = True
building_44 = [47.641387,-122.132817]
centroid = building_44
latfud = 0.9985/math.cos(math.radians(centroid[0]))
lonfud = 0.9981
SIN60 = math.sin(math.radians(60))

def get_hex_neighbors((x, y), major=1, ltm=LTM):
    if ltm:
        major /= 111120.
    aa = 1.5 * major * lonfud
    cc = major * SIN60 * latfud
    lst = [(x, y + 2 * cc), (x + aa, y + cc), (x + aa, y - cc),
           (x - aa, y - cc), (x, y - 2 * cc), (x - aa, y + cc)]
    return lst


def latlon_hash((x, y), prec=6):
    """ "rounds" a location
    prec = precision (decimal digits of longitude degrees)
    6: about 11 cm resolution
    5: about 1.1 m

    """
    x = abs(round(x, prec))
    y = abs(round(y, prec))
    return str(x) + str(y)


def generate_hexgrid((x, y), depth=2, major=10):
    hexcenters = [(x, y)]
    hexhashes = [latlon_hash((x, y))]
    lastshellsize = 0
    for idx in range(2, depth + 1):
        active = hexcenters[-lastshellsize:]
        for node in active:
            newnodes = get_hex_neighbors(node[:2], major)
            for newnode in newnodes:
                llhash = latlon_hash(newnode)
                if llhash not in hexhashes:
                    hexcenters.append(newnode)
                    hexhashes.append(llhash)
        lastshellsize += 6
    return hexcenters
