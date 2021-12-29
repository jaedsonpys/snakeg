class Base(BaseException):
    pass


class InvalidHTTPMessage(Base):
    def __init__(self):
        super().__init__('Mensagem HTTP inválida.')
