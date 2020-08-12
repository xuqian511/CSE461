import socket
import threading
import sys
import select
import datetime
#import requests
BUFFER=8192
HTTP=80
HTTPS=443

class Client_handler(threading.Thread):
    def __init__(self,proxy_socket, client_conn):
        threading.Thread.__init__(self)
        self.proxy_socket=proxy_socket
        self.client_conn=client_conn
    def run(self):
        msn=client_conn.recv(BUFFER)
        string=str(msn)
        print(string.split(' '))
    def response(self):
        
        
#        forward=string
        
        
if __name__ == '__main__':
    
    if sys.argv[1:]:
        tcp_port = sys.argv[1]
    else:
        tcp_port =HTTP
    server_ip = socket.gethostbyname("localhost")
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((server_ip, int(tcp_port)))
    proxy_socket.listen(200)
    print (datetime.datetime.now().strftime("%d %b %x")+ '- Proxy listening on 0.0.0.0:'+str(tcp_port))
    while 1:
        try:
            client_conn, client_addr = proxy_socket.accept()
            handler = Client_handler(proxy_socket, client_conn)
            handler.daemon = True
            handler.start()
        except (KeyboardInterrupt, SystemExit):
            proxy_socket.close()
            sys.exit()
    proxy_socket.close()