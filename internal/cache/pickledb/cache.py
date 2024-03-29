from typing import Optional

import pickledb

from internal.dto.picture import Picture


# TODO: add some logic not to run out of pictures
# TODO: make it independent of raccoon thing
class Cache:
    def __init__(self, database_location: str):
        self._db = pickledb.load(database_location, False)

        self._last_picture_timestamp = self._db.get("last_timestamp") or None

        self._racoon_pictures = []

    @property
    def last_picture_timestamp(self) -> int:
        return self._last_picture_timestamp

    def save_database(self) -> None:
        self._db.set("last_timestamp", self._last_picture_timestamp)
        self._db.dump()

    def add_raccoon_pictures(self, racoon_pictures: list[Picture]) -> None:
        self._racoon_pictures.extend(racoon_pictures)

    def get_racoon_picture(self) -> Optional[Picture]:
        if not self._racoon_pictures:
            return None
        picture = self._racoon_pictures.pop(0)
        self._last_picture_timestamp = picture.timestamp
        return picture
