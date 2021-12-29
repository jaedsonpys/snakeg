# SnakeG

O SnakeG é um WSGI feito para suprir necessidadades de perfomance e segurança.

Veja o que o SnakeG possui:

* Multiprocessamento de requisições HTTP
* Manipulação de cookies e headers para respostas e requisições
* Obtenção de variáveis em URLs
* Obtenção de parâmetros de URL
* Respostas com status e headers totalmente personalizáveis
* Proteção contra DDoS

Tudo isso em apenas um pacote, com o SnakeG, você pode criar seu próprio framework ou aplicação web de forma simples e segura.

## Exemplo de código

```python
from snakeg import SnakeG

def index():
    return 'Hello!'
  
 
 if __name__ == '__main__':
    app = SnakeG()
   
    app.add_route('/', index)
    app.start()
```

## License

Esse projeto está licenciado sob GNU General Public License v3.0

```Copyright © 2021-Now Jaedson Silva```

## Links

- [Instagram](https://instagram.com/firlastoficial)
- [Github](https://github.com/jaedsonpys)
- [LinkedIn](https://linkedin/in/jaedsonpys)
- Documentação (em breve)

###

```Made with 💜 and Python by Firlast.```
