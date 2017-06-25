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





if __name__ == '__main__':
    msft_seattle = '320 Westlake Ave N, Seattle, WA 98109'
    msft_bellevue = '205 108th Ave NE, Bellevue, WA 98004'
    msft_redmond = '15010 Northeast 36th Street, Redmond, WA 98052'

    Uber = UberWrapper()
    print Uber.address_lookup(47.575243199999996, -122.12976889999999)

    
