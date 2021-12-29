class Request:
    def __init__(self) -> object:
        self.path = None
        self.method = None
        self.http_version = None
        self.body = None

        self.cookies = {}
        self.headers = {}
