import socket

HOST = "taggame.dodofk.xyz"
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.send(b'{"UserId":2, "Username": "username", "Rank": 1, "GameMode": 0, "CharacterType": 0}')
    while True:
        data=s.recv(1024)
        if data == b'':
            continue
        else:
            print(data)