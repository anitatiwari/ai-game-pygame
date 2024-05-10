import heapq
import math

class AIBee:
    def __init__(self, x, y, size, speed, grid):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.score = 0
        self.grid = grid
        
    def update_grid(self,grid_):
        self.grid = grid_

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            self.x += int(dx / distance * self.speed)
            self.y += int(dy / distance * self.speed)

    def find_path(self, target_x, target_y):
        open_list = [(0, (self.x, self.y))]
        heapq.heapify(open_list)
        came_from = {}
        cost_so_far = {(self.x, self.y): 0}

        while open_list:
            current_cost, (current_x, current_y) = heapq.heappop(open_list)

            if (current_x, current_y) == (target_x, target_y):
                break

            for next_x, next_y in self.neighbors(current_x, current_y):
                new_cost = cost_so_far[(current_x, current_y)] + 1
                if (next_x, next_y) not in cost_so_far or new_cost < cost_so_far[(next_x, next_y)]:
                    cost_so_far[(next_x, next_y)] = new_cost
                    priority = new_cost + self.heuristic(next_x, next_y, target_x, target_y)
                    heapq.heappush(open_list, (priority, (next_x, next_y)))
                    came_from[(next_x, next_y)] = (current_x, current_y)

        path = []
        current = (target_x, target_y)
        while current != (self.x, self.y):
            path.append(current)
            current = came_from[current]
        return path

    def neighbors(self, x, y):
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x = x + dx
                new_y = y + dy
                if 0 <= new_x < len(self.grid[0]) and 0 <= new_y < len(self.grid) and self.grid[new_y][new_x] != 1:
                    neighbors.append((new_x, new_y))
        return neighbors

    def heuristic(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def update(self, target_x, target_y):
        path = self.find_path(target_x, target_y)
        if path:
            next_x, next_y = path[-1]
            self.move_towards(next_x, next_y)
