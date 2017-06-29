import requests
import json
import googlemaps
import gmplot
import time
from hexmath import generate_hexgrid
import params
from datetime import datetime


def readAPI_key():
    with open('APIKEYS.txt', 'r') as myfile:
        data = myfile.read().replace('\n', '')
        return data

#
# def get_lat_lng_from_geocode(blob):
#     pair = blob[0]['geometry']['location']
#     return pair['lat'], pair['lng']
#
# def get_address_from_reverse_geocode(blob):
#     address = blob[0]['formatted_address']
#     return address
#
# def get_address_from_placeID(blob):
#     address = blob['result']['formatted_address']
#     return address
#
# def get_placeID_from_latlng(blob):
#     place_id = blob[0]['place_id']
#     return place_id
#


def drawMap(pairs):
    gmap = gmplot.GoogleMapPlotter(params.centroid[0], params.centroid[1], 14)
    gmap.scatter(pairs['low'][1], pairs['low'][2], 'forestgreen', size=45, marker=False)
    gmap.scatter(pairs['medium'][1], pairs['medium'][2], '#F4A460', size=45, marker=False)
    gmap.scatter(pairs['high'][1], pairs['high'][2], 'red', size=45, marker=False)
    gmap.draw("mymap.html")

def drawMapWithGradient(fares_and_coordinates):
    fares = []
    for fare in fares_and_coordinates:
        fares.append(fare[0])

    num_distinct_prices = len(set(fares))
    print 'distinct fares:',set(fares)
    fares_and_coordinates.sort(key=lambda x: x[0])


    # # # # # # # # # # # # # #
    from colour import Color
    red = Color("red")
    colors = list(red.range_to(Color("green"), num_distinct_prices))
    print num_distinct_prices, 'colors generated\n'


    gmap = gmplot.GoogleMapPlotter(params.centroid[0], params.centroid[1], 14)
    i = 0


     # # # # # #  # # # #
    fare_dic = {}
    for fare in set(fares):
        fare_dic[fare] = []

    for fare in fares_and_coordinates:
        fare_dic[fare[0]].append(fare)

    gradient_dict = {}
    for i in range(len(fare_dic)):
        gradient_dict[colors[i].hex] = fare_dic[sorted(fare_dic)[i]]

    print gradient_dict
    for hex_fare in gradient_dict:
        lats = [i[1] for i in gradient_dict[hex_fare]]
        lngs = [i[2] for i in gradient_dict[hex_fare]]
        gmap.scatter(lats, lngs, hex_fare, size=60, marker=False)

    # # # # # # # # # # #
    #
    # while i < num_distinct_prices:
    #     begin_color_band = fares_and_coordinates[i]
    #     lats = []
    #     lngs = []
    #     j = i
    #     print 'color of interest:', colors[i].hex
    #     print 'starting fare:', fares_and_coordinates[i][0]
    #     print
    #     while j < len(fares_and_coordinates):
    #         print 'checking if next fare (%f) is same as starting fare (%f)' % (fares_and_coordinates[j][0], fares_and_coordinates[i][0])
    #         if fares_and_coordinates[j][0] == begin_color_band[0]:
    #             print 'fares are the same!'
    #             lats.append(fares_and_coordinates[j][1])
    #             lngs.append(fares_and_coordinates[j][2])
    #             print colors[i].hex
    #             print 'lats',lats
    #             print 'lngs',lngs
    #             print
    #         else:
    #             print 'fares are not the same...'
    #             break
    #
    #         j += 1
    #
    #     print '\nAdding points to map:'
    #     print 'color',colors[i].hex
    #     print 'lats',lats
    #     print 'lngs',lngs
    #     print
    #     gmap.scatter(lats, lngs, colors[i].hex, size=45, marker=False)
    #     print 'next color up!'
    #     print
    #
    #         # lats.append(fares_and_coordinates[j][1])
    #         # lngs.append(fares_and_coordinates[j][2])
    #         # if fares_and_coordinates[j][0] != begin_color_band[0]:
    #         #     print colors[i].hex
    #         #     print 'lats',lats
    #         #     print 'lngs',lngs
    #         #     print
    #         #     gmap.scatter(lats, lngs, colors[i].hex, size=45, marker=False)
    #         #     break
    #
    #
    #     i = j+1

    gmap.draw("mymap.html")




class UberWrapper(object):
    """
    Wrapper for address-lookup api endpoint
    """
    def __init__(self):
        self.url_AL = "https://www.uber.com/api/address-lookup?lat="
        self.url_FE = "https://www.uber.com/api/fare-estimate?"

    def address_lookup(self, lat, lng):
        req = requests.get(self.url_AL + str(lat) + "&lng=" + str(lng))
        return req.json()

    def fare_estimator(self, pickupID, destID):
        fares = []
        req = self.url_FE + 'pickupRef=' + pickupID + '&destinationRef=' + destID
        req = requests.get(req)
        return req.json()

    def get_UberX_from_fares(self, blob):

        fares = blob['prices']
        # UberX_fare = ''
        for vehicle in fares:
            if vehicle['vehicleViewDisplayName'] == 'uberX':
                return vehicle['fareString']

        return 'PRICE NOT FOUND'


