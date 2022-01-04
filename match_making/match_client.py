import socket

HOST = "127.0.0.1"
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(b'{"UserId":3, "Username": "username", "Rank": 1, "GameMode": 0, "CharacterType": 1}')
    while True:
        data=s.recv(1024)
        if data == b'':
            continue
        else:
            print(data)