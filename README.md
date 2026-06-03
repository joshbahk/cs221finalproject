# Cambio CS221 Final Project

This project models Cambio as a hidden-information stochastic game. We implement a two-player Cambio simulator, generate self-play data from bots, and compare baseline agents against an information-set Monte Carlo planning agent.

The simulator tracks the full true game state, while agents only receive observations containing the cards they are allowed to know.

## Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
PYTHONPATH=src python3 -m pytest
```

Play against the placeholder random bot in the terminal:

```bash
PYTHONPATH=src python3 -m cambio.cli
```

## Running the Project

To run the project locally, open two terminal windows from the project root directory.

### Backend

Start the FastAPI backend server:

```bash
uvicorn web.backend.server:app --reload
```

### Frontend

In a second terminal, start the React frontend:

```bash
cd web/frontend
npm install
npm run dev
```

> Note: `npm install` is only required the first time you set up the project.

### Accessing the Application

Once both servers are running, open the URL displayed by Vite in your browser (typically `http://localhost:5173`).

The frontend will communicate with the FastAPI backend running locally.

