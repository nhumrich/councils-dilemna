import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from cdilemna.user import User
from cdilemna.game import Game
import json
import random

app = FastAPI()

games = {}
players = {}
game_queues = {}

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RUNNING = True
EVENT_QUEUE = asyncio.Queue()

@app.get("/", response_class=HTMLResponse)
async def index():
    with open('static/dist/index.html') as f:
        contents = f.read()
        return contents


class Spend(BaseModel):
    current_player: str
    amount: int
    destination: str


@app.post('/api/spend')
async def read_item(spend: Spend):
    message = {'message': f'Player {spend.current_player} spent {spend.amount} and sent it to {spend.destination}'}
    await EVENT_QUEUE.put(message)
    return message

class Game_to_create(BaseModel):
    user_name: str

@app.post('/api/create_game')
async def create_game(game_to_create: Game_to_create):
    user_name = game_to_create.user_name
    game_number = random.randint(100000, 999999)
    user = User(user_name)
    players[user.id] = user
    while game_number in games:
        game_number = random.randint(100000, 999999)

    game = Game(user.id)
    games[game_number] = game
    game_queue = asyncio.Queue()
    game_queues[game_number] = game_queue
    user.game_id = game_number
    return {
        'user_id': f'{user.id}',
        'game_id': f'{game_number}',
        'game_owner': f'{user.id}',
        'players': f'{games[game_number].get_players()}'
    }

class JoinGame(BaseModel):
    game_id: int
    player_name: str

@app.post('/api/join_game')
async def join_game(joinable: JoinGame):
    player_name = joinable.player_name
    game_id = joinable.game_id
    game = games[game_id]
    # TODO ensure game exists
    user = User(player_name)
    players[user.id] = user
    # TODO ensure that we only add the player if the game is in 'SETUP' status
    game.add_player(user.id)
    await EVENT_QUEUE.put(
        {
            'type': 'GAME',
            'message': f'{player_name} joined the game {game_id}',
            'game_id': f'{game_id}'
        }
    )
    return {
        'user_id': f'{user.id}',
        'players': f'{game.get_players()}',
        'game_owner': f'{game.get_owner_id()}',
        'game_id': f'{game_id}'
    }

@app.websocket('/ws/game/{game_id}')
async def websocket_endpoint(websocket: WebSocket, game_id: int):
    await websocket.accept()
    game_queue = game_queues[game_id]
    game = games[game_id]
    await websocket.send_text({f'{json.dumps(game.__dict__)}'})
    while True:
        event = await game_queue.get()
        await websocket.send_text(f'{event}')
        game_queue.task_done()


async def estream():
    try:
        while RUNNING:
            next_event = await EVENT_QUEUE.get()
            print('got event', json.dumps(next_event).encode())
            yield json.dumps(next_event).encode() + b'\n'
    except asyncio.CancelledError as error:
        pass


@app.get('/api/event_stream')
async def event_stream():
    return StreamingResponse(estream(), media_type='text/event-stream')


app.mount('/static', StaticFiles(directory='static/dist'), name='static')


async def worker(queue):
    while True:
        event = await queue.get()
        print(f'{event}')
        if (event.type == 'GAME'):
            # TODO make sure game/queue exists
            game_queue = game_queues[event.game_id]
            game = games[game_id]
            await game_queue.put(game)

        queue.task_done()

@app.on_event('shutdown')
async def shutdown():
    global running
    running = False

def run():
    return app
