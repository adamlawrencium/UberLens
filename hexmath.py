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

def get_hex_neighbors(x, y, major, ltm=LTM):
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


def generate_hexgrid(x, y, depth, major):
    hexcenters = [(x, y)]
    hexhashes = [latlon_hash((x, y))]
    lastshellsize = 0

    # Loop through main layers
    for idx in range(2, depth + 1):
        active = hexcenters[-lastshellsize:]

        # Loop through outermost layer
        for node in active:
            newnodes = get_hex_neighbors(node[0], node[1], major)
            for n in newnodes:
                print n
            # print newnodes
            # return
            # Loop through outermost nodes' neighbors
            for newnode in newnodes:
                llhash = latlon_hash(newnode)
                if llhash not in hexhashes:
                    hexcenters.append(newnode)
                    hexhashes.append(llhash)
        lastshellsize += 6
    return hexcenters


if __name__ == "__main__": 
    # a = get_hex_neighbors(47.641387, -122.132817, 1, True)
    a = generate_hexgrid(47.641387, -122.132817, 3, 10)

    # for x in a: 
        # print x