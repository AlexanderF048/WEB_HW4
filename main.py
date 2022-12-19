import mimetypes
import pathlib
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket
from threading import Thread
from datetime import datetime
import json


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
        form_client_run(data, 'localhost', 5000)
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
    serv_socket_form.bind(('localhost', 5000))

    try:
        while True:
            data, address_port = serv_socket_form.recvfrom(1024)
            print(data, address_port)
            print(f'Received data: {data.decode()} from: {address_port}')
            data_parse = urllib.parse.unquote_plus(data.decode())
            # print(data_parse)
            time_mark = datetime.utcnow()
            print(time_mark)
            data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
            print(data_dict)
            print(data_dict)
            with open('test.txt', 'w') as txt_test:
                txt_test.write(str(data_dict))

            json_dict_pattern = {str(datetime.utcnow()): data_dict}

            try:

                with open('storage/wishes.json', 'r') as j_file:
                    work_file = json.load(j_file)
                    w = dict(work_file)

                w[str(datetime.utcnow())] = data_dict

                with open('storage/wishes.json', 'w') as j_file:
                    json.dump(w, j_file)
                    print('NO exeption JSON')

            except:
                print('exeption JSON')
                with open('storage/wishes.json', 'w') as j_file:
                    json.dump(json_dict_pattern, j_file)

    except KeyboardInterrupt:
        print(f'Destroy server')
    finally:
        serv_socket_form.close()
        print("Socket port 5000 finally closed!!!")


def form_client_run(data, ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.sendto(data, server)
    print(f'Send data: {data.decode()} to server: {server}')
    # response, address = sock.recvfrom(1024) # Если включить этот код то без ответа клиент не пойдет дальше.
    # print(f'Response data: {response.decode()} from address: {address}')
    sock.close()
    print("client socket CLOSED")


if __name__ == '__main__':
    http_serv_thread = Thread(target=run, args=())
    socket_serv_thread = Thread(target=form_socket_run, args=())
    socket_serv_thread.start()
    http_serv_thread.start()
