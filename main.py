import requests
import json

class AddressLookup(object):
    """docstring for AddressLookup."""
    def __init__(self):
        self.url = "https://www.uber.com/api/address-lookup?lat="


    def get(self, lat, lng):
        req = requests.get(self.url + str(lat) + "&lng=" + str(lng))
        return req.json()


al = AddressLookup()
print al.get(47.575243199999996, -122.12976889999999)



#
# lat = str(47.575243199999996)
# lng = str(-122.12976889999999)
#
# req = UBER_address_lookup + lat + "&lng=" + lng
#
# res = requests.get(req)
# print res.json()
