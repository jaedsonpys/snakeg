import socket
from _route_handler import RouteHandler

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
    def __init__(self):
        self._tread_limit = 0


if __name__ == '__main__':
    app = SnakeG()
    app.add_route('FUNC', '/login', methods=['GET'])

