# # server.py
# import socket
# import time
#
# # create a socket object
# serversocket = socket.socket(
# 	        socket.AF_INET, socket.SOCK_STREAM)
#
# objs = [socket.socket(
# 	        socket.AF_INET, socket.SOCK_STREAM) for i in range(10)]
#
# # get local machine name
# host = socket.gethostname()
# port = 0
#
# for obj in objs:
#     # bind to the port
#     obj.bind((host, port))
#
# for obj in objs:
#     # queue up to 5 requests
#     obj.listen(5)
#
# while True:
#     # establish a connection
#     clientsocket,addr = serversocket.accept()
#
#     print("Got a connection from %s" % str(addr))
#     currentTime = time.ctime(time.time()) + "\r\n"
#     clientsocket.send(currentTime.encode('ascii'))
#     clientsocket.close()

import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                 # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.

extension = "mp3"
nodeLocation = "G:\Test\\" + extension      #\\ is correct as \ was throwing errors.

f = open('torecv.png','wb')     #writing in binary mode.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print('Got connection from', addr)
    print("Receiving...")
    l = c.recv(1024)
    while (l):
        print("Receiving...")
        f.write(l)
        l = c.recv(1024)
    f.close()
    print("Done Receiving")
    c.send('Thank you for connecting')
    c.close()                # Close the connection

print(nodeLocation)
directoryList = {"mp3": "G:\Test\mp3", "txt": "G:\Test\jpeg", "jpeg": "G:\Test\jpeg"}

print(directoryList["mp3"])


