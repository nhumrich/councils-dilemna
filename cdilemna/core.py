import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import json

app = FastAPI()

RUNNING = True
EVENT_QUEUE = asyncio.Queue()

@app.get("/", response_class=HTMLResponse)
async def index():
    with open('static/dist/index.html') as f:
        contents = f.read()
        print(contents)
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


@app.on_event('shutdown')
async def shutdown():
    global running
    running = False

def run():
    return app
