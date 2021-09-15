import asyncio
import signal
from typing import Optional

import janus


class Core:
    # TODO: extend to support multiple communicators and scrapers
    def __init__(self, communicator, scraper, cache):
        self._communicator = communicator
        self._scraper = scraper
        self._cache = cache

        self._input = communicator.get_input_queue()
        self._output = communicator.get_output_queue()

        self._local_queue: Optional[janus.Queue] = None

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    # TODO: divide work into input and output streams
    async def run(self):
        self._local_queue = janus.Queue()
        while True:
            asyncio.run_coroutine_threadsafe(self.get_input(), self._communicator.loop)
            task_data = await self._local_queue.async_q.get()
            await self._process_input(task_data)

    async def get_input(self):
        self._local_queue.sync_q.put(await self._input.get())

    async def _process_input(self, task_data):
        channel, task, *_ = task_data
        if task == "szopiki":
            response = self._process_szopiki()
            await self._output.put((channel, response))
        else:
            await self._output.put((channel, "Unrecognized command"))
        self._task_data = None

    def _process_szopiki(self):
        raccoon_picture = self._cache.get_racoon_picture()
        if raccoon_picture:
            return raccoon_picture.url
        self._cache.add_raccoon_pictures(self._scraper.download_raccoon_pictures(
            before=self._cache.last_picture_timestamp))
        return self._cache.get_racoon_picture().url

    def exit_gracefully(self, *args, **kwargs):
        self._cache.save_database()
