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



def get_lat_lng_from_geocode(blob):
    pair = blob[0]['geometry']['location']
    return pair['lat'], pair['lng']

def get_address_from_reverse_geocode(blob):
    address = blob[0]['formatted_address']
    return address

def get_address_from_placeID(blob):
    address = blob['result']['formatted_address']
    return address

def get_placeID_from_latlng(blob):
    place_id = blob[0]['place_id']
    return place_id



def drawMap(pairs):
    gmap = gmplot.GoogleMapPlotter(params.centroid[0], params.centroid[1], 14)

    gmap.scatter(pairs['low'][1], pairs['low'][2], 'forestgreen', marker=True)
    gmap.scatter(pairs['medium'][1], pairs['medium'][2], 'yellow', marker=True)
    gmap.scatter(pairs['high'][1], pairs['high'][2], 'red', marker=True)
    # # gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
    # gmap.scatter(lats, lngs, 'k', marker=False)
    #
    # gmap.scatter(lats, lngs, 'azure', size=400, marker=True)
    # # gmap.scatter(lats, lngs, 'k', marker=True)
    # # gmap.heatmap(lats, lngs)

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
        """        prices [
            {
                fare string
                type
            }
        ]
        """
        fares = blob['prices']
        # UberX_fare = ''
        for vehicle in fares:
            if vehicle['vehicleViewDisplayName'] == 'uberX':
                return vehicle['fareString']

        return 'PRICE NOT FOUND'





if __name__ == '__main__':

    # address locations of Microsoft offices in Puget Sound
    msft_seattle = '320 Westlake Ave N, Seattle, WA 98109'
    center_seattle = '832 16th Ave, Seattle, WA 98122'
    molly_moons = '917 E Pine St, Seattle, WA 98122'
    msft_bellevue = '205 108th Ave NE, Bellevue, WA 98004'
    msft_redmond = '15010 Northeast 36th Street, Redmond, WA 98052'
    larkspur = '15805 SE 37th St, Bellevue, WA 98006'

    # # # # #

    Uber = UberWrapper()
    APIKEY = readAPI_key()
    gmaps = googlemaps.Client(key=APIKEY)

    geocode_result = gmaps.geocode(center_seattle)
    latlng = get_lat_lng_from_geocode(geocode_result) #tuple(params.centroid) #

    # Get place ID of origin
    reverse_geocode_result = gmaps.reverse_geocode(latlng)
    address = get_address_from_reverse_geocode(reverse_geocode_result)
    origin_placeID = get_placeID_from_latlng(reverse_geocode_result)


    pairs = {}
    pairs['low'] = [],[],[]
    pairs['medium'] = [],[],[]
    pairs['high'] = [],[],[]

    hexgrid = generate_hexgrid(params.centroid, params.shells, params.major)
    print len(hexgrid)

    fares = []
    for centroid in hexgrid:
        reverse_geocode_result = gmaps.reverse_geocode(centroid)
        dest_placeID = get_placeID_from_latlng(reverse_geocode_result)

        fares_response = Uber.fare_estimator(origin_placeID, dest_placeID)
        print fares_response
        if 'estimatesHasError' in fares_response.keys():
            print 'ERROR, TRYING AGAIN'
            fares_response = Uber.fare_estimator(origin_placeID, dest_placeID)
            print fares_response

        fare_string = Uber.get_UberX_from_fares(fares_response)

        fare_range = [ float(x) for x in fare_string[1:].split('-') ]
        fare = sum(fare_range) / len(fare_range)
        fares.append(fare)

        print fare

        # time.sleep(0.25)

    for i in range(len(fares)):
        if fares[i] < 7: #== min(fares):
            print 'low found', fares[i]
            pairs['low'][0].append(fares[i])
            pairs['low'][1].append(hexgrid[i][0])
            pairs['low'][2].append(hexgrid[i][1])
        elif fares[i] > 12: #== max(fares):
            print 'high found', fares[i]
            pairs['high'][0].append(fares[i])
            pairs['high'][1].append(hexgrid[i][0])
            pairs['high'][2].append(hexgrid[i][1])
        else:
            print 'medium found', fares[i]
            pairs['medium'][0].append(fares[i])
            pairs['medium'][1].append(hexgrid[i][0])
            pairs['medium'][2].append(hexgrid[i][1])

    # lats = []
    # lngs = []
    # for pair in hexgrid:
    #     lats.append(pair[0])
    #     lngs.append(pair[1])

    drawMap(pairs)
