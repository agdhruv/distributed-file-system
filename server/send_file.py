import socket               # Import socket module
import os

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12346                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.

print 'Server listening...'

while True:
    c, addr = s.accept()     # Establish connection with client.
    print '\n[+] Got connection from', addr
    c.send('Hello client!')

    request = c.recv(1)

    if request == '1':
        with open("myIndex/index.txt", 'rb') as f:
            c.send("\nYour files on the server are ('/' means updating):\n")
            l = f.read(1024)

            while (l):
                c.send(l)
                print "Sent", repr(l)
                l = f.read(1024)

    elif request == '0':
        header = ''

        # create header--basically the filename from the source
        while True:
            data = c.recv(1)
            if data == '\n':
                break
            header += data

        file_exists = 'no'

        with open("myIndex/index.txt", 'r') as f:
            for line in f:
                if line.rstrip('\n') == header:
                    file_exists = 'yes'
                    break
                elif line.rstrip('\n').rstrip('/') == header:
                    file_exists = 'updating'
                    break

        c.send(file_exists)

        if file_exists == 'yes':
            # create connection with the node to fetch the file
            s2 = socket.socket()
            host2 = '10.1.19.139'
            port2 = 9004

            # decide folder in node on the basis of file extension
            file_extension = os.path.splitext(header)[1]
            file_extension = file_extension[1:] # removing the dot from the file extension
            supported_mappings = ['mp3', 'txt', 'pdf']

            if file_extension not in supported_mappings:
                file_extension = 'others'

            s2.connect((host2, port2))

            print "Now connected to the node server"

            # send file name to the node to fetch it
            s2.send(file_extension + '/' + header + '\n')

            # read the file that was sent by the node and write to file with the same file name
            with open(header, 'wb') as f:
                print header, 'opened for writing'

                while True:
                    data = s2.recv(1024)
                    if not data:
                        break
                    f.write(data)

            s2.close()
            print "Now disconnected from the node server"

            # at this point, I have the file on this computer

            # send the file to the client
            with open(header, 'rb') as f:
                l = f.read(1024)
                while (l):
                    c.send(l)
                    l = f.read(1024)

            # remove the file from my system
            os.remove(header)

    c.close()
    print '[-] Connection closed with', addr