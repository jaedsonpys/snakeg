from exceptions import InvalidHTTPMessage
from _request import Request


class Formatter:
    def __init__(self, http_message: str):
        self._lines = http_message.split('\n')
        self.request_obj = Request()

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

    @staticmethod
    def __get_value_with_name(content, format_args=False) -> dict:
        # essa função obtém valores de headers
        # que são nesse formato e retorna em
        # um dicionário:
        # 
        # timeout=1; cookie=02dSl09

        content = content.replace(' ', '')

        if format_args:
            values = content.split('&')
        else:
            values = content.split(';')

        result = {}

        for v in values:
            name, value = v.split('=')
            result[name] = value

        return result


if __name__ == '__main__':
    app = Formatter('POST /login?user=jaedson&pid=3949 HTTP/1.1\n'
                    'Host: 127.0.0.1\n'
                    'Connection: keep-alive\n'
                    'Cookies: 1P_JAR=2021-12-27-23; NID=511')

    print(app.request_obj.__dict__['params'])
