import asyncio


class Core:
    # TODO: extend to support multiple communicators and scrapers
    def __init__(self, communicator, scraper, cache):
        self._communicator = communicator
        self._scraper = scraper
        self._cache = cache

        self._input = communicator.get_input_queue()
        self._output = communicator.get_output_queue()

    async def run(self):
        while True:
            print("waiting on input")
            if self._input:
                task_data = self._input.get()
                print("got input")
                self._process_input(task_data)
                print("processed")
            else:
                print("sleeping")
                await asyncio.sleep(1)

    def _process_input(self, task_data):
        channel, task, *_ = task_data
        if task == "szopiki":
            response = self._process_szopiki()
            self._output.put((channel, response))
        else:
            self._output.put((channel, "Unrecognized command"))

    def _process_szopiki(self):
        raccoon_picture = self._cache.get_racoon_picture()
        if raccoon_picture:
            return raccoon_picture.url
        self._cache.add_raccoon_pictures(self._scraper.download_raccoon_pictures())
        return self._cache.get_racoon_picture().url
