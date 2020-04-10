import asyncio
import asyncio
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
    return JSONResponse({
        'user_id': f'{user.id}',
        'game_id': f'{game_number}',
        'game_owner': f'{user.id}',
        'players': f'{games[game_number].get_players()}'
    })


async def join_game(request: Request):
    body = await request.json()
    player_name = body.get('player_name')
    game_id = body.get('game_id')
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
    return JSONResponse({
        'user_id': f'{user.id}',
        'players': f'{game.get_players()}',
        'game_owner': f'{game.get_owner_id()}',
        'game_id': f'{game_id}'
    })

# @app.websocket('/ws/game/{game_id}')
# async def websocket_endpoint(websocket: WebSocket, game_id: int):
#     await websocket.accept()
#     game_queue = game_queues[game_id]
#     game = games[game_id]
#     await websocket.send_json(game.__dict__)
#     while True:
#         await asyncio.sleep(5)
#         message = {'message': 'hello'}
#         await websocket.send_json(message)
#         # event = await game_queue.get()
#         # await websocket.send_text(f'{event}')
#         # game_queue.task_done()

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
        while RUNNING:
            await asyncio.sleep(2)
            # next_event = await EVENT_QUEUE.get()
            next_event = {'message': 'your mom'}
            print('got event', next_event)
            yield dict(data=next_event)
    except asyncio.CancelledError as error:
        pass


async def event_stream(request: Request):
    return EventSourceResponse(estream())


async def worker(queue):
    print('worker started')
    while True:
        event = await queue.get()
        print(f'{event}')
        if (event.type == 'GAME'):
            print('event going to game queue')
            # TODO make sure game/queue exists
            game_queue = game_queues[event.game_id]
            game = games[game_id]
            await game_queue.put(game)

        queue.task_done()


async def startup():
    asyncio.create_task(worker(EVENT_QUEUE))


async def shutdown():
    global RUNNING
    RUNNING = False

routes = [
    Route('/', index),
    Route('/api/spend', spend),
    Route('/api/create_game', create_game),
    Route('/api/join_game', join_game),
    Route('/api/event_stream', endpoint=event_stream),
    Route('/api/game/{game_id}', game_stream),
    Mount('/static', StaticFiles(directory='static/dist'), name='static')
]
app = Starlette(routes=routes, middleware=middleware, on_startup=[startup], on_shutdown=[shutdown])


def run():
    return app
