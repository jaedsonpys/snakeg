class RouteHandler:
    _routes = {}

    @classmethod
    def add_route(cls, func, path: str, methods: list) -> None:
        """Adiciona uma nova rota a
        aplicação::

            def func(request):
                return 'Hello'

            RouteHandler.add_route(func, '/',
                                    methods=['POST', GET])

        :param func: Função a ser disparada.
        :param path: Rota.
        :param methods: Métodos aceitos pela rota
        :return: None.
        """

        new_route = {'methods': methods, 'call': func}
        cls._routes[path] = new_route


if __name__ == '__main__':
    teste = RouteHandler()

    def teste_route(request):
        print(request)


    teste.add_route(teste_route, '/login', methods=['GET'])

