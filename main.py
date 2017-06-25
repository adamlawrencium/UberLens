import requests
import json

class UberWrapper(object):
    """
    Wrapper for address-lookup api endpoint
    """
    def __init__(self):
        self.url_AL = "https://www.uber.com/api/address-lookup?lat="

    def address_lookup(self, lat, lng):
        req = requests.get(self.url_AL + str(lat) + "&lng=" + str(lng))
        return req.json()




Uber = UberWrapper()
print Uber.address_lookup(47.575243199999996, -122.12976889999999)



#
# lat = str(47.575243199999996)
# lng = str(-122.12976889999999)
#
# req = UBER_address_lookup + lat + "&lng=" + lng
#
# res = requests.get(req)
# print res.json()
