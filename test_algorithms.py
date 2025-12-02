"""
Test script to verify the DFS maze generation and A* solving algorithms
without requiring pygame for visualization.
"""

import random
import heapq
import time

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Create grid - 0 for path, 1 for wall
        self.grid = [[1 for _ in range(width)] for _ in range(height)]
        self.start = (0, 0)
        self.end = (width - 1, height - 1)
        self.solution_path = []
    
    def is_valid(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_neighbors(self, x, y):
        neighbors = []
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Only consider cells 2 steps away
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny) and self.grid[ny][nx] == 1:
                neighbors.append((nx, ny))
        return neighbors
    
    def remove_wall(self, x1, y1, x2, y2):
        # Remove wall between two cells
        wall_x = (x1 + x2) // 2
        wall_y = (y1 + y2) // 2
        self.grid[y1][x1] = 0  # Current cell
        self.grid[wall_y][wall_x] = 0  # Wall between
    
    def generate_maze_dfs(self, start_x=1, start_y=1):
        """Generate maze using DFS algorithm"""
        stack = [(start_x, start_y)]
        visited = set()
        visited.add((start_x, start_y))
        
        # Make sure start and end are paths
        self.grid[start_y][start_x] = 0
        self.grid[self.height - 2][self.width - 2] = 0
        
        while stack:
            current_x, current_y = stack[-1]
            
            neighbors = self.get_neighbors(current_x, current_y)
            unvisited_neighbors = [n for n in neighbors if n not in visited]
            
            if unvisited_neighbors:
                next_x, next_y = random.choice(unvisited_neighbors)
                self.remove_wall(current_x, current_y, next_x, next_y)
                visited.add((next_x, next_y))
                stack.append((next_x, next_y))
            else:
                stack.pop()
        
        # Ensure the end point is properly connected to the maze
        # Force connection to an adjacent path if not already connected
        end_x, end_y = self.width - 2, self.height - 2
        if (end_x, end_y) not in visited:
            # Connect to an adjacent cell that is part of the maze
            directions = [(0, -2), (-2, 0), (0, 2), (2, 0)]  # Only even steps to connect to paths
            for dx, dy in directions:
                nx, ny = end_x + dx, end_y + dy
                if self.is_valid(nx, ny) and (nx, ny) in visited:
                    # Connect the end point to this visited neighbor
                    wall_x = (end_x + nx) // 2
                    wall_y = (end_y + ny) // 2
                    self.grid[end_y][end_x] = 0  # End point
                    self.grid[wall_y][wall_x] = 0  # Connecting wall
                    break
    
    def heuristic(self, pos1, pos2):
        """Manhattan distance heuristic"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_neighbors_astar(self, x, y):
        """Get valid neighbors for A* algorithm"""
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny) and self.grid[ny][nx] == 0:
                neighbors.append((nx, ny))
        return neighbors
    
    def solve_astar(self):
        """Solve maze using A* algorithm"""
        start = (1, 1)  # Start at top-left
        end = (self.width - 2, self.height - 2)  # End at bottom-right
        
        # Priority queue: (f_score, g_score, x, y)
        open_set = [(self.heuristic(start, end), 0, start[0], start[1])]
        closed_set = set()
        came_from = {}
        
        while open_set:
            f_score, g_score, x, y = heapq.heappop(open_set)
            
            if (x, y) == end:
                # Reconstruct path
                path = []
                current = (x, y)
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                self.solution_path = path
                return path
            
            if (x, y) in closed_set:
                continue
            
            closed_set.add((x, y))
            
            for nx, ny in self.get_neighbors_astar(x, y):
                if (nx, ny) in closed_set:
                    continue
                
                tentative_g_score = g_score + 1
                
                # Check if this path to neighbor is better
                found_better = False
                for item in open_set:
                    if item[2] == nx and item[3] == ny:
                        if tentative_g_score < item[1]:
                            found_better = True
                            break
                
                if not found_better:
                    new_f_score = tentative_g_score + self.heuristic((nx, ny), end)
                    heapq.heappush(open_set, (new_f_score, tentative_g_score, nx, ny))
                    came_from[(nx, ny)] = (x, y)
        
        return []  # No path found

def print_maze(maze, solution_path=None):
    """Print the maze to console"""
    path_set = set(solution_path) if solution_path else set()
    
    for y in range(maze.height):
        row = ""
        for x in range(maze.width):
            if (x, y) in path_set:
                row += "."
            elif maze.grid[y][x] == 1:  # Wall
                row += "#"
            else:  # Path
                row += " "
        print(row)

def main():
    print("Testing DFS Maze Generation and A* Solving Algorithms")
    print("=" * 50)
    
    # Create a small maze for testing
    maze = Maze(15, 11)  # Width, Height
    
    print("Original grid (before generation):")
    print_maze(maze)
    
    print("\nGenerating maze using DFS...")
    start_time = time.time()
    maze.generate_maze_dfs()
    gen_time = time.time() - start_time
    print(f"Maze generation completed in {gen_time:.4f} seconds")
    
    print("\nGenerated maze:")
    print_maze(maze)
    
    print("\nSolving maze using A*...")
    start_time = time.time()
    solution = maze.solve_astar()
    solve_time = time.time() - start_time
    print(f"Maze solving completed in {solve_time:.4f} seconds")
    
    if solution:
        print(f"\nSolution found! Path length: {len(solution)}")
        print("\nSolved maze with path marked by dots:")
        print_maze(maze, solution)
        
        print(f"\nPath coordinates: {solution[:10]}{'...' if len(solution) > 10 else ''}")
    else:
        print("\nNo solution found!")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    main()