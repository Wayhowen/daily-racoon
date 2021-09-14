from functools import partial
from threading import Thread
from typing import Callable, Any

from discord.ext import commands, tasks
from discord.ext.commands import Command, Context


class Communicator(commands.Bot):
    def __init__(self, command_prefix, listen_to_self, channels_map, bot_token):
        commands.Bot.__init__(self, command_prefix=command_prefix, self_bot=listen_to_self)

        self._running_tasks: dict[str, ] = {}
        self._channels_map = channels_map

        self._bot_background_thread = Thread(
            target=self.run, args=(bot_token,), name='bot-thread', daemon=True)

    # async def on_ready(self):
    #     entry_message = f"{self.user} connected to {self.guilds[0]}"
    #     print(entry_message)
    #     await self.write_to_channel("logs", entry_message)

    async def write_to_channel(self, channel_name: str, message: str):
        await self.wait_until_ready()
        channel = self.get_channel(id=self._channels_map[channel_name])
        await channel.send(message)

    # # TODO: add proper logging
    # async def on_error(self, event, *args, **kwargs):
    #     error = f"During execution of an '{event}', the following happened : {args[0]}\n " \
    #             f"Traceback: {sys.exc_info()}"
    #     print(error)
    #     channel = self.get_channel(id=self._channels_map["logs"])
    #     await channel.send(error)

    def add_looping_task(self, task_name: str, interval_seconds: int,
                         asynchronous_callback: Callable):
        @tasks.loop(seconds=interval_seconds)
        async def looping_task(self):
            await asynchronous_callback()
        looping_task.start(self)
        self._running_tasks[task_name] = looping_task

    def get_looping_tasks(self):
        return self._running_tasks

    def stop_looping_task(self, task_name: str):
        self._running_tasks[task_name].cancel()
        del self._running_tasks[task_name]

    def add_new_command(self, command_name: str, asynchronous_callback: Callable[[Context], Any],
                        usage: str = "", description: str = ""):
        command = Command(name=command_name, passcontext=True, usage=usage, description=description,
                          func=asynchronous_callback)
        self.add_command(command)

    def start_bot(self):
        self._bot_background_thread.start()


if __name__ == '__main__':
    async def test(context):
        print(type(context))
        print("test")

    async def test_loopin(bot):
        await bot.write_to_channel(channel_name="logs", message="loopin feely")

    async def stop_looping(context):
        context.bot.stop_looping_task("loopin task")

    bot = Communicator(command_prefix="!", listen_to_self=False, channels_map=CHANNEL_MAP,
                       bot_token=DISCORD_BOT_TOKEN)
    bot.add_new_command("test", test)
    bot.add_looping_task("loopin task", 10, partial(test_loopin, bot))
    bot.add_new_command("stop_loopin", stop_looping)
    bot.start_bot()
    while True:
        pass
