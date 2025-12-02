import pygame
import random
import heapq
import time
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 60

# Colors
BACKGROUND = (10, 10, 40)
WALL_COLOR = (200, 200, 200)
PATH_COLOR = (30, 30, 60)
START_COLOR = (0, 255, 0)
END_COLOR = (255, 0, 0)
VISITED_COLOR = (70, 70, 120)
CURRENT_COLOR = (255, 255, 0)
SOLUTION_PATH_COLOR = (255, 255, 100)
TEXT_COLOR = (255, 255, 255)

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Create grid - 0 for path, 1 for wall
        self.grid = [[1 for _ in range(width)] for _ in range(height)]
        self.start = (0, 0)
        self.end = (width - 1, height - 1)
        self.visited_dfs = set()
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
        self.visited_dfs = set()
        self.visited_dfs.add((start_x, start_y))
        
        # Make sure start and end are paths
        self.grid[start_y][start_x] = 0
        self.grid[self.height - 2][self.width - 2] = 0
        
        while stack:
            current_x, current_y = stack[-1]
            
            neighbors = self.get_neighbors(current_x, current_y)
            unvisited_neighbors = [n for n in neighbors if n not in self.visited_dfs]
            
            if unvisited_neighbors:
                next_x, next_y = random.choice(unvisited_neighbors)
                self.remove_wall(current_x, current_y, next_x, next_y)
                self.visited_dfs.add((next_x, next_y))
                stack.append((next_x, next_y))
            else:
                stack.pop()
        
        # Ensure the end point is properly connected to the maze
        # Force connection to an adjacent path if not already connected
        end_x, end_y = self.width - 2, self.height - 2
        if (end_x, end_y) not in self.visited_dfs:
            # Connect to an adjacent cell that is part of the maze
            directions = [(0, -2), (-2, 0), (0, 2), (2, 0)]  # Only even steps to connect to paths
            for dx, dy in directions:
                nx, ny = end_x + dx, end_y + dy
                if self.is_valid(nx, ny) and (nx, ny) in self.visited_dfs:
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

class MazeVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Generator & Solver - DFS & A*")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        self.small_font = pygame.font.SysFont(None, 20)
        
        # Create maze
        self.maze = Maze(GRID_WIDTH, GRID_HEIGHT)
        self.state = "generating"  # "generating", "solving", "solved"
        self.generation_complete = False
        self.solving_complete = False
        
        # For DFS visualization
        self.dfs_stack = [(1, 1)]
        self.dfs_visited = set([(1, 1)])
        self.maze.grid[1][1] = 0  # Mark start as path
        self.maze.grid[GRID_HEIGHT - 2][GRID_WIDTH - 2] = 0  # Mark end as path
        
        # For A* visualization
        self.astar_open_set = []
        self.astar_closed_set = set()
        self.astar_came_from = {}
        self.astar_path_found = False
        self.astar_current = None
        
    def draw(self):
        self.screen.fill(BACKGROUND)
        
        # Draw grid
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if self.maze.grid[y][x] == 1:  # Wall
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                    pygame.draw.rect(self.screen, (150, 150, 150), rect, 1)
                else:  # Path
                    pygame.draw.rect(self.screen, PATH_COLOR, rect)
                    pygame.draw.rect(self.screen, (60, 60, 90), rect, 1)
        
        # Draw DFS visualization if still generating
        if self.state == "generating":
            for x, y in self.dfs_visited:
                if (x, y) != (1, 1) and (x, y) != (GRID_WIDTH - 2, GRID_HEIGHT - 2):  # Don't color start/end
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, VISITED_COLOR, rect)
            
            if self.dfs_stack:
                current_x, current_y = self.dfs_stack[-1]
                rect = pygame.Rect(current_x * CELL_SIZE, current_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, CURRENT_COLOR, rect)
        
        # Draw A* visualization if solving
        elif self.state == "solving":
            # Draw open set (frontier)
            for _, _, x, y in self.astar_open_set:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (100, 150, 200), rect, 1)
            
            # Draw closed set (visited)
            for x, y in self.astar_closed_set:
                if (x, y) != (1, 1) and (x, y) != (GRID_WIDTH - 2, GRID_HEIGHT - 2):
                    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, (150, 100, 200), rect)
            
            # Draw current node being processed
            if self.astar_current:
                x, y = self.astar_current
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, CURRENT_COLOR, rect)
        
        # Draw solution path if found
        if self.state == "solved" and self.maze.solution_path:
            for x, y in self.maze.solution_path:
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, SOLUTION_PATH_COLOR, rect)
        
        # Draw start and end points
        start_rect = pygame.Rect(1 * CELL_SIZE, 1 * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        end_rect = pygame.Rect((GRID_WIDTH - 2) * CELL_SIZE, (GRID_HEIGHT - 2) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, START_COLOR, start_rect)
        pygame.draw.rect(self.screen, END_COLOR, end_rect)
        
        # Draw UI text
        if self.state == "generating":
            text = self.font.render("Generating Maze (DFS)...", True, TEXT_COLOR)
        elif self.state == "solving":
            text = self.font.render("Solving Maze (A*)...", True, TEXT_COLOR)
        else:
            text = self.font.render("Maze Solved!", True, TEXT_COLOR)
        
        self.screen.blit(text, (10, 10))
        
        # Draw instructions
        instructions = [
            "Press R to Reset and Regenerate",
            "Press SPACE to Toggle Auto-Solve",
            "Press S to Solve Manually"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, TEXT_COLOR)
            self.screen.blit(text, (10, HEIGHT - 60 + i * 20))
        
        pygame.display.flip()
    
    def generate_step(self):
        """Perform one step of maze generation"""
        if not self.dfs_stack:
            self.generation_complete = True
            self.state = "solving"
            self.setup_astar()
            return
        
        current_x, current_y = self.dfs_stack[-1]
        neighbors = self.maze.get_neighbors(current_x, current_y)
        unvisited_neighbors = [n for n in neighbors if n not in self.dfs_visited]
        
        if unvisited_neighbors:
            next_x, next_y = random.choice(unvisited_neighbors)
            self.maze.remove_wall(current_x, current_y, next_x, next_y)
            self.dfs_visited.add((next_x, next_y))
            self.dfs_stack.append((next_x, next_y))
        else:
            self.dfs_stack.pop()
    
    def setup_astar(self):
        """Setup A* algorithm"""
        start = (1, 1)
        end = (GRID_WIDTH - 2, GRID_HEIGHT - 2)
        heuristic = self.maze.heuristic(start, end)
        self.astar_open_set = [(heuristic, 0, start[0], start[1])]
        self.astar_closed_set = set()
        self.astar_came_from = {}
        self.astar_current = start
    
    def solve_step(self):
        """Perform one step of A* solving"""
        if not self.astar_open_set:
            self.solving_complete = True
            self.state = "solved"
            return
        
        f_score, g_score, x, y = heapq.heappop(self.astar_open_set)
        self.astar_current = (x, y)
        
        end = (GRID_WIDTH - 2, GRID_HEIGHT - 2)
        if (x, y) == end:
            # Reconstruct path
            path = []
            current = (x, y)
            while current in self.astar_came_from:
                path.append(current)
                current = self.astar_came_from[current]
            path.append((1, 1))
            path.reverse()
            self.maze.solution_path = path
            self.astar_path_found = True
            self.state = "solved"
            return
        
        if (x, y) in self.astar_closed_set:
            return
        
        self.astar_closed_set.add((x, y))
        
        for nx, ny in self.maze.get_neighbors_astar(x, y):
            if (nx, ny) in self.astar_closed_set:
                continue
            
            tentative_g_score = g_score + 1
            
            # Check if this node is already in open set with a better path
            found_better = False
            for item in self.astar_open_set:
                if item[2] == nx and item[3] == ny:
                    if tentative_g_score < item[1]:
                        found_better = True
                        break
            
            if not found_better:
                new_f_score = tentative_g_score + self.maze.heuristic((nx, ny), end)
                heapq.heappush(self.astar_open_set, (new_f_score, tentative_g_score, nx, ny))
                self.astar_came_from[(nx, ny)] = (x, y)
    
    def reset(self):
        """Reset the maze and visualization"""
        self.maze = Maze(GRID_WIDTH, GRID_HEIGHT)
        self.state = "generating"
        self.generation_complete = False
        self.solving_complete = False
        
        # Reset DFS visualization
        self.dfs_stack = [(1, 1)]
        self.dfs_visited = set([(1, 1)])
        self.maze.grid[1][1] = 0
        self.maze.grid[GRID_HEIGHT - 2][GRID_WIDTH - 2] = 0
        
        # Reset A* visualization
        self.astar_open_set = []
        self.astar_closed_set = set()
        self.astar_came_from = {}
        self.astar_path_found = False
        self.astar_current = None
    
    def solve_all(self):
        """Solve the entire maze at once"""
        if self.state == "generating":
            # Complete maze generation first
            while self.dfs_stack:
                self.generate_step()
            self.state = "solving"
        
        if self.state == "solving":
            # Run A* to completion
            while self.astar_open_set:
                self.solve_step()
                end = (GRID_WIDTH - 2, GRID_HEIGHT - 2)
                if self.astar_path_found or not self.astar_open_set:
                    break
            self.state = "solved"
    
    def run(self):
        running = True
        auto_solve = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_SPACE:
                        auto_solve = not auto_solve
                    elif event.key == pygame.K_s:
                        self.solve_all()
            
            # Update based on current state
            if self.state == "generating":
                self.generate_step()
            elif self.state == "solving":
                self.solve_step()
            elif auto_solve and self.state == "solved":
                self.reset()
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    visualizer = MazeVisualizer()
    visualizer.run()