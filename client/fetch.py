import sys, socket, time

s = socket.socket()         # Create a socket object
host = 'Dhruvs-Macbook-Pro.local' # Get local machine name
port = 12346                # Reserve a port for your service.
s.connect((host, port))

data = s.recv(1024)
print "\nMessage from server:", repr(data)

file_to_fetch = None

if len(sys.argv) == 1:       # fetching the log (list of files in the nodes)
	# send fetch command
	s.send("1")

	while True:
		data = s.recv(1024)
		if not data:
			break
		print data

	# print 'Index received'

else:                        # fetching the file asked by the client
	file_to_fetch = sys.argv[1]

	# send fetch file command
	s.send("0")

	s.send(file_to_fetch + '\n')

	exists = s.recv(1024)

	if exists == 'yes':
		with open('target_folder/' + file_to_fetch, 'wb') as f:
			# print file_to_fetch, 'opened'

			while True:
				data = s.recv(1024)
				if not data:
					break
				f.write(data)

		print 'Successfully received', file_to_fetch, 'in the target_folder/\n'
	elif exists == 'no':
		message = 'This file does not exist on the server.'
		print message
	else:
		message = 'This file is currently being updated. Please try again later.'
		print message

s.close()