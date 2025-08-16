from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

app = FastAPI()
players = []

class PlayerInput(BaseModel):
    player_name: str

class StageAnswer(BaseModel):
    player_name: str

class Player:
    def __init__(self, player_name: str):
        self.name = player_name
        self.joined = datetime.now()
        self.ended = None
        self.last_update = datetime.now()
        self.progress = 0
        self.completed = False

    def update_progress(self):
        self.last_update = datetime.now()
        self.progress += 1

    def complete_game(self):
        self.completed = True
        self.ended = datetime.now()
        self.last_update = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "joined": self.joined.isoformat(),
            "ended": self.ended.isoformat() if self.ended else None,
            "last_update": self.last_update.isoformat(),
            "progress": self.progress,
            "completed": self.completed,
            "completion_time": (self.ended - self.joined).total_seconds() if self.ended else None
        }

def find_player(player_name: str) -> Player:
    """Find a player by name"""
    for player in players:
        if player.name.lower() == player_name.lower():
            return player
    raise HTTPException(status_code=404, detail="Player not found")

@app.get("/players")
def get_players():
    """Get all players with their current status"""
    return [player.to_dict() for player in players]

@app.post("/start")
def start_game(player: PlayerInput):
    """Start a new game for a player"""
    # Check if player already exists
    for existing_player in players:
        if existing_player.name.lower() == player.player_name.lower():
            raise HTTPException(status_code=400, detail="Player already exists")

    new_player = Player(player.player_name)
    players.append(new_player)
    return {"clue": "I go up but never come down, though I have no legs to walk around."}

@app.post("/age")
def stage_2(answer: StageAnswer):
    """Stage 2: Check answer and provide next clue"""
    player = find_player(answer.player_name)

    if player.progress != 0:
        raise HTTPException(status_code=400, detail="Player not at correct stage")

    player.update_progress()
    return {"clue": "I eat all I'm given, no teeth in sight, the more I eat, the bigger and bright."}

@app.post("/fire")
def stage_3(answer: StageAnswer):
    """Stage 3: Check answer and provide next clue"""
    player = find_player(answer.player_name)

    if player.progress != 1:
        raise HTTPException(status_code=400, detail="Player not at correct stage")

    player.update_progress()
    return {"clue": "The more you share me, the less I stay, but I can still make your friend's day."}

@app.post("/secrets")
def final_stage(answer: StageAnswer):
    """Final stage: Check answer and complete the game"""
    player = find_player(answer.player_name)

    if player.progress != 2:
        raise HTTPException(status_code=400, detail="Player not at correct stage")

    if player.completed:
        raise HTTPException(status_code=400, detail="Player has already completed the game")

    player.complete_game()
    # player.ended is guaranteed to be set after complete_game()
    assert player.ended is not None
    completion_time = (player.ended - player.joined).total_seconds()
    return {
        "message": "You won!",
        "completion_time_seconds": completion_time,
        "completed_at": player.ended.isoformat()
    }

@app.get("/leaderboard")
def get_leaderboard():
    """Get leaderboard of completed players sorted by completion time"""
    completed_players = [p for p in players if p.completed]

    # Sort by completion time (fastest first)
    leaderboard = sorted(completed_players,
                        key=lambda p: (p.ended - p.joined).total_seconds() if p.ended else float('inf'))

    leaderboard_data = []
    for rank, player in enumerate(leaderboard, 1):
        # Completed players should always have ended timestamp
        assert player.ended is not None
        completion_time = (player.ended - player.joined).total_seconds()
        leaderboard_data.append({
            "rank": rank,
            "name": player.name,
            "completion_time_seconds": completion_time,
            "completion_time_formatted": f"{int(completion_time // 60)}m {int(completion_time % 60)}s",
            "completed_at": player.ended.isoformat()
        })

    return {
        "leaderboard": leaderboard_data,
        "total_completed": len(completed_players),
        "total_players": len(players)
    }

@app.get("/player/{player_name}/status")
def get_player_status(player_name: str):
    """Get detailed status for a specific player"""
    player = find_player(player_name)
    return player.to_dict()

@app.get("/stats")
def get_game_stats():
    """Get general game statistics"""
    total_players = len(players)
    completed_players = len([p for p in players if p.completed])
    active_players = len([p for p in players if not p.completed])

    if completed_players > 0:
        completion_times = []
        for p in players:
            if p.completed and p.ended is not None:
                completion_times.append((p.ended - p.joined).total_seconds())

        if completion_times:
            avg_completion_time = sum(completion_times) / len(completion_times)
            fastest_time = min(completion_times)
        else:
            avg_completion_time = None
            fastest_time = None
    else:
        avg_completion_time = None
        fastest_time = None

    return {
        "total_players": total_players,
        "completed_players": completed_players,
        "active_players": active_players,
        "completion_rate": f"{(completed_players/total_players)*100:.1f}%" if total_players > 0 else "0%",
        "average_completion_time_seconds": avg_completion_time,
        "fastest_completion_time_seconds": fastest_time
    }
