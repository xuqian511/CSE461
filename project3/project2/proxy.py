import socket
import select
import time
import sys

import request_parser as parser

delay = 0.0001
buf_size = 4096
HTTPS_DEFAULT_PORT = 443
HTTP_DEFAULT_PORT = 80

# socket from server to browser
class Forward(object):
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception as e:
            print(e)
            return False

class ProxyServer(object):


    def __init__(self, host, port):
        self.input_list = []
        self.channel = {}
        # server socket setup
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen()

    def run(self):
        self.input_list.append(self.server)
        while True:
            # sleep to prevent breaking things
            time.sleep(delay)

            # fetches server fp when its ready
            read_ready, write_ready, exception_ready = select.select(self.input_list, [], [])
            # print(read_ready)

            for fp in read_ready:
                if not fp in self.input_list:
                    # removed by close
                    continue

                if fp == self.server:
                    self.accept()
                    break

                try:
                    self.data = fp.recv(buf_size)
                except (ConnectionAbortedError, ConnectionResetError):
                    # print("ConnectionError: closing " + str(fp))
                    self.close(fp)
                    break

                if len(self.data) == 0:
                    self.close(fp)
                    break
                else:
                    self.recv(fp)


    def accept(self):
        # attempt to establish connection between client (locahost) and server
        # accept connection to browser
        client_sock, client_addr = self.server.accept()

        # read data to determine forwarding host
        self.data = client_sock.recv(buf_size)

        # if empty reset
        if (len(self.data) == 0):
            client_sock.close()
            return

        # retrieve host's address and IP
        request = parser.HTTPRequest(self.data)
        request.print_request_line()
        forward_to = request.headers['host'].split(':')
        if (len(forward_to) == 2):
            forward_to[1] = int(forward_to[1])
        else:
            if request.path.find('https://') != -1:
                forward_to.append(HTTPS_DEFAULT_PORT)
            else:
                forward_to.append(HTTP_DEFAULT_PORT)

        forward = Forward().connect(forward_to[0], forward_to[1])
        if forward:
            # print("Client has successfuly connected")

            if (request.command == "CONNECT"):
                # send success to client
                client_sock.send(b'HTTP/1.1 200 OK\r\n\r\n')
            else:
                request.headers['connection'] = 'close'
                if ('proxy-connection' in request.headers.keys() and \
                    request.headers['proxy-connection'] == 'keep-alive'):
                    request.headers['proxy-connection'] = 'close'
                request.protocol_version = 'HTTP/1.0'
                self.data = request.rebuild_message()
                forward.send(self.data)

            # add fps to readables
            self.input_list.append(client_sock)
            self.input_list.append(forward)

            # map client to server and vise versa
            self.channel[client_sock] = forward
            self.channel[forward] = client_sock

        else:
            # print("Cannot establish connection with client")

            if (request.command == "CONNECT"):
                # send success to client
                client_sock.send(b'HTTP/1.1 502 Bad Gateway\r\n\r\n')
            client_sock.close()

    def close(self, fp):
        # close the connnection between client and server
        # print(fp.getpeername(), "has disconnected")

        # remove fp and its mapping from readables
        self.input_list.remove(fp)
        self.input_list.remove(self.channel[fp])

        # close connection with client and remote server
        out = self.channel[fp]
        self.channel[out].close()
        self.channel[fp].close()

        # remove from mapping
        del self.channel[out]
        del self.channel[fp]

    def recv(self, fp):
        try:
            self.channel[fp].send(self.data)
        except ConnectionAbortedError:
            # print("ConnectionAbortError: closing " + str(fp))
            self.close(fp)


