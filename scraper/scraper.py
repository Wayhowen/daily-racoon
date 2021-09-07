import json
import re

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
        data = self._tumblr_client.posts('dailyraccoons.tumblr.com', limit=50, type="photo")
        for post in data["posts"]:
            self._choose_method(post)

    def _choose_method(self, data):
        if data["type"] == "text":
            res = re.search(r'img src=".*?\"', data["body"])
            if res:
                print(res.group(0))
            else:
                print(data)