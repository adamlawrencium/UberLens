import googlemaps
import os

class GMapsWrapper(object):
    """ Wrapper for Google Maps API """
    def __init__(self):
        APIKEY = self.readAPI_key()
        self.gmaps = googlemaps.Client(key=APIKEY)

    def geocode(self, origin):
        return self.gmaps.geocode(origin)

    def readAPI_key(self):
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            print f

        with open('APIKEYS.txt', 'r') as myfile:
            data = myfile.read().replace('\n', '')
            return data

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

    def get_placeID_from_latlng(self, latlng):
        reverse_geocode_result = self.gmaps.reverse_geocode(latlng)
        # print reverse_geocode_result
        return reverse_geocode_result[0]['place_id']

    def isWater(self, latlng):
        response = self.gmaps.elevation(latlng)
        if response[0]['elevation'] < 8:
            print "Uh oh, there's water here:", latlng
            return True
        else:
            return False
