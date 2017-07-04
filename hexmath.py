# -*- coding: utf-8 -*-
"""
Hexagonal Grid Generator
(c) Michael McDermott, for One Hudson
"""

import math
import random
import params
import gmplot

# import fileclerk

SIN60 = math.sin(math.radians(60))


def dist(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def hexagon_number(n):
    """centered hexagon number, minus the innermost tile
    :param n:
    """
    return 6 * (n * (n - 1) / 2)


def get_hex_pts((x, y), major=1, ltm=params.LTM):
    """
    (x, y) is origin coordinates
    major is distance from center of hexagon to vertex
    if ltm flag is True, then this assumes x,y is in lat,long and major is in meters.
    This automatically converts meters into lat-long degrees. Assumes no curvature
    :type major: object
    :param major:
    :type ltm: bool
    :param ltm:
    """
    if ltm:
        major /= 111120.
    bb = major / 2.
    cc = major * SIN60
    lst = [(x - major, y), (x - bb, y + cc), (x + bb, y + cc),
           (x + major, y), (x + bb, y - cc), (x - bb, y - cc)]

    return lst


def get_hex_neighbors((x, y), major=1, ltm=params.LTM):
    if ltm:
        major /= 111120.
    aa = 1.5 * major * params.lonfud
    # bb = major/2.
    cc = major * SIN60 * params.latfud
    lst = [(x, y + 2 * cc), (x + aa, y + cc), (x + aa, y - cc),
           (x - aa, y - cc), (x, y - 2 * cc), (x - aa, y + cc)]
    return lst


def latlon_hash((x, y), prec=6):
    """ "rounds" a location
    prec = precision (decimal digits of longitude degrees)
    6: about 11 cm resolution
    5: about 1.1 m

    """
    # d1 = dist((x,y),centroid)
    # return round( (x**2 + y**2 + d1**2)**0.5 , prec)
    x = abs(round(x, prec))
    y = abs(round(y, prec))
    return str(x) + str(y)


def generate_hexgrid((x, y), depth=2, major=10):
    hexcenters = [(x, y)]
    hexhashes = [latlon_hash((x, y))]
    lastshellsize = 0
    # newnodes = list(hexcenters)
    for idx in range(2, depth + 1):
        # print "Making shell:",idx
        active = hexcenters[-lastshellsize:]
        #        print "AS:",len(active)
        #        print "LSS:",lastshellsize
        for node in active:
            # print node
            newnodes = get_hex_neighbors(node[:2], major)
            for newnode in newnodes:
                llhash = latlon_hash(newnode)
                # print llhash
                if llhash not in hexhashes:
                    hexcenters.append(newnode)
                    hexhashes.append(llhash)
        lastshellsize += 6

    # print hexhashes
    return hexcenters


def hexagon_generator(edge_length, offset):
    """Generator for coordinates in a hexagon."""
    x, y = offset
    for angle in range(0, 360, 60):
        x += math.cos(math.radians(angle)) * edge_length
        y += math.sin(math.radians(angle)) * edge_length
        yield x, y


def overlay_generator(hexgrid, depth=params.shells, major=params.major):
    # GPolygon.RegularPoly(coord,major,poly,rot,"#000000",strokeOpacity,linethick,"#00ffff",fillalpha)
    s1 = ''
    numhextiles = float(len(hexgrid))
    for idx, hexel in enumerate(hexgrid):
        speckle = random.gauss(1, 0.5)
        rank = int((speckle * idx / numhextiles) * 15)
        invrank = 15 - rank
        blue = hex(rank)[2:]
        red = hex(invrank)[2:]
        tilecolor = red + red + '00' + blue + blue
        ts = "map.addOverlay(GPolygon.RegularPoly(new GLatLng{coord},\
            {major},6,90,\"\#{strokeColor}\",{strokeOpacity},{strokeWeight},\"\#{fillColor}\",{fillalpha}))\
            \n".format(coord=hexel, major=major, strokeColor=tilecolor, strokeOpacity=params.opacity,
                       strokeWeight=params.strokeWeight, fillColor=tilecolor, fillalpha=params.opacity)
        s1 += ts
    return s1


def create_hexel_file(hexgrid):
    # hexgrid = generate_hexgrid((x, y), shells, major)
    fileclerk.csv_dump(params.coordFile, hexgrid)


if __name__ == "__main__":
    hexgrid = generate_hexgrid(params.centroid, params.shells, params.major)
    print len(hexgrid)
    lats = []
    lngs = []
    for pair in hexgrid:
        lats.append(pair[0])
        lngs.append(pair[1])

    gmap = gmplot.GoogleMapPlotter(params.centroid[0], params.centroid[1], 14)

    # gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
    gmap.scatter(lats, lngs, 'k', size=40, marker=True)
    # gmap.heatmap(heat_lats, heat_lngs)

    gmap.draw("mymap.html")




    # create_hexel_file(hexgrid)
    # formattedString = overlay_generator(hexgrid)
    # # hexgrid = generate_hexgrid(rpi,shells,params.major)
    # # formattedString += overlay_generator(hexgrid)
    # # hexgrid = generate_hexgrid(schdy,shells,params.major)
    # # formattedString += overlay_generator(hexgrid)
    # fileclerk.clone_file_and_replace(params.templateFile, params.outputFile, "$OverlayPoints", formattedString)
    # # with open(params.templateFile, 'r') as fin:
    # #     with open(params.outputFile, 'w') as fout:
    # #         fout.write(fin.read().replace("$OverlayPoints", formattedString))
    print "done, created {} tiles".format(len(hexgrid))
