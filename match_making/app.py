import asyncio
import websockets
import json
from pydantic import BaseModel, ValidationError
from collections import OrderedDict
import uuid


MATCH_PLAYER_NUM = 4
ticket_pool = OrderedDict()
ticket_status = dict()
ticket_game = dict()


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
    GameMode: int


running_games = list()


def create_game():
    # not implement yet
    game_stat = {
        "IP": "127.0.0.1",
        "Port": "8787"
    }
    return Game(**game_stat)


async def core_match_pair():
    print("hi")
    while True:
        if len(ticket_pool.keys()) >= MATCH_PLAYER_NUM:
            game = create_game()
            for key in ticket_pool.keys():
                ticket_status[key] = True
                ticket_game[key] = game
            for key in ticket_pool.keys():
                if ticket_status[key]:
                    del ticket_pool[key]


async def find_match(
        user_id: str
):
    authid = uuid.uuid3(uuid.NAMESPACE_URL, user_id)
    ticket_pool[authid] = user_id
    ticket_status[authid] = False

    while not ticket_status[authid]:
        continue

    match_info_dict = dict()
    match_info_dict['GameServerIP'] = ticket_game[authid].IP
    match_info_dict['GameServerPort'] = ticket_game[authid].Port
    match_info_dict['success'] = True
    match_info_dict['ConnectionAuthId'] = authid

    del ticket_game[authid]
    del ticket_status[authid]

    match_info = MatchInfo(**match_info_dict)

    return match_info


async def handler(websocket):
    try:
        message = await websocket.recv()
    except websockets.ConnectionClosedOK:
        return
    print(message)
    deserialize_message = json.loads(message)
    try:
        ticket = Ticket(**deserialize_message)
    except ValidationError as e:
        print(e.json())
    # while True:
    #     continue


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())