class GMapsWrapper(object):
    """ Wrapper for Google Maps API """
    def __init__(self):
        APIKEY = readAPI_key()
        self.gmaps = googlemaps.Client(key=APIKEY)

    def geocode(self, origin):
        return self.gmaps.geocode(origin)

    # TODO: CLEAN THIS UP
    def get_lat_lng_from_geocode(self, blob):
        pair = blob[0]['geometry']['location']
        return pair['lat'], pair['lng']

    def get_latlng_from_address(self, origin):
        geocode_result = self.gmaps.geocode(origin)
        return self.get_lat_lng_from_geocode(geocode_result)

    def get_address_from_reverse_geocode(self, blob):
        address = blob[0]['formatted_address']
        return address

    def get_placeID_from_latlng(self, blob):
        place_id = blob[0]['place_id']
        return place_id

    def get_placeID_from_latlng(self, latlng):
        reverse_geocode_result = self.gmaps.reverse_geocode(latlng)
        return reverse_geocode_result[0]['place_id']


if __name__ == '__main__':





    # POIs in Puget Sound
    msft_seattle = '320 Westlake Ave N, Seattle, WA 98109'
    msft_studioG = '3950 148th Ave NE, Redmond, WA 98052'
    building_44 = '15595 NE 36th St, Redmond, WA 98052'
    center_seattle = '832 16th Ave, Seattle, WA 98122'
    molly_moons = '917 E Pine St, Seattle, WA 98122'
    msft_bellevue = '205 108th Ave NE, Bellevue, WA 98004'
    msft_redmond = '15010 Northeast 36th Street, Redmond, WA 98052'
    larkspur = '15805 SE 37th St, Bellevue, WA 98006'

    # # # # # USER INPUTS # # # # #
    origin_of_travel = larkspur
    destination = msft_bellevue
    num_shells = 5
    major = 200
    # # # # # # # # # # # # # # # #


    # Initialize wrappers
    Uber = UberWrapper()
    GMaps = GMapsWrapper()

    # Get origin lat,lng and Google place ID (for Uber API)
    origin_latlng = GMaps.get_latlng_from_address(origin_of_travel)
    origin_placeID = GMaps.get_placeID_from_latlng(origin_latlng)

    print "\nOrigin:\t\t", origin_of_travel
    print "Destination:\t", destination


    # Basic data structure to store different levels of fares
    pairs = {}
    pairs['low'] = [],[],[]
    pairs['medium'] = [],[],[]
    pairs['high'] = [],[],[]

    # Generate hexgrid for target area of destination
    destination_latlng = GMaps.get_latlng_from_address(building_44)
    hexgrid = generate_hexgrid(list(destination_latlng), num_shells, major)

    num_hexs = len(hexgrid)
    print "\n%d points generated\n" % (num_hexs)
    print "Estimating fares to every point in destination area..."

    fares = []
    counter = 1
    for centroid in hexgrid:

        # TODO: MULTITHREAD THIS?
        proximity_dest_placeID = GMaps.get_placeID_from_latlng(centroid)
        fares_response = Uber.fare_estimator(origin_placeID, proximity_dest_placeID)
        if 'estimatesHasError' in fares_response.keys():
            print 'ERROR, TRYING AGAIN'
            fares_response = Uber.fare_estimator(origin_placeID, proximity_dest_placeID)

        fare_string = Uber.get_UberX_from_fares(fares_response)

        fare_range = [ float(x) for x in fare_string[1:].split('-') ]
        fare = sum(fare_range) / len(fare_range)
        fares.append([fare, centroid[0], centroid[1]])

        print "[%d/%d]:\t$%f" % (counter, num_hexs, fare)
        counter += 1
        time.sleep(1)

    print
    for i in range(len(fares)):
        if fares[i] == min(fares):# <=7: #
            # print 'low found', fares[i]
            pairs['low'][0].append(fares[i])
            pairs['low'][1].append(hexgrid[i][0])
            pairs['low'][2].append(hexgrid[i][1])
        elif fares[i] == max(fares):#>= 11:
            # print 'high found', fares[i]
            pairs['high'][0].append(fares[i])
            pairs['high'][1].append(hexgrid[i][0])
            pairs['high'][2].append(hexgrid[i][1])
        else:
            # print 'medium found', fares[i]
            pairs['medium'][0].append(fares[i])
            pairs['medium'][1].append(hexgrid[i][0])
            pairs['medium'][2].append(hexgrid[i][1])


    # drawMap(pairs)
    drawMapWithGradient(fares)




    # # # # # # DRAWING MAP # # # #
    import matplotlib.pyplot as plt
    import numpy as np

    x = fares
    # print x
    plt.hist(x, normed=True, bins=30)
    plt.ylabel('Probability');

    # plt.show()
