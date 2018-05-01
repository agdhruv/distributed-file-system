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
    c.send("Hello Client")
    fileToServe = b''

    while True:
        data = c.recv(1)

        if data == b'\n':
            break
        fileToServe += data
    f = open(fileToServe, 'rb')
    l = f.read(1024)

    while l:
        c.send(l)
        print("Sent:", repr(l))
        l = f.read(1024)
    f.close()

    print('Successfully sent the file')
    c.close()
    print('connection closed')
