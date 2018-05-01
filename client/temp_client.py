import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = 'Dhruvs-Macbook-Pro.local' # Get local machine name
port = 12345                # Reserve a port for your service.

s.connect((host, port))

data = s.recv(1024)
print 'Client received', repr(data)

# send filename and extension and then open file to be read and sent
filename = 'SDCI'
extension = '.pdf'

s.send(filename + extension + '\n')

f = open(filename + extension, 'rb')
l = f.read(1024)    # read 1024 bytes of data
while (l):
    s.send(l)
    print 'Sent', repr(l)
    l = f.read(1024)
f.close()

print 'Done sending'
s.close()
