from src.snakeg.wsgi import SnakeG
from src.snakeg.response import Response

from os import urandom

SECRET_KEY = urandom(32)

animals = {'cats': {'Melk': {'age': '2', 'status': 'has owner'},
                    'Janis': {'age': '5', 'status': 'needs home'},
                    'Amy': {'age': '1', 'status': 'needs home'},
                    'Frida': {'age': '3', 'status': 'has owner'}},
           'dogs': {'Yoda': {'age': '7', 'status': 'needs home'},
                    'Chris': {'age': '4', 'status': 'needs home'},
                    'Beethoven': {'age': '9', 'status': 'has owner'},
                    'Luna': {'age': '2', 'status': 'has owner'}}}


def index(req):
    body = {'message': 'Hey user! Welcome to the example of using WSGI SnakeG.'
                       'Use the /animals paths to get all the animals,'
                       '/animals/dogs to get all the dogs and /animals/cats to'
                       'get all the cats. You can also specify the "name"'
                       'parameter to get only one animal.'}

    headers = {'Content-Type': 'application/json'}
    return Response(body, headers=headers)


def get_animals(request):
    name = request.params.get('name')

    if not name:
        response = animals
    else:
        dog_with_name = animals['dogs'].get(name)
        cat_with_name = animals['cats'].get(name)

        response = {}

        if dog_with_name:
            response['dog'] = dog_with_name

        if cat_with_name:
            response['cat'] = cat_with_name

        if not response:
            response = {'message': 'No animals found with this name.'}

    return response


def get_cats(request):
    name = request.params.get('name')

    if not name:
        return animals['cats']

    name = name.capitalize()
    animal_info = animals['cats'].get(name)

    if not animal_info:
        response = {'message': 'Sorry, this animal doesn\'t exist here.'}
    else:
        response = animal_info

    return response


def get_dogs(request):
    name = request.params.get('name')

    if not name:
        return animals['dogs']

    name = name.capitalize()
    animal_info = animals['dogs'].get(name)

    if not animal_info:
        response = {'message': 'Sorry, this animal doesn\'t exist here.'}
    else:
        response = animal_info

    return response


if __name__ == '__main__':
    app = SnakeG(SECRET_KEY)

    app.add_route('/', index, methods=['GET'])
    app.add_route('/animals', get_animals, methods=['GET'])

    app.add_route('/animals/dogs', get_dogs, methods=['GET'])
    app.add_route('/animals/cats', get_cats, methods=['GET'])

    app.start()
