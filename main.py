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



def drawMap(lats, lngs):
    gmap = gmplot.GoogleMapPlotter(params.centroid[0], params.centroid[1], 14)

    # gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
    gmap.scatter(lats, lngs, 'k', marker=True)
    # gmap.heatmap(heat_lats, heat_lngs)

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
    molly_moons = '917 E Pine St, Seattle, WA 98122'
    msft_bellevue = '205 108th Ave NE, Bellevue, WA 98004'
    msft_redmond = '15010 Northeast 36th Street, Redmond, WA 98052'
    larkspur = '15805 SE 37th St, Bellevue, WA 98006'

    # # # # #

    Uber = UberWrapper()
    APIKEY = readAPI_key()
    gmaps = googlemaps.Client(key=APIKEY)

    geocode_result = gmaps.geocode(msft_bellevue)
    latlng = tuple(params.centroid) # get_lat_lng_from_geocode(geocode_result)

    # Get place ID of origin
    reverse_geocode_result = gmaps.reverse_geocode(latlng)
    address = get_address_from_reverse_geocode(reverse_geocode_result)
    origin_placeID = get_placeID_from_latlng(reverse_geocode_result)


    # nearby_result = gmaps.places_radar(latlng, 1000, keyword='food')
    # nearby_result = nearby_result['results']
    # lats = []
    # lngs = []
    # for r in nearby_result:
    #     pair = r['geometry']['location']['lat'], r['geometry']['location']['lng']
    #     print 'Gmaps:\t', get_address_from_reverse_geocode(gmaps.reverse_geocode(pair))
    #     print 'Uber:\t', (Uber.address_lookup(pair[0], pair[1]))['longAddress']
    #     print
    #     lats.append(pair[0])
    #     lngs.append(pair[1])


    hexgrid = generate_hexgrid(params.centroid, params.shells, params.major)
    print len(hexgrid)
    for centroid in hexgrid[::18]:

        reverse_geocode_result = gmaps.reverse_geocode(centroid)
        dest_placeID = get_placeID_from_latlng(reverse_geocode_result)

        fares_response = Uber.fare_estimator(origin_placeID, dest_placeID)
        print Uber.get_UberX_from_fares(fares_response)

        time.sleep(0.5)


    lats = []
    lngs = []
    for pair in hexgrid:
        lats.append(pair[0])
        lngs.append(pair[1])

    drawMap(lats, lngs)
