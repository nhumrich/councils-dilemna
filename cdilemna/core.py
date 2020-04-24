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
PLAYERS = {}
game_connections = {'3111': {}}
connections = {}

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
    player_id = body.get('player_id')
    amount = body.get('amount')
    destination = body.get('destination')
    player = PLAYERS[player_id]
    player.spend_money(amount)
    message = {
        'type': 'GAME',
        'subtype': 'PLAYER_CHANGE',
        'currency': 'money',
        'amount': amount,
        'destination': destination,
        'message': f'Player {player_id} spent {amount} money and sent it to {destination}',
        'game_id': f'{player.game_id}'
    }
    await EVENT_QUEUE.put(json.dumps(message))
    return JSONResponse(message)

async def gain_money(request: Request):
    body = await request.json()
    player_id = body.get('player_id')
    amount = body.get('amount')
    destination = body.get('destination')
    player = PLAYERS[player_id]
    player.gain_money(amount)
    message = {
        'type': 'GAME',
        'subtype': 'PLAYER_CHANGE',
        'currency': 'money',
        'amount': amount,
        'destination': destination,
        'message': f'Player {player_id} gained {amount} money from {destination}',
        'game_id': f'{player.game_id}'
    }
    await EVENT_QUEUE.put(json.dumps(message))
    return JSONResponse(message)

async def gain_power(request: Request):
    body = await request.json()
    player_id = body.get('player_id')
    amount = body.get('amount')
    destination = body.get('destination')
    player = PLAYERS[player_id]
    player.gain_power(amount)
    message = {
        'type': 'GAME',
        'subtype': 'PLAYER_CHANGE',
        'currency': 'power',
        'amount': amount,
        'destination': destination,
        'message': f'Player {player_id} gained {amount} power from {destination}',
        'game_id': f'{player.game_id}'
    }
    await EVENT_QUEUE.put(json.dumps(message))
    return JSONResponse(message)

async def spend_power(request: Request):
    body = await request.json()
    player_id = body.get('player_id')
    amount = body.get('amount')
    destination = body.get('destination')
    player = PLAYERS[player_id]
    player.spend_power(amount)
    message = {
        'type': 'GAME',
        'subtype': 'PLAYER_CHANGE',
        'currency': 'power',
        'amount': amount,
        'destination': destination,
        'message': f'Player {player_id} sent {amount} power to {destination}',
        'game_id': f'{player.game_id}'
    }
    await EVENT_QUEUE.put(json.dumps(message))
    return JSONResponse(message)

async def player(request: Request):
    player_id = request.path_params.get('player_id')
    return JSONResponse(PLAYERS[player_id])

async def create_game(request: Request):
    body = await request.json()
    user_name = body.get('user_name')
    user_id = body.get('user_id')
    game_number = random.randint(100000, 999999)
    user = User(user_name, user_id)
    PLAYERS[user.id] = user
    while game_number in games:
        game_number = random.randint(100000, 999999)

    game = Game(user.id)
    games[game_number] = game
    # game_queue = asyncio.Queue()
    # game_queues[game_number] = game_queue
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
    PLAYERS[user.id] = user
    # TODO ensure that we only add the player if the game is in 'SETUP' status
    game.add_player(user.id)
    user.join_game(game.id)
    await EVENT_QUEUE.put(json.dumps({
            'type': 'GAME',
            'subtype': 'PLAYER_CHANGE',
            'message': f'{player_name} joined the game {game_id}',
            'game_id': f'{game_id}'
        })
    )
    return JSONResponse({
        'user_id': f'{user.id}',
        'players': f'{game.get_players()}',
        'game_owner': f'{game.get_owner_id()}',
        'game_id': f'{game_id}'
    })

