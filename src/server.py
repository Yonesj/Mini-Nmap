import socket
import json


class User:
    user_counter = 0

    def __init__(self, name: str, age: int):
        self.id = User.user_counter
        self.name = name
        self.age = age
        User.user_counter += 1

    def to_json(self) -> str:
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "age": self.age
        })

    def save(self):
        DB[self.id] = self

    def __str__(self):
        return self.name


DB = {
    0: User('Alice', 30),
    1: User('Bob', 25),
    2: User('Charlie', 35),
}


def handle_get_request(request: str) -> bytes:
    # Parse the request and extract the requested user ID
    request_parts = request.split()

    if len(request_parts) < 2:
        return "HTTP/1.1 400 Bad Request\n\nNo ID is specified".encode("ascii")

    user_id = int(request_parts[1])

    if user_id in DB:
        user_info = DB[user_id].to_json()
        response = f"HTTP/1.1 200 OK\nContent-Type: application/json\n\n{user_info}"
    else:
        response = "HTTP/1.1 404 Not Found\n\nUser not found"

    return response.encode("ascii")


def handle_post_request(request: str) -> bytes:
    command = request.split(' ')

    if len(command) < 3:
        return "HTTP/1.1 400 Bad Request\n".encode("ascii")

    name = command[1]
    age = int(command[2])
    User(name, age).save()

    return "HTTP/1.1 200 OK\n\nUser data updated".encode("ascii")


def main():
    host = 'localhost'
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server is listening on http://{host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        request = client_socket.recv(1024).decode("ascii")

        if "GET" in request:
            response = handle_get_request(request)
        elif "POST" in request:
            response = handle_post_request(request)
        else:
            response = "HTTP/1.1 400 Bad Request\n\nInvalid request".encode("ascii")

        client_socket.sendall(response)
        client_socket.close()


if __name__ == '__main__':
    main()
