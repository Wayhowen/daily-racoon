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

    def get_raccoon_picture_urls(self):
        picture_urls = []
        data = self._tumblr_client.posts('dailyraccoons.tumblr.com', limit=50, type="photo")
        for post in data["posts"]:
            picture_urls.append(self._extract_racoon_picture_url(post))
        return picture_urls


    def _extract_racoon_picture_url(self, data):
        if data["type"] == "text":
            res = re.search(r'(http)?s?:?(//[^"\']*\.(?:png|jpg|jpeg|gif|png|svg))', data["body"])
            if res:
                pic_link = res.group(0)
        elif data["type"] == "photo":
            pic_link = data["photos"][0]["original_size"]["url"]
        else:
            pic_link = None
        return pic_link
