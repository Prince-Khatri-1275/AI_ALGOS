# Maze Generator and Solver Solution

## Overview

This project implements a complete maze generator and solver with visualization using Pygame. The program demonstrates two important algorithms:

1. **Depth-First Search (DFS)** for maze generation
2. **A* algorithm** for pathfinding

## Files Created

### 1. maze_generator_solver.py
Main program that:
- Generates mazes using DFS algorithm
- Solves mazes using A* algorithm
- Visualizes both processes in real-time with Pygame
- Provides interactive controls for user interaction

### 2. test_algorithms.py
Test script that:
- Verifies the core algorithms work without requiring Pygame
- Demonstrates maze generation and solving in console
- Shows the maze with ASCII characters

### 3. README.md
Documentation file with:
- Installation instructions
- Usage guide
- Algorithm explanations
- Controls reference

## Algorithm Details

### DFS Maze Generation
- Uses a stack-based approach to explore the maze
- Starts from a cell and randomly explores unvisited neighbors
- Carves paths by removing walls between cells
- Creates a perfect maze (exactly one path between any two points)

### A* Pathfinding
- Uses Manhattan distance as the heuristic function
- Maintains open and closed sets to track nodes
- Guarantees the shortest path solution
- Efficiently explores the most promising paths first

## Features

- Real-time visualization of maze generation and solving
- Color-coded representation of different states
- Interactive controls (reset, solve, auto-run)
- Efficient algorithms with good performance

## Requirements

- Python 3.6+
- Pygame library

## How to Run

```bash
pip install pygame
python maze_generator_solver.py
```

Note: The program requires a graphical display environment to run.

## Controls

- `R`: Reset and regenerate the maze
- `SPACE`: Toggle auto-solve mode
- `S`: Solve the current maze immediately
- Close window to exit

## Visualization Colors

- **White/Gray**: Walls
- **Dark Blue**: Paths
- **Green**: Start point
- **Red**: End point
- **Yellow**: Current cell during generation/solving
- **Light Blue**: A* open set (frontier)
- **Purple**: A* closed set (visited)
- **Yellow-Gold**: Solution path

## Algorithm Complexity

- **DFS Generation**: O(n×m) time complexity, where n and m are maze dimensions
- **A* Solving**: O(b^d) in the worst case, where b is the branching factor and d is the depth, but typically much better with a good heuristic

## Key Improvements Made

1. Fixed connection issue to ensure start and end points are always connected
2. Implemented proper visualization of algorithm states
3. Added interactive controls for user experience
4. Included comprehensive documentation

This solution provides a complete educational tool for understanding both maze generation and pathfinding algorithms.