import re
from typing import Optional

import pytumblr as pytumblr

from internal.dto.picture import Picture


class Scraper:
    def __init__(self, oauth_consumer_key: str, secret_key: str, oauth_token: str,
                 oauth_secret: str):

        self._oauth_consumer_key = oauth_consumer_key
        self._secret_key = secret_key
        self._oauth_token = oauth_token
        self._oauth_secret = oauth_secret
        self._tumblr_client = pytumblr.TumblrRestClient(
            oauth_consumer_key,
            secret_key,
            oauth_token,
            oauth_secret
        )

    def download_raccoon_pictures(self, before: Optional[int] = None) -> list[Picture]:
        pictures = []
        data = self._tumblr_client.posts('dailyraccoons.tumblr.com', limit=50, type="photo",
                                         before=before)
        for post in data["posts"]:
            raccoon_picture = self._extract_racoon_picture(post)
            if raccoon_picture:
                pictures.append(self._extract_racoon_picture(post))
        return pictures

    # TODO: rewrite this bit
    def _extract_racoon_picture(self, response: dict) -> Picture:
        if response["type"] == "text":
            res = re.search(r'(http)?s?:?(//[^"\']*\.(?:png|jpg|jpeg|gif|png|svg))',
                            response["body"])
            if res:
                picture_url = res.group(0)
                timestamp = response["timestamp"]
                picture = Picture(url=picture_url, timestamp=timestamp)
        elif response["type"] == "photo":
            picture_url = response["photos"][0]["original_size"]["url"]
            timestamp = response["timestamp"]
            picture = Picture(url=picture_url, timestamp=timestamp)
        else:
            picture = None
        return picture
