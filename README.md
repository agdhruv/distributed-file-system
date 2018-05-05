# distributed-file-system

Programming assignment 3 for the Operating Systems course at Ashoka University taught by Professor Anirban Mondol. Uses primarily python watchdog and python sockets.


## Folder Structure

Ideally, this project requires three different machines: one acts as the **Client**, another acts as the **Server**, and the third has all the **Storage Nodes**.

1) **Client**: This is where the source folder is located. Any file creation or modification (detected using [Watchdog](https://pythonhosted.org/watchdog/)) in the `client/source_folder/` is immediately synced to the server using the `client/client_watch.py` script. Later, this file can be retrieved using the `client/fetch.py` script in the `client/target_folder/` folder.

2) **Server**: This is where most of the work happens. The script `server/server.py` listens for connections from the client, writes a synced file locally, decides the storage node (port number) a file must be sent to on the basis of its extension, sends the file to the appropriate storage node, updates the local file index on the server (stored in `server/myIndex/index.txt`), and then deletes the file locally. At this point, the file has been sent to the storage node (the third computer system).

	The file `server/send_file.py` listens to fetch file requests from the client on a different port. It sends either the list of files on the nodes (as listed in `server/myIndex/index.txt`, or sends a specific file that the client may have asked for.

3) **Storage Nodes**: On the third system, `node/node.py` must be running on 4 ports. It takes the port number as a command line argument: `$ python node.py 9000`, `$ python node.py 9001`, `$ python node.py 9002`, `$ python node.py 9003`. This starts 4 servers that correspond to port numbers that files with different extensions may be sent to by the server.

	This system also runs `node/sendFile.py` to respond to fetch requests that are sent to it by the server.


## How to run

#### On all three machines
```bash
$ git clone https://github.com/agdhruv/distributed-file-system.git
$ cd distributed-file-system/
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

#### On the client
```bash
$ cd client/
$ mkdir source_folder target_folder # git does not detect empty folders (contents of these folders are in gitignore)
$ python client_watch.py
```
```bash
# run the following to fetch a file when required (in a separate terminal)
$ python fetch.py
$ python fetch.py filename.ext
```

#### On the server
```bash
$ cd server/
$ echo "" > myIndex/index.txt # emptying index, in case it has old values
$ python server.py
```
```bash
$ python send_file.py # in a separate terminal to listen to fetch requests
```

#### On the node
```bash
$ cd node/
$ mkdir mp3 txt pdf others # folders corresponding to each port
$ python node.py 9000
```
```bash
$ python node.py 9001 # separate terminal
```
```bash
$ python node.py 9002 # separate terminal
```
```bash
$ python node.py 9003 # separate terminal
```
```bash
$ python sendFile.py 9004 # in a separate terminal to listen to fetch requests
```

## Working

* Create a file in `source_folder/`. This will be synced to the server, update in the file index, and then sent to the node.
* Now run `python fetch.py` on the client. You will receive a list of files on the nodes.
* Running `python fetch.py filename.ext` on the client. You will either receive the file in `target_folder/` or a message if the file is not found or is being updated on the node at that moment.
