import time
import socket
import random
from struct import pack, unpack

Std_Num = 199
SERVER_NAME = 'attu2.cs.washington.edu'
PORT = 12235
BUFFER_SIZE = 1024
TIMEOUT = 0.5
STEP_NUM = 1

def get_header(payload_len:int, psecret:int, step:int ,Std_Num:int) -> bytes:
    # big-endian
    header = payload_len.to_bytes(4, byteorder = 'big')
    header += psecret.to_bytes(4, byteorder = 'big')
    header += step.to_bytes(2, byteorder = 'big')
    # header += std_id.to_bytes(2, byteorder = 'big')
    # header += text.to_bytes(2, byteorder = 'big')
    header += Std_Num.to_bytes(2, byteorder = 'big')
    return header



def Stage_a():
    # Internet & UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    # Creating a Socket
    with sock as s_a:
        # no padding,'hello world' + '\0'= 12 bytes
        text = get_header(12, 0, STEP_NUM, Std_Num)
        message = 'hello world' + '\0'
        text += str.encode(message, encoding = 'utf-8')
        s_a.sendto(text,(SERVER_NAME, PORT))
        # Reference:convert the address recieved from a recvfrom() function to str
        # https://stackoverflow.com/questions/25524431/python-how-to-convert-the-address-recieved-from-a-recvfrom-function-to-a-stri
        pbytes, addr = s_a.recvfrom(BUFFER_SIZE)

        global num
        global packet_len
        global udp_port 
        global secretA
        
        num = int.from_bytes(pbytes[12:16], byteorder = 'big')
        packet_len = int.from_bytes(pbytes[16:20], byteorder = 'big')
        udp_port = int.from_bytes(pbytes[20:24], byteorder = 'big')
        secretA = int.from_bytes(pbytes[24:], byteorder = 'big')

        print(' Beginning Stage A')
        print(' Student ID#last 3 digits:',Std_Num,'\n','num:',num,'\n',\
        'packet_len:', packet_len,'\n','udp_port:',udp_port,'\n',\
        'secretA:',secretA,'\n')
    s_a.close()


def Stage_b():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    stage_b_final = None
    print(' Beginning Stage B')
    with sock as s_b:
        packet_id = 0
        for packet_id in range(num):
            text = get_header(packet_len + 4, secretA, 1, Std_Num)
            text += packet_id.to_bytes(4, byteorder = 'big')
            text += packet_id.to_bytes(packet_len, byteorder = 'big')
            # i = 0
            # while i<num:
            # header = pack( packet_len + 4, secretA, 1, 199, i)
            # if packet_len % 4 != 0:
            # payload=bytearray(packet_len+(4-packet_len%4))
            # else:
            # payload=bytearray(packet_len)
            # message=header+payload
            # sock.sendto(message, (SERVER_NAME, udp_port))
            # try:
            # sock.settimeout(timeout)
            # ans = sock.recv(chunk_size)
            # except socket.timeout:
            # i -= 1
            # i += 1
            # result = s_b.recvfrom(BUFFER_SIZE)
            while (1):
                s_b.settimeout(TIMEOUT)
                try:
                    data, addr = s_b.recvfrom(BUFFER_SIZE)
                   
        # global tcp_port
        # global secretB
        # tcp_port = int.from_bytes(stage_b_final[12:16], byteorder = 'big')
        # secretB = int.from_bytes(stage_b_final[16:20], byteorder = 'big')
        # print(' packet_id:', packet_id,'\n','tcp_port:', tcp_port,'\n',\
        # 'secretB:', secretB, '\n')
    
    s_b.close()

def Stage_c():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_NAME, tcp_port))
    pbytes, addr = sock.recvfrom(BUFFER_SIZE)

    global c
    global num2
    global secretC    
    global packet_len2
  
    num2 = int.from_bytes(pbytes[12:16], byteorder='big')
    packet_len2 = int.from_bytes(pbytes[16:20], byteorder='big')
    secretC = int.from_bytes(pbytes[20:24], byteorder='big')
    c = bytes.decode(pbytes[24:25], encoding='utf-8') 
    print(' Beginning Stage C')
    print(' num2:', num2,'\n','packet_len2:', packet_len2,'\n',\
    'secretC:',secretC,'\n')





if __name__ == '__main__':
    
    Stage_a()
    Stage_b()
    Stage_c()
  
    socket.socket(socket.AF_INET, socket.SOCK_STREAM).close()
