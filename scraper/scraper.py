import json

import pytumblr as pytumblr


class Scraper:
    def __init__(self, consumer_key_location):
        with open(consumer_key_location, "r") as file:
            api_keys = json.load(file)
        self._tumblr_client = pytumblr.TumblrRestClient(
            api_keys["OAuthConsumerKey"],
            api_keys["SecretKey"],
            api_keys["OAuthToken"],
            api_keys["OAuthSecret"]
        )

    def scrape(self):
        print(self._tumblr_client.info())
