import socket
from struct import pack, unpack


UDP_PORT=12235 
presecret=0 
cur_step=1 
sid=128 
chunk_size=1024 
byte_alignment=4 
timeout=1 
Domain='127.0.0.1'

print("Beginning Stage A")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message='hello world'+'\0'
header=pack('>iihh',len(message),presecret,cur_step,sid)+message.encode('utf-8')
sock.sendto(header,(Domain,UDP_PORT))
result = sock.recv(chunk_size)
#print(unpack('>iihhiiii', result))
payload_len, psecret, step, sid, num, length, UDP_PORT, secretA = unpack('>iihhiiii', result)
print('payload_len:',payload_len,'presecret',psecret,'step',step,'student id#last 3 digits',sid, 'num',\
      num,'len', length,'udp_port',UDP_PORT,'secretA',secretA)

print("Beginning Stage B")

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
print('payload_len:',payload_len,'presecret',psecret,'step',step,'student id#last 3 digits',sid,\
      'tcp_port',TCP_port,'secretB',secretB)
print("Beginning Stage C")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((Domain,TCP_port))
sock.settimeout(timeout)
ans = sock.recv(chunk_size)
#print(unpack('>iihhiiic', ans[0:25]))
payload_len, psecret, step, sid, num2, len2, secretC, c= unpack('>iihhiiic', ans[0:25])
print('payload_len:',payload_len,'presecret',psecret,'step',step,'student id#last 3 digits',sid,\
      'num2',num2,'len2',len2,'secretC',secretC)

print("Beginning Stage D")
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
print('payload_len',payload_len,'presecret',psecret,'step',step,'student id#last3 digits',sid,'secretD',secretD)
#print(unpack('>iihhi', ans))
