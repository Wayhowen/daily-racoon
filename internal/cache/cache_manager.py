import pickledb


class CacheManager:
    def __init__(self, database_name):
        self._db = pickledb.load(database_name, False)

    def save_database(self):
        self._db.dump()

