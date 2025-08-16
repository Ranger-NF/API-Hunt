from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

players = []

class PlayerInput(BaseModel):
    name: str

class Player():
    name: str
    joined: datetime
    ended: datetime | None = None
    progress: int = 0
    completed: bool = False

    def __init__(self, player_name: str):
        self.name = player_name
        self.joined = datetime.now()
        self.progress = 0
        self.completed = False

@app.get("/players")
def get_players():
    return players

@app.post("/start")
def start_game(player: PlayerInput):
    new_player = Player(player.name)
    players.append(new_player)
    return {"clue": "I go up but never come down, though I have no legs to walk around."}

@app.get("/age")
def clue_1():
    return {"clue": "I eat all I’m given, no teeth in sight, the more I eat, the bigger and bright."}

@app.get("/fire")
def clue_2():
    return {"clue": "The more you share me, the less I stay, but I can still make your friend’s day."}
# secrets
