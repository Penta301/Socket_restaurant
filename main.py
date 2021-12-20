import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager

app = FastAPI()

origins = ['https://localhost:3000',]

sio = SocketManager(app=app, mount_location='/', cors_allowed_origins=[])

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.sio.on('connect_tables_restaurant')
def handle_connection(sid, *args, **kwargs):
    app.sio.enter_room(sid, args[0])


@app.sio.on('quest_table')
async def handle_quest_table(sid, *args, **kwargs):
    data = args[0]

    await app.sio.emit('new_quest', data['restaurant'], room=data['restaurant'])
    return


@app.sio.on('call_waitres')
async def call_waitres(sid, *args, **kwargs):
    data = args[0]

    await app.sio.emit('call_waitres', data['table'], room=data['restaurant'])
    return

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
