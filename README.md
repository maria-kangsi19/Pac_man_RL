# Pacman Q-learning

A small browser game where Pacman learns to eat pellets and avoid a ghost using Q-learning. It is a single `index.html` file with no libraries and no install.

## How to run

Open `index.html` in a browser. That's it.

When the page loads it trains for 60,000 games first, so the page freezes for a few seconds. After that you can watch Pacman play using what it learned. Win rates during training are printed in the browser console (F12 -> Console).

The game is not pretrained. Every page load starts from scratch, so results can differ a little each time.

## How the game works

- The board is a 10x10 grid.
- Pacman starts at the top left and the ghost at the bottom right.
- There are 6 pellets on the board.
- The ghost moves randomly.
- The game ends when Pacman eats every pellet (win), the ghost catches Pacman (loss), or 120 steps pass.

### Rewards

| Event | Reward |
|-------|--------|
| Every step | -1 |
| Eating a pellet | +10 |
| Eating the last pellet | +50 |
| Getting caught by the ghost | -50 |

## How the learning works

Pacman keeps a table (the Q-table) with a score for each of the 4 moves in every situation it has seen. After each move it updates the score:

```
new score = old score + ALPHA * (reward + GAMMA * best next score - old score)
```

Settings used:

- `ALPHA = 0.1` (learning rate)
- `GAMMA = 0.95` (how much future rewards matter)
- epsilon starts at 1 and drops to 0.05, so Pacman tries random moves at first and then relies on what it learned

## Files

- `index.html` - the whole project (game, training and drawing)
- `README.md` - this file

## Ideas to try

- Change `train(60000)` to a bigger or smaller number and see how the win rate changes
- Change the rewards and see how Pacman's behaviour changes
- Save the Q-table so the game doesn't need to train every time
