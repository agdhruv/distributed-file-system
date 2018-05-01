import socket, sys  # Import socket module

s = socket.socket()  # Create a socket object
# host = socket.gethostname()  # Get local machine name
host = '0.0.0.0'
print(host)
port = int(sys.argv[1])  # Reserve a port for your service.
# folder_name = sys.argv[2]
s.bind((host, port))  # Bind to the port

s.listen(5)  # Now wait for client connection.

print('Server listening....')

while True:
    c, addr = s.accept()  # Establish connection with client.
    print('Got connection from', addr)
    c.send(b'Hello client!')

    header = b''

    while True:
        data = c.recv(1)

        if data == b'\n':
            break
        header += data

    with open(header, 'wb') as f:
        print(header, 'opened')

        while True:
            # print 'receiving data...'
            data = c.recv(1024)
            if not data:
                break
            # print 'data = %s' % data
            f.write(data)
    print('Successfully received the file')
    c.close()
    print('connection closed')
