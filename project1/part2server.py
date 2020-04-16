import socket
import threading
import random
from _thread import *
from time import sleep
from struct import pack, unpack

header_size = 12
secret = 0
server_step = 2
udp_ip="127.0.0.1"
byte_alignment=4
buffer_len = 1024
timeout = 3
backlog=10
"""
unexpected number of buffers have been received
unexpected payload, or length of packet or length of packet payload has been received
the server does not receive any packets from the client for 3 seconds
the server does not receive the correct secret
"""

def ProcessPacket(message, client_ip):
    # Part A
    expected_payload = "hello world" + '\0'
    expected_message_len = header_size + len(expected_payload)
    
    payload_len, presecret, step, sid = unpack('>iihh', message[0:12])
    payload = message[12:12+payload_len]
    
    if presecret!=secret or payload!=expected_payload.encode('utf-8')\
    or len(payload)!= len(expected_payload) or expected_message_len!=len(message) \
    or expected_payload.encode('utf-8')!=payload :
        return
    #random policy
    num = random.randint(5, 16)
    ln = random.randint(24, 400)
    udp_port = random.randint(20000, 32000)
    secretA = random.randint(1, 400)
    response = pack('>iihhiiii', 16, presecret, server_step, sid, num, ln, udp_port, secretA)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.sendto(response, client_ip)
    
    # Part B
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))
    sock.settimeout(timeout)
    print(udp_port)
    print(udp_ip)
    
    payload_of_length_len = ln + 4
    if (payload_of_length_len % byte_alignment != 0):
        payload_of_length_len = ln + 4 + (byte_alignment - (ln % byte_alignment))

    expected_message_len = header_size + payload_of_length_len
    num_received = 0
    
    while num_received < num:
        print(num_received)
        try:
            message = sock.recv(buffer_len)
        except:
            return
        payload_len, psecret, step, sid, pid = unpack('>iihhi', message[0: header_size+4])
        payload = message[header_size+4: header_size+4 + payload_len]
        if (psecret != secretA or payload_len != ln + 4 or pid != num_received) or (len(message) != expected_message_len):
            return
        
        response = pack('>iihhi', 4, psecret, server_step, sid, num_received)
        sock.sendto(response, client_ip)
        num_received += 1

    tcp_port =  random.randint(20000, 32000)
    secretB = random.randint(1, 400)
    response = pack('>iihhii', 4, psecret, server_step, sid, tcp_port, secretB)
    sock.sendto(response, client_ip)
    #part C
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((udp_ip, tcp_port))
    sock.listen(backlog)
    
    connection, client_address = sock.accept()
    num2 = random.randint(5, 16)
    len2 = random.randint(24, 400)
    secretC = random.randint(1, 400)
    special_char = chr(random.randint(0, 100)) 
    
    response = pack('>iihhiii', 13 , secretB, step, sid, num2, len2, secretC) + special_char.encode("ascii")
    connection.sendto(response, client_address)
    # Part D
    received_messages = 0
    sock.settimeout(timeout)
    message_length = header_size + len2

    if (message_length % byte_alignment != 0):
        message_length += (byte_alignment - message_length % byte_alignment)

    while received_messages < num2:
        try:
            message = connection.recv(message_length)
        except:
            return
        
        # Verify message contents
        if (len(message) != message_length):
            return

        payload_len, psecret, step, sid = unpack('>IIHH', message[0:header_size])
        payload = message[header_size:header_size + len2]

        if (psecret != secretC or payload_len != len2):
            return

        for i in range(len2):
            if chr(payload[i]) != special_char:
                return

        received_messages += 1

    #random create SecretD
    secretD = random.randint(1, 400)
    response = pack('>IIHHI', 4, secretC, step, sid, secretD)
    connection.sendto(response, client_address)

    
def Main():
    udp_port = 12235
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))
    while True:
        message, client_ip = sock.recvfrom(buffer_len)
        start_new_thread(ProcessPacket, (message, client_ip))
    sock.close()

if __name__ == '__main__':
    Main()