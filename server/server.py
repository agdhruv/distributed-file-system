import socket               # Import socket module
import os

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.

print 'Server listening...'

while True:
    c, addr = s.accept()     # Establish connection with client.
    print '\n[+] Got connection from', addr
    c.send('Hello client!')

    header = ''

    # create header--basically the filename from the source
    while True:
        data = c.recv(1)

        if data == '\n':
            break

        header += data
    
    # read the file that was sent and write to file with the same file name
    with open(header, 'wb') as f:
        print header, 'opened'

        while True:
            data = c.recv(1024)
            if not data:
                break
            f.write(data)

    print 'Successfully received the file', header
    c.close()
    print '[-] Connection closed with', addr

    # at this point, the file has reached level 2 (Dhruv's laptop)
    # now it has to be sent to the storage node i.e. level 3 (Harshit's laptop)

    # create a new socket object to send the code
    s2 = socket.socket()
    host2 = '10.1.19.139'

    # decide port number on the basis of the file extension
    filename, file_extension = os.path.splitext(header)
    file_extension = file_extension[1:] # removing the dot from the file extension
    supported_mappings = ['mp3', 'txt', 'pdf']

    extension_port_mapping = {
        'mp3': 9000,
        'txt': 9001,
        'pdf': 9002,
        'others': 9003
    }

    if file_extension not in supported_mappings:
        file_extension = 'others'

    port2 = extension_port_mapping[file_extension]

    # we have the port number decided at this point
    # now we just need to send the file to the decided port

    # now, update the index
    with open('myIndex/index.txt', 'a+') as f:
        f.seek(0)
        for line in f:
            line = line.rstrip('\n')
            # if filename exists: modification. Mention that in the log
            if line == header:
                line = line + '/\n'
                break

    s2.connect((host2, port2))

    data = s2.recv(1024)
    print 'Message received from node:', repr(data)

    # send the filename and extension to the server to store it
    s2.send(file_extension + '/' + header + '\n')

    # open the file to be read and sent
    f = open(header, 'rb')
    l = f.read(1024)
    while l:
        s2.send(l)
        l = f.read(1024)
    f.close()

    os.remove(header)

    with open('myIndex/index.txt', 'r') as f:
        for line in f:
            print line

    import time
    time.sleep(10)

    # now, update the index
    with open('myIndex/index.txt', 'a+') as f:
        f.seek(0)
        file_found = False
        for line in f:
            line = line.rstrip('\n')
            # if filename already exists, update flag
            if line.rstrip('/') == header:
                line = line[:-1]
                file_found = True
                break

        if not file_found:
            f.write(header + '\n')

    print 'Done sending', file_extension + '/' + header, 'to port', port2, 'of storage node\n'
    s2.close()
