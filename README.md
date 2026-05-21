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
