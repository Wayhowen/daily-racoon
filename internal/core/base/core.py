class Core:
    # TODO: extend to support multiple communicators and scrapers
    def __init__(self, communicator, scraper):
        self._communicator = communicator
        self._scraper = scraper

    def run(self):
        while True:
            pass
