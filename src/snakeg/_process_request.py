from _format_http import Formatter


class ProcessRequest:
    ROUTES = {}
    QUEUE_PROCESS = []

    def process_request(self, request: str) -> None:
        """Processa a requisição HTTP
        e retorna uma resposta.

        Args:
            request (str): [description]
        """

        request_http = Formatter(request)
        route_info = self.ROUTES.get(request_http.path)
        
        if not route_info:
            self.build_http_message(404, body='404. Not found')
            
    def build_http_message(self, status: int, headers: list=[], body: str = '') -> str:
        """Constrói uma mensagem HTTP
        com headers, status e body.

        * O argumento body será mudado
        para receber uma classe que
        possui as respostas para cada
        status HTTP, possibilitando
        a personalização das páginas.

        Args:
            status (int): Status da resposta
            headers (list, optional): Headers da resposta.
            body (str, optional): Corpo da resposta.

        Returns:
            str: Retorna a mensagem HTTP estruturada.
        """

        pre_message = [f'HTTP/1.1 {status}']

        # definindo headers na resposta
        pre_message.append(f'Server: SnakeG')
    
        if headers:
            for header in headers:
                name = header[0]
                value = header[1]

                pre_message.append(f'{name}: {value}')

        # definindo o body
        if body:
            pre_message.append('')
            pre_message.append(body)

        http_response_message = '\n'.join(pre_message)
        return http_response_message


if __name__ == '__main__':
    test = ProcessRequest()

    headers = [('Content-Type', 'text/plain'),
               ('Set-Cookie', 'nft=8374784; auth=dy3hrn'),
               ('Auth', '83iud')]

    response = test.build_http_message(200, headers=headers,
                                       body='404. Not found.')

    test.build_http_message()

    print(response)
