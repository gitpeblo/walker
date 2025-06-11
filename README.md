# walker

© 2025 Paolo Bonfini — All rights reserved.


**`walker`** is an interactive grid-based simulation environment built with `pygame`, designed as a lightweight gym for training and evaluating path-finding neural networks.

## Overview

This project provides a real-time, visual environment for experimenting with agent navigation over a procedurally generated tile map. It supports both manual controls and automatic path-following using A* as a baseline algorithm.

The environment is particularly suited for research in:
- Reinforcement learning
- Planning under partial observability
- Path-finding heuristics and algorithm benchmarking

## Features

- Procedural map generation
- Player navigation via keyboard input
- A* algorithm as baseline path-finder
- Toggleable command overlay panel
- Minimap for global context
- Visual feedback for path-finding and tile occupancy
- Easily extendable to neural policies or RL agents

## Project Goals

This project serves as a:
- **Training ground** for neural path-finding models
- **Testing framework** for evaluating traditional vs learned policies
- **Interactive demo** to visualize real-time agent decisions and map transitions

## Controls

| Key       | Action                          |
|-----------|---------------------------------|
| `ESC`     | Quit the game                   |
| `M`       | Generate a new map              |
| `E`       | Set an end point (via mouse)    |
| `TAB`     | Toggle command overlay panel    |

## Baseline: A* Pathfinding

The environment includes a reference implementation of the A* path-finding algorithm. The core logic is based on a `Node` class that evaluates the cost `f(n) = g(n) + h(n)` and navigates through a binary maze where `0` indicates walkable tiles.

### A* Highlights

- Uses Euclidean squared distance as heuristic (`h`)
- Expands to 8-connected neighbors (cardinal and diagonal)
- Skips impassable terrain (non-zero tiles)
- Returns the optimal path (if one exists) as a list of grid positions

### Example

```python
maze = [
    [1, 1, 1, 0, 0, ...],
    [0, 1, 1, 0, 0, ...],
    ...
]

start = (0, 0)
end = (7, 6)
path = astar(maze, start, end)
```

## Folder Structure

```
walker/
│
├── main.py                # Entry point and main game loop
├── src/
│   ├── world.py           # Map generation and tile structure
│   ├── player.py          # Player control and physics
│   ├── utils.py           # Coordinate transforms, collision checks
│   ├── commands_list.py   # Command overlay interface
│   ├── set_end_point.py   # Endpoint selector (mouse-based)
│   └── astar.py           # A* algorithm (baseline)
```

## Requirements

- Python ≥ 3.7  
- `pygame` ≥ 2.0  
- Tested on Linux and macOS

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## Notes

- This environment is **not** Gym-compatible out of the box, but can be wrapped.
- To plug in a neural agent, override `player.move()` with policy outputs.
- Paths found by A* are used as ground truth to benchmark learning-based policies.

## Acknowledgment

Special thanks to [DaFluffyPotato](https://www.youtube.com/@DaFluffyPotato) for his excellent tutorials on game development with Pygame.
