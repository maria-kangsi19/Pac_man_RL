# Pac-Man RL

A tiny Pac-Man game where the agent learns to play using Q-learning (no neural network).

## Run it

```bash
pip install pygame
python pacman_simple.py
```

Trains for a few minutes, prints the win rate as it learns, then opens a window showing
the trained agent play. Use `--no-gui` to skip the window.

## How it works

- `SIZE = 10`: a 10x10 grid with fixed pellet positions and a randomly-moving ghost.
- A Q-table (`Q[state] -> [4 numbers]`) stores how good each move looks in each situation.
- The core learning rule: `Q(s,a) += ALPHA * (target - Q(s,a))`, where
  `target = reward + GAMMA * best future Q-value`.
- Epsilon-greedy exploration: starts mostly random, shifts to mostly best-known moves.

See the comments in `pacman_simple.py` for a full walkthrough.
