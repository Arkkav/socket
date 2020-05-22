import socket
from views import *

URLS = {
    # '/': 'Hello index',
    # '/blog'index:'Hello blog',
    '/': index,
    '/blog': blog,

}


def parse_request(request):
    parsed = request.split()
    method = parsed[0]
    url = parsed[1]
    return (method, url)


def generate_headers(method, url):
    if not method == 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)  # отделяем заголовок от тела

    if url not in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)

    return ('HTTP/1.1 200 OK\n\n', 200)


def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    if code == 404:
        return '<h1>404</h1><p>not found</p>'
    return URLS[url]()


def generate_response(request):
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)  # если url не тот, то 404, если method, то др. заголовок
    body = generate_content(code, url)

    return (headers + body).encode()


def run():
    # создаем субъекта
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # указали, какой протокол будет исп-ть.
    # AF_INET - протокол 4-й версии
    # SOCK_STREAM - TCP протокол
    # Связываем субъекта с конкретным IP:port
    # server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)  # опции (на каком уровне SOlevel, переисп. адрес устан. в 1 (не SO_REUSEADDR))
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,
                             1)  # sudo fuser -k 5000/tcp            - удаляем порт

    server_socket.bind(('localhost', 5000))  # картеж
    # Теперь нужно сказать: чувак, давай, тебе могут придти пакеты, иди посмотри
    server_socket.listen()

    while True:
        clint_socket, addr = server_socket.accept()  # возвращает картеж, кот. распаковываем в 2-е переменные
        # возвращает сокет, но со сороны клиенты
        request = clint_socket.recv(1024)  # 1024 - кол-во байт в пакете
        # print(request.decode('utf-8'))  # можно просто request
        print(request)  # приходит в bytes, более наглядно бывает
        print()
        print(addr)

        response = generate_response(request.decode('utf-8'))  # декодируем все таки, т.к. приходит в браузер

        clint_socket.sendall(response)  # преобразовываем из строки с bytes
        '''
        localhost sent an invalid response.
        ERR_INVALID_HTTP_RESPONSE - в chrome! а в firefox вывод корректен. Скорее всего дело в заголовках
        '''
        clint_socket.close()  # ничего не увидем, пока не закроем соединение


if __name__ == '__main__':
    run()
