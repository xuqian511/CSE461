# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 12:42:25 2020

@author: fghjk
"""
"""
In part 1 you will create a client application that will communicate with a server using a specific protocol. 
Your client's task is to follow the protocol as closely as possible 
and to extract a secret from the server for each stage of the protocol. 
The server's task is to validate that the client is following the protocol -- 
any deviation of the client from the protocol will cause the server to close the connection. 
The client and the server will communicate over UDP as well as TCP sockets. 
What follows is a thorough description of the protocol, broken up into stages (a,b,c,d). 
Remember, you must follow this protocol exactly. If you find any problems with this protocol description, 
or have further questions, do not hesitate to contact the TAs or the instructor.
"""
import socket
from struct import pack, unpack



"""
Every payload (TCP and UDP) sent to the server and sent by the server must have a packet header. 
This header must be located in the leading bytes of the transmission, prefixed to the payload. 
The header has a constant length of 12-bytes. 
The first four bytes of the header contain 
the payload length of the packet (excluding any padding to byte-align the packet). 
The next four bytes contain the secret of the previous stage of the protocol, psecret. 
The next two bytes contain an integer step number of the current protocol stage. 
For example, for step c1, the header's first four bytes will contain the length of the packet, 
the next four bytes will contain secretB, 
and the following two bytes will be set to the value 1. 
Note: for Client side, the step number will always be 1 since you are doing step 1 at each stage while the server is doing step 2. 
For stage a, psecret is defined as 0. 
The last two bytes of the header should be set to an integer representation of the last 3 digits of (one of) your student number. 
This 12-byte header does not count towards the length of the payload (which is to be 4-byte aligned). 
Throughout this part 1 description we will use diagrams such as the following to describe packet formats; 
here is the format of the packet header for part 1:
     0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                          payload_len                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            psecret                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|              step             |   last 3 digits of student #  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""
print("Beginning Part A")

UDP_PORT=12235
presecret=0
cur_step=1
sid=128
chunk_size=1024
byte_alignment=4
timeout=1
Domain='attu2.cs.washington.edu'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message='hello world'+'\0'
header=pack('>iihh',len(message),presecret,cur_step,sid)+message.encode('utf-8')
sock.sendto(header,(Domain,UDP_PORT))
result = sock.recv(chunk_size)
print(unpack('>iihhiiii', result))
payload_len, psecret, step, sid, num, length, UDP_PORT, secretA = unpack('>iihhiiii', result)

"""
STAGE a:
Step a1. The client sends a single UDP packet containing the string "hello world" 
without the quotation marks to attu2.cs.washington.edu (referred to as the 'server') on port 12235:

 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                          hello world                          |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
Note: 'hello world' is not actually 4 bytes.

Step a2. The server responds with a UDP packet containing four integers: num, len, udp_port, secretA:

 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                              num                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                              len                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            udp_port                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            secretA                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""



print("Beginning Part B")
"""
Step b1. The client reliably transmits num UDP packets to the server on port udp_port. 
Each of these 'data' packets has length len+4 (remember that each packet's entire payload must be byte-aligned to a 4-byte boundary). 
The first 4-bytes of each data packet payload must be integer identifying the packet. 
The first packet should have this identifier set to 0, while the last packet should have its counter set to num-1. 
The rest of the payload bytes in the packet (len of them) must be 0s. 
The packet header length does not count towards len:

 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                           packet_id                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|                     payload of length len                     |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

For each received data packet, the server will acknowledge (ack) that packet by replying with an 'ack' packet
that contains as the payload the identifier of the acknowledged packet:

 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        acked_packet_id                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

 
To complete this step, the client must receive ack packets from the server for all num packets that it generates. 
To do so, the client resends those packets that the server does not acknowledge. 
The client should use a retransmission interval of at least .5 seconds.

Step b2. Once the server receives all num packets, it sends a UDP packet containing two integers: a TCP port number, secretB.

 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            tcp_port                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            secretB                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""

i=0


while i<num:
    header = pack('>iihhi', length + byte_alignment, secretA, cur_step, sid, i)
    if length % byte_alignment !=0:
        payload=bytearray(length+(byte_alignment-length%byte_alignment))
    else:
        payload=bytearray(length)
    message=header+payload
    sock.sendto(message, (Domain, UDP_PORT))
    try:
        sock.settimeout(timeout)
        ans = sock.recv(chunk_size)
    except socket.timeout:
        i -= 1
    i += 1
result = sock.recv(chunk_size)
print(unpack('>iihhii', result))
payload_len, psecret, step, sid, TCP_port, secretB = unpack('>iihhii', result)
print("Beginning Part C")
"""
Step c1. The client opens a TCP connection to the server on port tcp_port received from the server in step b2.

Step c2. The server sends three integers: num2, len2, secretC, and a character: c.

 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                              num2                             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                              len2                             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            secretC                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       c       |
+-+-+-+-+-+-+-+-+

 
Note: If you receive 16 bytes as the payload_len, 
it's a mistake in our implementation so you can disregard that as it doesn't affect any of the later stages 
anyway. However don't make the same mistake in your part 2 stage c2.
"""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((Domain,TCP_port))
sock.settimeout(timeout)
ans = sock.recv(chunk_size)
print(unpack('>iihhiiic', ans[0:25]))

payload_len, psecret, step, sid, num2, len2, secretC, c= unpack('>iihhiiic', ans[0:25])

"""
Step d1. The clients sends num2 payloads, each payload of length len2, 
and each payload containing all bytes set to the character c.

 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
|           payload of length len2 filled with char c           |
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

 
Step d2. The server responds with one integer payload: secretD:

 0               1               2               3
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            secretD                            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""
print("Beginning Part D")
i=0
header = pack('>iihh', len2, secretC, cur_step, sid)
payload=c

if len2 % byte_alignment==0:
    for i in range(1,len2):
        payload+=c

else:
    for i in range(1,len2+byte_alignment-len2%byte_alignment):
        payload+=c

message=header+payload
for i in range(num2):
    sock.send(message)

sock.settimeout(timeout)
ans = sock.recv(chunk_size)
payload_len, psecret, step, sid, secretD = unpack('>iihhi', ans)
print(unpack('>iihhi', ans))