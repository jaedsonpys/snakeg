import socket


class SocketHandler:
    def __init__(self) -> None:
        """SocketHandler permite criar novos
        sockets e receber conexões de clientes.
        """

        self.server_s = None

    def create_socket_server(
        self, host: str, port: int
    ) -> None:
        """Cria um novo socket
        no host e porta especificados.

        :param host:
        :param port:
        :return:
        """

        address = (host, port)

        self.server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_s.bind(address)

        self.server_s.listen(5024)

    def wait_connection(self) -> [socket.SocketType, str]:
        """Aguarda novas conexões ao
        socket.

        :return: Retorna o socket do cliente e a mensagem recebida.
        """

        client_s, addr = self.server_s.accept()
        http_message = client_s.recv(5024).decode()

        return client_s, http_message

    def close_server(self) -> None:
        """Fecha o socket.

        :return:
        """

        self.server_s.shutdown(0)


if __name__ == '__main__':
    teste = SocketHandler()
    teste.create_socket_server('127.0.0.1', 3040)

    cl_s, http_msg = teste.wait_connection()
    cl_s.close()
    teste.close_server()

    print(http_msg)
