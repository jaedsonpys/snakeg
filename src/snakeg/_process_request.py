from _format_http import Formatter
from exceptions import InvalidHTTPMessage
import json


def build_http_message(
        body: str,
        status: int = 200,
        headers: dict = None,
        cookies: dict = None
) -> bytes:
    """Constrói uma mensagem HTTP
    com headers, status e body.

    * O argumento body será mudado
    para receber uma classe que
    possui as respostas para cada
    status HTTP, possibilitando
    a personalização das páginas.

    :param cookies: Cookies
    :param body: Body da resposta.
    :param status: Código de status HTTP
    :param headers: Headers da resposta
    :return: None
    """

    pre_message = list()
    pre_message.append(f'HTTP/1.1 {status}')
    pre_message.append(f'Server: SnakeG')

    if cookies:
        cookies_list = []
        for name, value in cookies.items():
            cookies_list.append(f'{name}={value}')

        headers['Set-Cookie'] = '; '.join(cookies_list)
        del cookies_list
        del cookies

    if headers:
        for name, value in headers.items():
            pre_message.append(f'{name}: {value}')
    else:
        pre_message.append('Content-Type: text/html')

    # definindo o body
    if body:
        pre_message.append('')
        pre_message.append(body)

    http_response_message = '\n'.join(pre_message)
    return http_response_message.encode()


class ProcessRequest:
    ROUTES = {}

    def process_request(self, request: str) -> bytes:
        """Processa a requisição HTTP
        e retorna uma resposta.

        Caso a mensagem HTTP seja inválida,
        a exceção InvalidHTTPMessage é lançada.

        Args:
            request (str): A requisição HTTP.
        """

        try:
            request_http = Formatter(request).request_obj
        except InvalidHTTPMessage:
            return build_http_message('400. Bad Request', 400)

        route_info = self.ROUTES.get(request_http.path)

        # validações padrões para o 
        # gerenciamento de rotas.
        
        if not route_info:
            return build_http_message('404. Not found', 404)

        if request_http.method not in route_info.get('methods'):
            return build_http_message('405. Method Not Allowed', 405)

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
        # usuário do SnakeG (como uma página HTML estilizada).

        # a subclasse Request de Formatter é
        # passada como argumento para a função
        # designada pela rota para que o usuário
        # possa manipular os dados vindos do cliente.

        call_function = route_info.get('call')

        try:
            response = call_function(request_http)
        except TypeError:
            response = call_function()

        # verificando tipo do retorno de call_function

        if isinstance(response, tuple):
            # se a resposta da função for uma
            # tupla, é esperado que o primeiro
            # elemento seja a resposta, e o segundo
            # o status.

            # verificar body para
            # realizar a conversão
            # para JSON.

            body, status = response
            response_header = {'Content-Type': 'text/html'}

            if isinstance(body, dict) or isinstance(body, list):
                response_header['Content-Type'] = 'application/json'
                body = json.dumps(body)

            return build_http_message(body, status=status, headers=response_header)

        elif isinstance(response, dict):
            # se a resposta da função for apenas
            # um dicionário, sabemos que não
            # há um status especificado,
            # então apenas convertemos o dicionário
            # para string e alteramos o content-type.

            body = json.dumps(response)
            response_header = {'Content-Type': 'application/json'}

            return build_http_message(body, headers=response_header)

        elif isinstance(response, str):
            # se a resposta da função for apenas
            # uma string, sabemos que não
            # há um status especificado,
            # então retornamos a string e o código
            # de status padrão.

            body = response
            response_header = {'Content-Type': 'text/html'}

            return build_http_message(body, headers=response_header)


if __name__ == '__main__':
    header = {'Content-Type': 'text/html',
              'Set-Cookie': 'nd=3434'}

    response = build_http_message('405. Method Not Allowed', 405, headers=header)
    print(response.decode())
