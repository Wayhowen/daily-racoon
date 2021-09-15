import asyncio
import sys
from queue import Queue
from threading import Thread

from discord import Message
from discord.ext import commands


class Communicator(commands.Bot):
    def __init__(self, command_prefix, channels_map, work_on_channels, bot_token):
        commands.Bot.__init__(self, command_prefix=command_prefix)
        self._channels_map = channels_map
        self._work_on_channels = work_on_channels

        self._input_queue = asyncio.Queue()
        self._output_queue = asyncio.Queue()

        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.start(bot_token))
        self._bot_thread = Thread(
            target=self.loop.run_forever, name='bot-thread', daemon=True).start()

    def get_input_queue(self) -> Queue:
        return self._input_queue

    def get_output_queue(self) -> Queue:
        return self._output_queue

    async def on_ready(self):
        message = ("start", f"{self.user} connected to {self.guilds[0]}")
        print(message)
        while True:
            message_info = await self._output_queue.get()
            channel, message = message_info
            await self.write_to_channel(channel, message)

    async def on_message(self, message: Message):
        if message.channel.name in self._work_on_channels and message.author != self.user\
                and message.content.startswith("!"):
            message_content = message.content[1:]
            message_data = (message.channel.name, *message_content.split())
            await self._input_queue.put(message_data)

    async def write_to_channel(self, channel_name: str, message: str):
        await self.wait_until_ready()
        channel = self.get_channel(id=self._channels_map[channel_name])
        await channel.send(message)

    # TODO: add proper logging
    async def on_error(self, event, *args, **kwargs):
        error_message = f"During execution of an '{event}', the following happened : {args[0]}\n " \
                f"Traceback: {sys.exc_info()}"
        message = ("error", error_message)
        print(message)
