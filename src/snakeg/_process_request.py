from _format_http import Formatter
from exceptions import InvalidHTTPMessage


class ProcessRequest:
    ROUTES = {}
    QUEUE_PROCESS = []

    def process_request(self, request: str) -> [str, bool]:
        """Processa a requisição HTTP
        e retorna uma resposta.

        Caso a mensagem HTTP seja inválida,
        a exceção InvalidHTTPMessage é lançada.

        Args:
            request (str): A requisição HTTP.
        """

        try:
            request_http = Formatter(request)
        except InvalidHTTPMessage:
            return self.build_http_message('400. Bad Request', 400)

        route_info = self.ROUTES.get(request_http.path)

        # validações padrões para o 
        # gerenciamento de rotas.
        
        if not route_info:
            return self.build_http_message('404. Method Not Allowed', 404)

        if request_http.method not in route_info.get('methods'):
            return self.build_http_message('405. Method Not Allowed', 405)

        # call_function é onde ficará
        # a resposta da função para determinada
        # rota e método.
        # 
        # por exemplo, a função de uma rota /login
        # que aceita apenas o método POST
        # será chamada pelo SnakeG quando
        # essa rota ("/login") for requisitada
        # por um cliente. 
        # 
        # se a rota não existir, o SnakeG retorna
        # um erro 404 padrão ou personalizada pelo
        # usuário do SnakeG (como uma página HTML estilizada).#

        call_function = route_info.get('call')

        # o código abaixo é apenas para testes:
        headers = [('Content-Type', 'text/plain')]
        body = call_function()

        return self.build_http_message(body, headers=headers)

    @staticmethod
    def build_http_message(
        body: str,
        status: int = 200,
        headers: list = None
    ) -> bytes:
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

        pre_message = list()
        pre_message.append(f'HTTP/1.1 {status}')

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
        return http_response_message.encode()


if __name__ == '__main__':
    test = ProcessRequest()

    header = [('Content-Type', 'text/plain'),
               ('Set-Cookie', 'nft=8374784; auth=dy3hrn'),
               ('Auth', '83iud')]

    response = test.build_http_message(200, headers=header,
                                       body='404. Not found.')
