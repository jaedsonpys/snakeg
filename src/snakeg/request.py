class Request:
    def __init__(self) -> object:
        self.path = None
        self.method = None
        self.http_version = None
        self.body = None

        self.host = None
        self.port = None
        self.time = None

        self.cookies = {}
        self.headers = {}
        self.params = {}
