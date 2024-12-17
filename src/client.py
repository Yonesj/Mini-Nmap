import socket


class HTTPConnection:
    def __init__(self, ip_address, port):
        self.c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c_socket.connect((ip_address, port))

    def get_request(self, id: int) -> str:
        self.c_socket.sendall(f"GET {id}".encode('ascii'))
        return self.c_socket.recv(1024).decode("ascii")

    def post_request(self, name: str, age: int) -> str:
        self.c_socket.sendall(f"POST {name} {age}".encode('ascii'))
        return self.c_socket.recv(1024).decode("ascii")