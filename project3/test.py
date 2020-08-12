import socket


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('cnn.com', 80))
    request = b'GET cnn.com HTTP/1.1\n\n'
    s.send(request)
    print(s.recv(4096).decode())

main()