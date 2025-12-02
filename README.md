# Maze Generator and Solver

This program generates mazes using Depth-First Search (DFS) and solves them using the A* algorithm, with visualization using Pygame.

## Features

- **Maze Generation**: Uses DFS algorithm to create a random maze
- **Maze Solving**: Uses A* algorithm to find the shortest path from start to end
- **Visualization**: Shows the generation and solving process in real-time
- **Interactive Controls**: Keyboard controls to reset, solve, and auto-run

## Requirements

- Python 3.6+
- Pygame

## Installation

```bash
pip install pygame
```

## How to Run

```bash
python maze_generator_solver.py
```

## Controls

- `R`: Reset and regenerate the maze
- `SPACE`: Toggle auto-solve mode (continuously generate and solve)
- `S`: Solve the current maze immediately
- `ESC` or close window: Exit the program

## Algorithm Details

### DFS Maze Generation
- Starts from a random cell
- Uses a stack to keep track of the path
- Randomly explores unvisited neighbors
- Creates paths by removing walls between cells
- Results in a maze with long, winding corridors

### A* Pathfinding
- Uses Manhattan distance as the heuristic
- Maintains open and closed sets to track nodes
- Finds the shortest path from start to end
- Guarantees optimal solution

## Visual Elements

- **White/Gray**: Walls
- **Dark Blue**: Paths
- **Green**: Start point
- **Red**: End point
- **Yellow**: Current cell during generation/solving
- **Light Blue**: A* open set (frontier)
- **Purple**: A* closed set (visited)
- **Yellow-Gold**: Solution path

## File Structure

- `maze_generator_solver.py`: Main program with both algorithms and visualization
- `README.md`: This file

## Customization

You can adjust the constants at the top of the Python file:
- `WIDTH`, `HEIGHT`: Window size
- `CELL_SIZE`: Size of each cell in pixels
- Colors: Various color constants for visualization