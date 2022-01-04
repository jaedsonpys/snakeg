from _route_handler import RouteHandler
from _process_request import ProcessRequest
from _socket_handler import SocketHandler

from threading import Thread
from base64 import urlsafe_b64encode
from _environ import _set_key
import os

# 4. Criar método para retornar arquivos.
# 6. Obter parâmetros da URL


class SnakeG(RouteHandler):
    def __init__(self, key) -> None:
        self.thread_limit = 10
        self._atual_thread = 0

        # a chave secreta é utilizada
        # para criptografar cookies e sessões
        self.key = key
        _set_key(key)

        self._process_req = ProcessRequest()
        self._process_req.ROUTES = self._routes

        self._sock_handler = SocketHandler

    def start(self, host: str = '127.0.0.1', port: int = 5500) -> None:
        """Inicia a aplicação no host e
        porta especificado.

        Todas as requisições são processadas
        utilizando threads, quando uma nova
        solicitaçao chega ao servidor, uma nova
        thread é criada e o servidor
        continua a receber solicitações.

        Quando o limite (o padrão é 10) for atingido,
        o servidor é obrigado a esperar que as
        outras solicitações que estão em processamento
        terminem, e após isso, a solicitação é processada.

        Se o servidor receber uma solicitação
        enquanto o limite de threads ainda
        estiver excedido, a solicitação ficará
        esperando até que uma "vaga" seja liberada.

        Você pode alterar o limite de threads
        a serem criadas em SnakeG.thread_limit.

        :param host: Endereço IP a ser usado.
        :param port: Porta a ser usada.
        :return: None
        """

        self._sock_handler = SocketHandler(host, port)

        try:
            while True:
                client_s, message = self._sock_handler.wait_connection()

                # a instrução while abaixo
                # serve para que a requisição
                # recebida ainda seja processada,
                # mas obedecendo o limite de Threads
                # estabelecido no servidor.
                #
                # quando a condição for falsa, a
                # requisição será processada normalmente.

                while self._atual_thread == self.thread_limit:
                    continue

                process_thread = Thread(target=self._process_request,
                                        args=[client_s, message])

                process_thread.start()
        except KeyboardInterrupt:
            self._sock_handler.close_server()
            exit()

    def _process_request(self, client_s, message) -> None:
        # todas as requisições que chegam são
        # processadas pela classe ProcessRequest.
        #
        # este método (_process_request) serve
        # apenas para obter a resposta de
        # ProcessRequest.process_request e envia-la
        # ao cliente, fechando a conexão posteriormente.

        self._atual_thread += 1

        try:
            response = self._process_req.process_request(message)
            self._sock_handler.send_response(client_s, response)
            self._atual_thread -= 1
        except KeyboardInterrupt:
            self._sock_handler.close_server()
            exit()


if __name__ == '__main__':
    app = SnakeG()

    def get_user():
        return {'name': 'Jaedson', 'age': 14}

    def index():
        return 'Index Route'

    def about():
        return 'Test method 404', 404

    def show_info_request(request):
        info = [request.cookies,
                request.headers,
                {'method': request.method, 'path': request.path}]

        return info, 200


    app.add_route(get_user, '/user', methods=['GET'])
    app.add_route(index, '/', methods=['GET'])
    app.add_route(about, '/about', methods=['GET'])
    app.add_route(show_info_request, '/request', methods=['GET'])

    app.start('127.0.0.1', 5500)
