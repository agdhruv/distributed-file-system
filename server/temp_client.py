import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = '10.1.19.71' # Get local machine name
port = 9001                # Reserve a port for your service.

s.connect((host, port))

data = s.recv(1024)
print 'Client received', repr(data)

# send filename and extension and then open file to be read and sent
filename = 'to_send'
extension = '.txt'

s.send(filename + extension + '\n')

f = open(filename + extension, 'rb')
l = f.read(1024)    # read 1024 bytes of data
while (l):
    s.send(l)
    # print 'Sent', repr(l)
    l = f.read(1024)
f.close()

print 'Done sending'
s.close()