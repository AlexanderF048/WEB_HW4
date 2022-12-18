import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket
from threading import Thread
from datetime import datetime


class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/contact_us':
            self.send_html_file('contact_us.html')
        elif pr_url.path == '/pictures':
            self.send_html_file('pictures.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        form_client_run(data, '127.0.0.1', 5000)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def form_socket_run():
    serv_socket_form = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serv_socket_form.bind(('127.0.0.1', 5000))
    try:
        while True:
            data, address = serv_socket_form.recvfrom(1024)
            print(f'Received data: {data.decode()} from: {address}')
            data_parse = urllib.parse.unquote_plus(data.decode())
            # print(data_parse)
            data_dict = {
                datetime.datetime.now(): {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}}
            print(data_dict)
            with open('test.txt', 'wb') as txt_test:
                txt_test.write(data)


    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        serv_socket_form.close()


def form_client_run(data, ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.sendto(data, server)
    print(f'Send data: {data.decode()} to server: {server}')
    response, address = sock.recvfrom(1024)
    print(f'Response data: {response.decode()} from address: {address}')
    sock.close()


if __name__ == '__main__':
    http_serv_thread = Thread(target=run, args=())
    socket_serv_thread = Thread(target=form_socket_run, args=())

    http_serv_thread.start()
    socket_serv_thread.start()
