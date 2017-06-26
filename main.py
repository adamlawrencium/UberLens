import requests
import json
import googlemaps
import gmplot
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



class UberWrapper(object):
    """
    Wrapper for address-lookup api endpoint
    """
    def __init__(self):
        self.url_AL = "https://www.uber.com/api/address-lookup?lat="

    def address_lookup(self, lat, lng):
        req = requests.get(self.url_AL + str(lat) + "&lng=" + str(lng))
        return req.json()





if __name__ == '__main__':

    # address locations of Microsoft offices in Puget Sound
    msft_seattle = '320 Westlake Ave N, Seattle, WA 98109'
    msft_bellevue = '205 108th Ave NE, Bellevue, WA 98004'
    msft_redmond = '15010 Northeast 36th Street, Redmond, WA 98052'
    larkspur = '15805 SE 37th St, Bellevue, WA 98006'

    # # # # #

    Uber = UberWrapper()
    APIKEY = readAPI_key()
    gmaps = googlemaps.Client(key=APIKEY)

    geocode_result = gmaps.geocode(msft_bellevue)
    latlng = get_lat_lng_from_geocode(geocode_result)

    reverse_geocode_result = gmaps.reverse_geocode(latlng)
    address = get_address_from_reverse_geocode(reverse_geocode_result)

    nearby_result = gmaps.places_radar(latlng, 5000, keyword='address')
    nearby_result = nearby_result['results']
    lats = []
    lngs = []
    for r in nearby_result:
        pair = r['geometry']['location']['lat'], r['geometry']['location']['lng']
        print 'Gmaps:\t', get_address_from_reverse_geocode(gmaps.reverse_geocode(pair))
        print 'Uber:\t', (Uber.address_lookup(pair[0], pair[1]))['longAddress']
        print
        lats.append(pair[0])
        lngs.append(pair[1])




    gmap = gmplot.GoogleMapPlotter(latlng[0], latlng[1], 14)

    # gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
    gmap.scatter(lats, lngs, 'k', marker=True)
    # gmap.heatmap(heat_lats, heat_lngs)

    gmap.draw("mymap.html")
