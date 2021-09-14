import json
import time

from internal.configs.default import TUMBLR_KEYS_LOCATION, DISCORD_TOKEN_LOCATION, CHANNELS_MAP
from internal.discord.bot import DiscordBot
from internal.scraper.scraper import Scraper


class TempMain:
    def __init__(self):
        self._raccoon_picture_urls = []

    async def send_szopik(self, context):
        await context.bot.write_to_channel(channel_name="szopiki",
                                           message=self._raccoon_picture_urls.pop(0))

    def main(self):
        s = Scraper(TUMBLR_KEYS_LOCATION)
        self._raccoon_picture_urls = s.get_raccoon_picture_urls()
        with open(DISCORD_TOKEN_LOCATION, "r") as file:
            discord_token = json.load(file)["token"]
        bot = DiscordBot(command_prefix="!", listen_to_self=False, channels_map=CHANNELS_MAP,
                         bot_token=discord_token)
        bot.add_new_command("szopiki", self.send_szopik)
        bot.start_bot()
        while True:
            if self._raccoon_picture_urls:
                time.sleep(5)
            else:
                self._raccoon_picture_urls = s.get_raccoon_picture_urls()



if __name__ == "__main__":
    m = TempMain()
    m.main()