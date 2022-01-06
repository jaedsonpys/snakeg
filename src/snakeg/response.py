from process_request import build_http_message


class Response:
    def __init__(
        self,
        body,
        status: int = 200,
        headers: dict = None,
        cookies: dict = None
    ) -> object:
        """Cria uma resposta ao cliente.

        __call__ retornará a mensagem HTTP
        em bytes e é utilizada no envio
        da resposta pelo socket ao cliente.

        :param body: Corpo da resposta
        :param status: Status
        :param headers: Headers da resposta
        :param cookies: Cookies da resposta
        """

        self.status = status
        self._response = build_http_message(body, status, headers, cookies)

    def __call__(self):
        return self._response


if __name__ == '__main__':
    cookies = {'auth': 'jaedson'}
    test = Response('Hello World!', cookies=cookies)
    print(test())
