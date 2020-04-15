import asyncio
import asyncio
import itertools
from uuid import uuid4

import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.routing import Route, Mount
from sse_starlette.sse import EventSourceResponse
from starlette.responses import JSONResponse, HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.requests import Request

from cdilemna.user import User
from cdilemna.game import Game
import json
import random

app = Starlette()

games = {}
players = {}
connections = {}
game_queues = {}

middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=['localhost', '*']),
    Middleware(CORSMiddleware, allow_origins=['*'])
]

RUNNING = True
EVENT_QUEUE = asyncio.Queue()


async def index(request):
    with open('static/dist/index.html') as f:
        contents = f.read()
        return HTMLResponse(contents)


async def spend(request: Request):
    body = await request.json()
    message = {'message': f'Player {body.get("current_player")} spent '
                          f'{body.get("amount")} and sent it to {body.get("destination")}'}
    await EVENT_QUEUE.put(message)
    return JSONResponse(message)


async def create_game(request: Request):
    body = await request.json()
    user_name = body.get('user_name')
    user_id = body.get('user_id')
    game_number = random.randint(100000, 999999)
    user = User(user_name, user_id)
    players[user.id] = user
    while game_number in games:
        game_number = random.randint(100000, 999999)

    game = Game(user.id)
    games[game_number] = game
    game_queue = asyncio.Queue()
    game_queues[game_number] = game_queue
    user.game_id = game_number
    return JSONResponse({
        'user_id': f'{user.id}',
        'game_id': f'{game_number}',
        'game_owner': f'{user.id}',
        'players': f'{games[game_number].get_players()}'
    })


async def join_game(request: Request):
    body = await request.json()
    player_name = body.get('player_name')
    player_id = body.get('player_id')
    game_id = body.get('game_id')
    # TODO ensure game exists
    game = games[int(game_id)]
    user = User(player_name, player_id)
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
    return JSONResponse({
        'user_id': f'{user.id}',
        'players': f'{game.get_players()}',
        'game_owner': f'{game.get_owner_id()}',
        'game_id': f'{game_id}'
    })

async def game_stream(game_id):
    try:
        while RUNNING:
            game_queue = game_queues[game_id]
            game = games[game_id]
            next_event = await game_queue.get()
            yield next_event
    except asyncio.CancelledError as error:
        pass


async def game_stream(request: Request):
    game_id = request.path_params.get('game_id')
    return EventSourceResponse(game_stream(game_id), media_type='text/event-stream')


async def estream():
    try:
        connection = asyncio.Queue()
        uuid = uuid4()
        connections[uuid] = connection
        while RUNNING:
            # await asyncio.sleep(2)
            # next_event = {'message': 'your mom'}
            next_event = await connection.get()
            print('got event', next_event)
            yield dict(data=next_event)
            connection.task_done()
    except asyncio.CancelledError as error:
        pass


async def event_stream(request: Request):
    return EventSourceResponse(estream())


async def worker(queue):
    print('worker started')
    while True:
        await asyncio.sleep(2)
        event = await queue.get()
        print(f'{event}')
        for i, c in connections.items():
            await c.put(event)
        # if (event[type] == 'GAME'):
        #     print('event going to game queue')
        #     # TODO make sure game/queue exists
        #     game_queue = game_queues[event.game_id]
        #     game = games[game_id]
        #     await game_queue.put(game)
        #
        # queue.task_done()

async def test_worker(queue):
    for count in itertools.count():
        await asyncio.sleep(3)
        await EVENT_QUEUE.put({'message': 'your mom', 'count': count})

async def startup():
    asyncio.create_task(test_worker(EVENT_QUEUE))
    asyncio.create_task(worker(EVENT_QUEUE))


async def shutdown():
    global RUNNING
    RUNNING = False

routes = [
    Route('/', index),
    Route('/api/spend', spend),
    Route('/api/create_game', create_game, methods=['POST']),
    Route('/api/join_game', join_game, methods=['POST']),
    Route('/api/event_stream', endpoint=event_stream),
    Route('/api/game/{game_id}', game_stream),
    Mount('/static', StaticFiles(directory='static/dist'), name='static')
]
app = Starlette(routes=routes, middleware=middleware, on_startup=[startup], on_shutdown=[shutdown])


def run():
    return app
