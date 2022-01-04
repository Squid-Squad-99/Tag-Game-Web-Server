import asyncio
import websockets
import json
from pydantic import BaseModel, ValidationError
import queue


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


ticket_pool = queue.Queue()
e


async def handler(websocket):
    while True:
        try:
            message = await websocket.recv()
        except websockets.ConnectionClosedOK:
            break
        deserialize_message = json.loads(message)
        try:
            ticket = Ticket(**deserialize_message)
        except ValidationError as e:
            print(e.json())
            break
        print(ticket.UserId)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())