import gmplot
from colour import Color

# Creates a gradient of colors stepped by each unique price
def createColorGradientList(color1, color2, color_steps):
    color1 = Color(color1)
    colors = list(color1.range_to(Color(color2), color_steps))
    print len(colors), 'colors generated\n'
    return colors


# Create a dictionary keyed by a color, values are a fare with it's coordinates
def createGradientDict(fares, fares_and_coordinates, color_list):
    fare_dic = {}
    for fare in set(fares):
        fare_dic[fare] = []
    for fare in fares_and_coordinates:
        fare_dic[fare[0]].append(fare)
    gradient_dict = {}
    for i in range(len(fare_dic)):
        gradient_dict[color_list[i].hex] = fare_dic[sorted(fare_dic)[i]]

    return gradient_dict


def drawMapWithGradient(fares_and_coordinates, origin_latlng, dest_latlng, zoom):
    fares = []
    for fare in fares_and_coordinates:
        fares.append(fare[0])
    num_distinct_prices = len(set(fares))
    print 'distinct fares:',set(fares)

    fares_and_coordinates.sort(key=lambda x: x[0])

    color_list = createColorGradientList('green', 'red', num_distinct_prices)
    gradient_dict = createGradientDict(fares, fares_and_coordinates, color_list)

    # Initialize map view
    gmap = gmplot.GoogleMapPlotter(dest_latlng[0], dest_latlng[1], zoom)
    # Set pin at origin
    print origin_latlng
    gmap.scatter([origin_latlng[0]], [origin_latlng[1]], 'red', size=100, marker=True)
    for hex_fare in gradient_dict:
        lats = [i[1] for i in gradient_dict[hex_fare]]
        lngs = [i[2] for i in gradient_dict[hex_fare]]
        gmap.scatter(lats, lngs, hex_fare, size=120, marker=False)


    gmap.draw("mymap.html")

    # UNCOMMENT TO SHOW FARE DISTRIBUTION :)
    # import matplotlib.pyplot as plt
    # import numpy as np
    # plt.hist(fares, normed=True, bins=30)
    # plt.ylabel('Probability');
    # plt.show()
