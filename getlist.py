from __future__ import print_function
import socket
from contextlib import closing

def main():
  #host = '219.98.61.56/get_record_file.cgi?PageIndex=0?PageSize=128&loginuse=admin&loginpas=bukkuden&user=admin&pwd=bukkuden&'
  host = '219.98.61.56'
  port = 48257
  bufsize = 4096

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  with closing(sock):
    sock.bind((host, port))
    while True:
      print(sock.recv(bufsize))
  return

if __name__ == '__main__':
  main()
