import sys

from pkg.utils import get_settings, load_json_from_file, load_json_from_env, decode_base64, \
    load_from_env


class Builder:
    def __init__(self, config_file):
        self._settings: dict = get_settings(config_file)

    def build(self) -> None:
        if "COMMUNICATOR" in self._settings:
            if self._settings["COMMUNICATOR"] == "discord":
                from internal.communicator.discord import Communicator as DiscordCommunicator
                try:
                    discord_secrets = load_json_from_file(self._settings["DISCORD_KEYS_LOCATION"])
                except FileNotFoundError:
                    encoded_secrets = load_from_env(self._settings["DISCORD_ENV"])
                    discord_secrets = decode_base64(load_from_env(encoded_secrets))
                communicator = DiscordCommunicator(self._settings["DISCORD_COMMAND_PREFIX"],
                                                   self._settings["DISCORD_CHANNELS_MAP"],
                                                   self._settings["DISCORD_WORK_ON_CHANNELS"],
                                                   discord_secrets["token"])
            else:
                sys.exit(1)

        if "SCRAPER" in self._settings:
            if self._settings["SCRAPER"] == "tumblr":
                from internal.scraper.tumblr import Scraper as TumblrScraper
                try:
                    tumblr_secrets = load_json_from_file(self._settings["TUMBLR_KEYS_LOCATION"])
                except FileNotFoundError:
                    encoded_secrets = load_from_env(self._settings["TUMBLR_ENV"])
                    tumblr_secrets = decode_base64(load_from_env(encoded_secrets))
                scraper = TumblrScraper(tumblr_secrets["OAuthConsumerKey"],
                                        tumblr_secrets["SecretKey"], tumblr_secrets["OAuthToken"],
                                        tumblr_secrets["OAuthSecret"])

        if "CACHE" in self._settings:
            if self._settings["CACHE"] == "pickledb":
                from internal.cache.pickledb import Cache as PickledbCache
                cache = PickledbCache(self._settings["CACHE_LOCATION"])
            elif self._settings["CACHE"] == "redis":
                from internal.cache.redis import Cache as RedisCache
                cache = RedisCache(self._settings["REDIS_URL"])

        if "CORE" in self._settings:
            if self._settings["CORE"] == "base":
                from internal.core.base import Core as BaseCore
                core = BaseCore(communicator=communicator, scraper=scraper,
                                cache=cache)

        return core


