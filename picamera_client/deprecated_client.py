import asyncio
import socketio
import sys

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection established')

@sio.event
async def my_message(data):
    print('message received with ', data)
    await sio.emit('my response', {'response': 'my response'})

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('http://localhost:5000',wait_timeout=10)
    await sio.wait()
    # await sio.emit('update live parameters', {'response': 'my response'})
    # import code
    # code.interact(local=dict(globals(), **locals()))
    # try:
    # except asyncio.CancelledError as e:
    #     print('disconecting...')



if __name__ == '__main__':
    asyncio.run(main())