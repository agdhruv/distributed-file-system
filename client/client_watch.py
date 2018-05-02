import time, socket, os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):

    def send_to_server(self, event):

    	filename = os.path.split(event.src_path)[1]

    	s = socket.socket()         # Create a socket object
    	host = 'Dhruvs-Macbook-Pro.local' # Get local machine name
    	port = 12345                # Reserve a port for your service.

    	s.connect((host, port))

    	data = s.recv(1024)
    	print 'Client received', repr(data)

    	# send filename and extension and then open file to be read and sent
    	s.send(filename + '\n')

    	f = open(event.src_path, 'rb')
    	l = f.read(1024)    # read 1024 bytes of data
    	while (l):
    	    s.send(l)
    	    print 'Sent', repr(l)
    	    l = f.read(1024)
    	f.close()

    	print 'Done sending', filename
    	s.close()

        # print event.src_path, event.event_type, event.is_directory

    def on_modified(self, event):
    	# do nothing if the modification is something related to a folder
    	if event.is_directory:
    		return
        self.send_to_server(event)

    # def on_created(self, event):
    # 	# do nothing if the modification is something related to a folder
    # 	if event.is_directory:
    # 		return
    #     self.send_to_server(event)

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, './source_folder/', recursive = False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()