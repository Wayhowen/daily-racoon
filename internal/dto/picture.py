class Picture:
    def __init__(self, url, timestamp):
        self._url = url
        self._timestamp = timestamp

    @property
    def url(self):
        return self._url

    @property
    def timestamp(self):
        return self._timestamp
