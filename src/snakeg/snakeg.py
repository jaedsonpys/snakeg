from _route_handler import RouteHandler
from _process_request import ProcessRequest
from _socket_handler import SocketHandler

from threading import Thread

# 1. Criar método para receber requisições
#   HTTP por meio do socket.
# 
# 2. Criar método para enviar respostas
#   HTTP.
# 
# 3. Criar método para montar respostas
#   sem a necessidade de um objeto ser
#   retornado.
# 
# 4. Criar método para retornar arquivos.


class SnakeG(RouteHandler):
    def __init__(self) -> None:
        self.thread_limit = 10
        self._atual_thread = 0

        self._process_req = ProcessRequest()
        self._process_req.ROUTES = self._routes

    def start(self, host: str = '127.0.0.1', port: int = '5500') -> None:
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

        sock_handler = SocketHandler()
        sock_handler.create_socket_server(host, port)

        try:
            while True:
                client_s, message = sock_handler.wait_connection()

                # a instrução while abaixo
                # serve para que a requisição
                # recebida ainda seja processada,
                # mas obedecendo o limite de Threads
                # estabelecido no servidor.
                #
                # quando a condição for falsa, a
                # requisição será processada normalmente.

                while self._atual_thread == self._thread_limit:
                    continue

                process_thread = Thread(target=self._process_request,
                                        args=[client_s, message])

                process_thread.start()
        except KeyboardInterrupt:
            raise

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

            client_s.send(response)
            client_s.close()

            self._atual_thread -= 1
        except KeyboardInterrupt:
            raise


if __name__ == '__main__':
    app = SnakeG()

    def teste():
        return 'Hello!'


    app.add_route(teste, '/', methods=['GET'])
    app.start('0.0.0.0', 3000)
