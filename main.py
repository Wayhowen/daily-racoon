from configs.default import KEYS_LOCATION
from scraper.scraper import Scraper


def main():
    s = Scraper(KEYS_LOCATION)
    s.scrape()



if __name__ == "__main__":
    main()