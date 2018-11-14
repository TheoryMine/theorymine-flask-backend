class BadRequestError(Exception):
    def __init__(self, message ="Bad request made"):
        self.message = message

class NonExistentError(Exception):
    def __init__(self, message ="Data does not exists"):
        self.message = message
