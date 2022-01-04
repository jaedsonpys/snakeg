from exceptions import InvalidHTTPMessage
from _request import Request

from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidKey, UnsupportedAlgorithm


class Formatter:
    def __init__(self, http_message: str, key: str):
        self._lines = http_message.split('\n')
        self.request_obj = Request()

        self.fr = Fernet(key)

        self.__format_http()
        self.__format_headers()
        self.__format_cookies()
        self.__format_params()

    def __format_http(self):
        try:
            method, path, http_version = self._lines[0].split(' ')
        except ValueError:
            raise InvalidHTTPMessage

        self.request_obj.method = method
        self.request_obj.path = path

        # print(f'Method: {method}')
        # print(f'Path: {path}')
        # print(f'HTTP: {http_version}')

    def __format_headers(self):
        headers = self._lines[1:]

        for index, header in enumerate(headers):
            if header:
                header_split = header.split(':')

                name = header_split[0]
                value = header_split[-1].strip()

                # print(f'Header Name: {name}')
                # print(f'Header Value: {value}')

                self.request_obj.headers[name] = value
            else:
                # obtendo o body
                self.body = header[index + 1:]
                break

    def __format_params(self):
        # exemplo: /login?user=jaedson&pid=3949
        path_split = self.request_obj.path.split('?')
        new_path = path_split[0]

        if len(path_split) < 2:
            return

        args = path_split[1]

        # definindo novo path
        self.request_obj.path = new_path

        # obtendo parâmetros da URL
        self.request_obj.params = self.__get_value_with_name(args, format_args=True)

    def __format_cookies(self) -> None:
        # obtém todos os cookies
        # e retorna um dicionário.

        cookies = self.request_obj.headers.get('Cookies')

        if not cookies:
            return

        self.request_obj.cookies = self.__get_value_with_name(cookies)
        self.request_obj.headers['Cookies'] = self.request_obj.cookies

    def __get_value_with_name(self, content, format_args=False) -> dict:
        # essa função obtém valores de headers
        # que são nesse formato e retorna em
        # um dicionário:
        # 
        # timeout=1; cookie=02dSl09

        content = content.replace(' ', '')
        decrypt = False

        if format_args:
            values = content.split('&')
        else:
            values = content.split(';')
            decrypt = True

        result = {}

        for v in values:
            v_split = v.split('=')

            # a variavel 'value' recebe todos
            # os valores da lista depois do index
            # 1.
            #
            # isso acontece porque se tivermos um valor "HSFD==",
            # o método split também irá fatiar os dois sinais presentes
            # no valor ("...=="), fazendo com que a lista possua
            # mais de dois valores.

            name = v_split[0]
            value = '='.join(v_split[1:])
            if decrypt:
                try:
                    value = self.fr.decrypt(value.encode()).decode()
                    print(f'Value decyrpt: {value}')
                except (InvalidKey, UnsupportedAlgorithm):
                    # se este erro ocorrer. significa que a chave
                    # secreta ou o valor do cookie foi alterado
                    pass

            result[name] = value

        return result


if __name__ == '__main__':
    app = Formatter('POST /login?user=jaedson&pid=3949 HTTP/1.1\n'
                    'Host: 127.0.0.1\n'
                    'Connection: keep-alive\n'
                    'Cookies: auth=gAAAAABh1IW0nELxt0Via7ezKwEuCckJEwa2WHTIaMd2sFxlcdUr-ZIxRpD_RTW0kPJ8TE17f8upmGJr8Pjrgnv5mZ_RJxU3Uw==', key='PfyVEm3rkC2p4ioeUvNprDiTm6A4OTU3ST5xb35UlEU=')

    # print(app.request_obj.__dict__['params'])
