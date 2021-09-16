class Picture:
    def __init__(self, url: str, timestamp: int):
        self._url = url
        self._timestamp = timestamp

    @property
    def url(self) -> str:
        return self._url

    @property
    def timestamp(self) -> int:
        return self._timestamp