async def game_stream(game_id):
    print(f'type {type(game_id)}')
    print(f'game_stream requested {game_id}')
    connection = asyncio.Queue()
    uuid = uuid4()
    if not game_id in game_connections:
        game_connections[game_id] = {}
    print(f'adding \'{uuid}\' to game_connections')
    game_connections[game_id][f'{uuid}'] = connection
    try:
        fullgame = await get_full_game_for_frontend(game_id)
        yield dict(data=fullgame)
        while RUNNING:
            next_event = await connection.get()
            parsed_event = json.loads(next_event)
            print('game steam', next_event)
            yield dict(data=next_event)
            if (parsed_event['subtype'] == 'PLAYER_CHANGE'):
                print('oh boy')
                full_game_players = await get_players_in_game_for_frontend(game_id)
                message = {
                    'players': full_game_players
                }
                yield dict(data=json.dumps(message))
            connection.task_done()
    except asyncio.CancelledError as error:
        pass

async def game_event_stream(request: Request):
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

async def get_full_game_for_frontend(game_id):
    game_id_as_number = int(game_id)
    if game_id_as_number in games:
        game_to_return = games[game_id_as_number]
        full_game_players = await get_players_in_game_for_frontend(game_id)
        return json.dumps({'type': 'GAME', 'game': game_to_return.__dict__, 'players': full_game_players})
    else:
        return json.dumps({'type': 'GAME', 'game':{}})

async def get_players_in_game_for_frontend(game_id):
    game_id_as_number = int(game_id)
    full_game_players = []
    if game_id_as_number in games:
        game_to_return = games[game_id_as_number]
        game_players = game_to_return.get_players()
        for player in game_players:
            full_player = PLAYERS[player]
            if full_player is not None:
                full_game_players.append(full_player.__dict__)
        return full_game_players
    else:
        return full_game_players


async def worker(queue):
    print('worker started')
    while True:
        await asyncio.sleep(2)
        event = await queue.get()
        parsed_event = json.loads(event)
        print(f'got event: {event}')
        if ('type' in parsed_event):
            if ('game_id' in parsed_event):
                print('event going to game queue')
                game_id = parsed_event['game_id']
                print(f'gameid {game_id}')
                if game_id in game_connections:
                    print('about to itterate in worker')
                    for key, conn in game_connections[game_id].items():
                        print(f'key: {key}')
                        await conn.put(event)
        else:
            for i, c in connections.items():
                await c.put(event)

async def test_worker(queue):
    for count in itertools.count():
        await asyncio.sleep(3)
        await EVENT_QUEUE.put(json.dumps({'message': 'your mom', 'count': count}))

async def test_worker_2(queue):
    for count in itertools.count():
        await asyncio.sleep(3)
        await EVENT_QUEUE.put(json.dumps({'type': 'GAME', 'game_id': '3111', 'count': count}))

async def startup():
    # asyncio.create_task(test_worker(EVENT_QUEUE))
    # asyncio.create_task(test_worker_2(EVENT_QUEUE))
    asyncio.create_task(worker(EVENT_QUEUE))


async def shutdown():
    global RUNNING
    RUNNING = False

routes = [
    Route('/', index),
    Route('/api/spend', spend, methods=['POST']),
    Route('/api/spend_power', spend_power, methods=['POST']),
    # These two methods are only going to be usable when the game is in setup status
    Route('/api/gain_money', gain_money, methods=['POST']),
    Route('/api/gain_power', gain_power, methods=['POST']),
    # The about two methods are only going to be usable when the game is in setup status
    Route('/api/create_game', create_game, methods=['POST']),
    Route('/api/join_game', join_game, methods=['POST']),
    Route('/api/event_stream', endpoint=event_stream),
    Route('/api/game_stream/{game_id}', endpoint=game_event_stream),
    Route('/api/player/{player_id}', player),
    Mount('/static', StaticFiles(directory='static/dist'), name='static')
]
app = Starlette(routes=routes, middleware=middleware, on_startup=[startup], on_shutdown=[shutdown])


def run():
    return app
