class ShallowInputCancel(Exception):
    def __init__(self, message: str):
        self.message = message


class DeepInputCancel(Exception):
    def __init__(self, message: str):
        self.message = message