class DatabaseLockedException(Exception):
    def __init__(self):
        super().__init__("Database is locked")

class IntegrityError(Exception):
    def __init__(self):
        super().__init__("Foreign keys error")


""" try:
    raise DatabaseLockedException()

except Exception as error:
    print(type(error).__name__ )
    print(type(error))
    print(error) """