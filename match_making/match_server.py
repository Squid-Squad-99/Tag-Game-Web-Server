import socket
import threading
from pydantic import BaseModel, validator, ValidationError
import json
import uuid
from typing import List

HOST = ''
PORT = 9990
HUMAN_MIN = 1
GHOST_MIN = 1


class Game(BaseModel):
    IP: str = "127.0.0.1"
    Port: str = "8787"


class MatchInfo(BaseModel):
    GameServerIP: str
    GameServerPort: str
    ConnectionAuthId: str
    success: bool = True


class Ticket(BaseModel):
    UserId: int
    Username: str
    Rank: int
    GameMode: int = 0
    CharacterType: int = 0

    @validator('CharacterType')
    def type_check(cls, v):
        assert v in [0, 1], "Invalid CharacterType"
        return v

    @validator('GameMode')
    def mode_check(cls, v):
        assert v in [0], "Invalid Game Mode"
        return v


class ServerTicket(BaseModel):
    UserId: int
    Username: str
    Rank: int
    GameMode: int
    CharacterType: int
    ConnectionAuthId: str


class ServerTicketList(BaseModel):
    ServerTicketList: List[ServerTicket]



human_waiting = list()
ghost_waiting = list()

conn_dict = dict()

finish_ticket = list()


# handle ticket validation and let socket continuing connect
def handle_join(conn, data):
    deserialize_data = json.loads(data)

    try:
        ticket = Ticket(**deserialize_data)
    except ValidationError as e:
        print(e.json())

    if ticket.CharacterType == 0:
        human_waiting.append(ticket)
    else:
        ghost_waiting.append(ticket)

    conn_dict[ticket.UserId] = conn

    while True:
        if ticket not in human_waiting and ticket not in ghost_waiting:
            conn.close()
            break


def create_game():
    # not yet inplement
    game = Game()
    return game


def server_check(conn):
    while True:
        if len(finish_ticket) < 2:
            continue
        ticket_1 = finish_ticket.pop()
        ticket_2 = finish_ticket.pop()
        ticket_dict = {
            "ServerTicketList": [ticket_1, ticket_2],
        }
        response = ServerTicketList(**ticket_dict)
        conn.send(str.encode(response.json()))
        break


def core_match():
    while True:
        if len(human_waiting) >= HUMAN_MIN and len(ghost_waiting) >= GHOST_MIN:
            game = create_game()

            for _ in range(0, HUMAN_MIN):
                human = human_waiting[0]
                auth_id = str(uuid.uuid3(uuid.NAMESPACE_URL, str(human.UserId)))
                match_info = {
                    "GameServerIP": game.IP,
                    "GameServerPort": game.Port,
                    "success": True,
                    "ConnectionAuthId": auth_id
                }
                match = MatchInfo(**match_info)
                conn_dict[human.UserId].send(str.encode(match.json()))
                human_waiting.pop()

                ticket_info = {
                    "UserId": human.UserId,
                    "Username": human.Username,
                    "Rank": human.Rank,
                    "GameMode": human.GameMode,
                    "CharacterType": human.CharacterType,
                    "ConnectionAuthId": auth_id,
                }
                ticket = ServerTicket(**ticket_info)
                finish_ticket.append(ticket)

            for _ in range(0, GHOST_MIN):
                ghost = ghost_waiting[0]
                auth_id = str(uuid.uuid3(uuid.NAMESPACE_URL, str(ghost.UserId)))
                match_info = {
                    "GameServerIP": game.IP,
                    "GameServerPort": game.Port,
                    "success": True,
                    "ConnectionAuthId": auth_id,
                }
                match = MatchInfo(**match_info)
                conn_dict[ghost.UserId].send(str.encode(match.json()))
                ghost_waiting.pop()

                ticket_info = {
                    "UserId": ghost.UserId,
                    "Username": ghost.Username,
                    "Rank": ghost.Rank,
                    "GameMode": ghost.GameMode,
                    "CharacterType": ghost.CharacterType,
                    "ConnectionAuthId": auth_id,
                }
                ticket = ServerTicket(**ticket_info)
                finish_ticket.append(ticket)



if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(10)
        threads = list()
        t = threading.Thread(target=core_match)
        threads.append(t)
        t.start()
        while True:
            conn, addr = s.accept()
            data = conn.recv(1024)
            if data == b"server":
                t_outer = threading.Thread(target=server_check, args=(conn, ))
                print("This is server")
            else:
                t_outer = threading.Thread(target=handle_join, args=(conn, data, ))
                print("This is client")
            threads.append(t_outer)
            t_outer.start()
            print(len(threads))

        for i in threads:
            threads[i].join()
