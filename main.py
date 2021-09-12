from internal.configs.default import KEYS_LOCATION
from internal.scraper.scraper import Scraper
import pickledb


def main():
    s = Scraper(KEYS_LOCATION)
    # picture_urls = s.get_raccoon_picture_urls()
    db = pickledb.load('example.db', False)
    # for picture in picture_urls:
    #     db.set(picture, picture)
    print(db.getall())
    with open("cache.pkl", "w") as file:
        file.write(db.dump())


if __name__ == "__main__":
    main()