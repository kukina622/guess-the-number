import os
import socket
import threading
import random


bind_ip = '0.0.0.0'
bind_port = 8005
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, bind_port))
server.listen(25)
print("[+]listening on %s, %d" % (bind_ip, bind_port))

def handle_client(client_socket):
  r = random.Random()
  r.seed(os.urandom(16))
  client_socket.sendall("Welcome to Guess the Number Contest2\n".encode())
  while 1:
    client_socket.sendall("Whats your guess: \n".encode())
    guess = client_socket.recv(1024).decode(encoding='UTF-8').strip()
    answer = str(r.getrandbits(32))
    if guess == answer:
      content = ""
      path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"flag.txt")
      with open(path,"r") as f:
        content = f.read()
      client_socket.sendall(f"Correct!!! The flag is {content}\n".encode())
      break

    else:
      client_socket.send(f"None, true answer is {answer}\n".encode())

  client_socket.close()

while True:
  client, addr = server.accept()
  print("[*]Accepted connection from:%s:%d" % (addr[0], addr[1]))
  
  client_handler = threading.Thread(target=handle_client, args=(client, ))
  client_handler.start()
