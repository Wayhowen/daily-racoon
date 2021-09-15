import sys

from pkg.utils import get_settings, load_json_from_file


class Builder:
    def __init__(self, config_file):
        self._settings = get_settings(config_file)

    def build(self):
        if "COMMUNICATOR" in self._settings:
            if self._settings["COMMUNICATOR"] == "discord":
                from internal.communicator.discord import Communicator as DiscordCommunicator
                discord_secrets = load_json_from_file(self._settings["DISCORD_KEYS_LOCATION"])
                communicator = DiscordCommunicator(self._settings["DISCORD_COMMAND_PREFIX"],
                                                   self._settings["DISCORD_CHANNELS_MAP"],
                                                   self._settings["DISCORD_WORK_ON_CHANNELS"],
                                                   discord_secrets["token"])
            else:
                sys.exit(1)

        if "SCRAPER" in self._settings:
            if self._settings["SCRAPER"] == "tumblr":
                from internal.scraper.tumblr import Scraper as TumblrScraper
                tumblr_secrets = load_json_from_file(self._settings["TUMBLR_KEYS_LOCATION"])
                scraper = TumblrScraper(tumblr_secrets["OAuthConsumerKey"],
                                        tumblr_secrets["SecretKey"], tumblr_secrets["OAuthToken"],
                                        tumblr_secrets["OAuthSecret"])

        if "CACHE" in self._settings:
            if self._settings["CACHE"] == "pickledb":
                from internal.cache.pickledb import Cache as PickledbCache
                cache = PickledbCache(self._settings["CACHE_LOCATION"])

        if "CORE" in self._settings:
            if self._settings["CORE"] == "base":
                from internal.core.base import Core as BaseCore
                core = BaseCore(communicator=communicator, scraper=scraper,
                                cache=cache)

        return core


