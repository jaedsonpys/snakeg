from base64 import urlsafe_b64encode


def set_key(key: bytes):
    with open('.env', 'w') as env_file:
        key = urlsafe_b64encode(key).decode()
        env_file.write(f'SNKEY={key}')


def get_key():
    with open('.env', 'r') as env_file:
        content = env_file.read()
        value = content[6:]

    return value.encode()


if __name__ == '__main__':
    from cryptography.fernet import Fernet
    fr = Fernet(get_key())
    print(get_key())
