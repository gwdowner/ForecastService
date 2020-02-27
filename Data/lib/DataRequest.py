import json
import requests

class DataRequest():
    localFilePath = './cachedData'

    # Makes GET request to given url and returns JSON data
    @staticmethod
    def getData(url):
        result = requests.get(url)
        return result.json()