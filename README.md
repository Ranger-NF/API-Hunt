


<img width="1920" height="1080" alt="nasahub" src="https://github.com/user-attachments/assets/e8544200-f902-41ee-a2f2-7375cad5043d" />

# 🏆 API Hunt - Interactive Riddle Challenge
**API Hunt** is an engaging treasure hunt game that challenges developers to solve riddles and navigate through API endpoints. Race against time, solve cryptic clues, and climb the leaderboard in this unique puzzle game!

## 🎯 Features

- **🧩 Multi-stage riddle challenges** - Solve cryptic clues to find the next endpoint
- **⏱️ Real-time leaderboard** - Compete with other players based on completion time
- **🔒 Sequential progression** - Must complete stages in order, no skipping allowed
- **📊 Player statistics** - Track your progress and game statistics
- **🚀 RESTful API design** - Clean, well-structured endpoints
- **⚡ Fast and lightweight** - Built with FastAPI for optimal performance


## product walkthrough

[![Watch the video](docs/logo.jpeg)](https://github.com/user-attachments/assets/4232d6ea-1c19-4133-bd2e-5ff30cb7a7ba)

## 🎮 How to Play


### 1. Start Your Adventure
```bash
POST /start
{
  "player_name": "YourPlayerName"
}
```

### 2. Follow the Clues
Each successful stage gives you a new riddle. Solve it to find the next endpoint!

**Example Flow:**
- **Stage 1**: `POST /answer1` with your answer
- **Stage 2**: `POST /answer2` with your answer
...

### 3. Submit Your Answers
```bash
POST /{endpoint}
{
  "player_name": "YourPlayerName"
}
```

### 4. Win and Celebrate! 🎉
Complete all stages to win and see your completion time!

## Libraries used
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation and settings
- **[Uvicorn](https://www.uvicorn.org/)** - ASGI web server

## How to configure

### Prerequisites
- Python 3.7+
- pip package manager

### Installation & Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/Ranger-NF/API-Hunt.git
   cd API-Hunt
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi uvicorn
   ```

## How to Run
1. **Run the game server**
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the game**
   - API Documentation: http://localhost:8000/docs
   - Game Endpoints: http://localhost:8000/


## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/start` | POST | Begin the game with your player name |
| `/age` | POST | First riddle stage |
| `/fire` | POST | Second riddle stage |
| `/secrets` | POST | Final challenge |
| `/leaderboard` | GET | View top players by completion time |
| `/players` | GET | List all players and their status |
| `/player/{name}/status` | GET | Get specific player details |
| `/stats` | GET | Overall game statistics |
