from src.snakeg.wsgi import SnakeG

users = [{'name': 'Jaedson', 'age': '14'},
         {'name': 'Maria', 'age': '34'},
         {'name': 'Júlia', 'age': '12'},
         {'name': 'Pedro', 'age': '19'},
         {'name': 'Lucas', 'age': '23'}]


def get_users(request):
    user = request.params.get('user')

    if not user:
        return users

    try:
        response = users[int(user)]
    except IndexError:
        response = {'message': 'Usuário não encontrado.'}

    return response


if __name__ == '__main__':
    from os import urandom

    key = urandom(32)
    app = SnakeG(key)

    app.add_route('/users', get_users, methods=['GET'])
    app.start()
