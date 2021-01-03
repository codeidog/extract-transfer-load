import socket
import time
import os

port = 5432
server = os.environ["DB_SERVER"]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while True:
    try:
        s.connect((server, port))
        s.close()
        break
    except socket.error as ex:
        time.sleep(0.1)