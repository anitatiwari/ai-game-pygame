import pygame
import random
from queue import PriorityQueue

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 700, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bee and Flowers")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 100, 0)

# Load images
bee_img = pygame.image.load('bee.png')
ai_bee_img = pygame.image.load('ai_bee.png')  # Using the same image for simplicity
bug_img = pygame.image.load('bug.png')
flower_img = pygame.image.load('flower.png')

# Define the bees
bee_size = 50
bee_x, bee_y = WIDTH // 2, HEIGHT // 2
bee_speed = 5
bee_img = pygame.transform.scale(bee_img, (bee_size, bee_size))

# Define the AI bee
ai_bee_x, ai_bee_y = WIDTH // 3, HEIGHT // 3
ai_bee_img = pygame.transform.scale(ai_bee_img, (bee_size, bee_size))

# Define the bug
bug_size = 50
bug_x, bug_y = random.randint(0, WIDTH - bug_size), random.randint(0, HEIGHT - bug_size)
bug_speed = bee_speed  # Same as bee_speed for fair gameplay
bug_img = pygame.transform.scale(bug_img, (bug_size, bug_size))

# Define flowers
flower_size = 30
flowers = []
flower_img = pygame.transform.scale(flower_img, (flower_size, flower_size))

# Game variables
player_score = 0
ai_score = 0
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
game_over = False
GRID_SIZE = 5  # Size of the grid cell for pathfinding

# Define helper functions for A* and Dijkstra's Algorithms
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def dijkstra_search(start, goal, obstacles):
    frontier = PriorityQueue()
    frontier.put((0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current_cost, current = frontier.get()

        if current == goal:
            break

        for next in [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                     (current[0], current[1] + 1), (current[0], current[1] - 1)]:
            if 0 <= next[0] < WIDTH // GRID_SIZE and 0 <= next[1] < HEIGHT // GRID_SIZE:
                new_cost = current_cost + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost
                    frontier.put((priority, next))
                    came_from[next] = current
    return came_from

def a_star_search(start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in [(current[0] + 1, current[1]), (current[0] - 1, current[1]),
                     (current[0], current[1] + 1), (current[0], current[1] - 1)]:
            if 0 <= next[0] < WIDTH // GRID_SIZE and 0 <= next[1] < HEIGHT // GRID_SIZE:
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + heuristic(next, goal)
                    frontier.put(next, priority)
                    came_from[next] = current
    return came_from

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append((current[0] * GRID_SIZE, current[1] * GRID_SIZE))
        current = came_from[current]
    path.reverse()
    return path
# Define a variable to store the bug's path
bug_path = []

# Function to display score
def show_score(final=False):
    player_message = f"Player Score: {player_score}"
    ai_message = f"AI Score: {ai_score}"
    player_score_text = font.render(player_message, True, WHITE)
    ai_score_text = font.render(ai_message, True, RED)
    screen.blit(player_score_text, (10, 10))
    screen.blit(ai_score_text, (10, 40))
    if final:
        winner = "Player" if player_score > ai_score else "AI"
        winner_message = f"{winner} won!" if player_score != ai_score else "It's a tie!"
        winner_text = font.render(winner_message, True, WHITE)
        screen.blit(winner_text, (WIDTH // 2 - 100, HEIGHT // 2 + 40))

# Function to check collision
def check_collision(x1, y1, x2, y2, size):
    return (x1 < x2 + size and x1 + size > x2 and
            y1 < y2 + size and y1 + size > y2)
# Define a function to log AI behavior
def log_ai(message):
    print("[AI]:", message)

# Main game loop
def main():
    global bee_x, bee_y, ai_bee_x, ai_bee_y, bug_x, bug_y, flowers, player_score, ai_score, game_over
    game_over = False
    player_score = 0
    ai_score = 0
    flowers = []
    bee_x, bee_y = WIDTH // 2, HEIGHT // 2
    ai_bee_x, ai_bee_y = WIDTH // 3, HEIGHT // 3
    bug_x, bug_y = random.randint(0, WIDTH - bug_size), random.randint(0, HEIGHT - bug_size)
    path = []
    ai_path = []

    while not game_over:
        screen.fill(GREEN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True  # Quit the entire game

        # Handle bee movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and bee_x > bee_speed:
            bee_x -= bee_speed
        if keys[pygame.K_RIGHT] and bee_x < WIDTH - bee_size:
            bee_x += bee_speed
        if keys[pygame.K_UP] and bee_y > bee_speed:
            bee_y -= bee_speed
        if keys[pygame.K_DOWN] and bee_y < HEIGHT - bee_size:
            bee_y += bee_speed

        # Update bug's path and move bug
        if not path or random.randint(0, 50) == 0:
            came_from = a_star_search((bug_x // GRID_SIZE, bug_y // GRID_SIZE), (bee_x // GRID_SIZE, bee_y // GRID_SIZE))
            path = reconstruct_path(came_from, (bug_x // GRID_SIZE, bug_y // GRID_SIZE), (bee_x // GRID_SIZE, bee_y // GRID_SIZE))
        log_ai(f"Bug's path: {path}")
        # Update bug's path
        bug_path = path[:]
        if path:
            bug_x, bug_y = path.pop(0)

        # AI bee movement
        if not ai_path and flowers:
            # Find the nearest flower
            nearest_flower = min(flowers, key=lambda f: heuristic((ai_bee_x // GRID_SIZE, ai_bee_y // GRID_SIZE), (f[0] // GRID_SIZE, f[1] // GRID_SIZE)))
            came_from = dijkstra_search((ai_bee_x // GRID_SIZE, ai_bee_y // GRID_SIZE), (nearest_flower[0] // GRID_SIZE, nearest_flower[1] // GRID_SIZE), [])
            ai_path = reconstruct_path(came_from, (ai_bee_x // GRID_SIZE, ai_bee_y // GRID_SIZE), (nearest_flower[0] // GRID_SIZE, nearest_flower[1] // GRID_SIZE))
        if ai_path:
            ai_bee_x, ai_bee_y = ai_path.pop(0)

        # Check for collisions
        if check_collision(bee_x, bee_y, bug_x, bug_y, bee_size):
            game_over = True

        # Manage flower interactions
        for flower in flowers[:]:
            if check_collision(bee_x, bee_y, flower[0], flower[1], flower_size):
                flowers.remove(flower)
                player_score += 1
            elif check_collision(ai_bee_x, ai_bee_y, flower[0], flower[1], flower_size):
                flowers.remove(flower)
                ai_score += 1

        # Add new flowers
        if len(flowers) < 5:
            flower_x = random.randint(0, WIDTH - flower_size)
            flower_y = random.randint(0, HEIGHT - flower_size)
            flowers.append((flower_x, flower_y))

         # Draw bug's path
        if bug_path:
            for i in range(len(bug_path) - 1):
                x1, y1 = bug_path[i]
                x2, y2 = bug_path[i + 1]
                pygame.draw.line(screen, RED, (x1, y1), (x2, y2), 2)

        # Draw elements
        screen.blit(bee_img, (bee_x, bee_y))
        screen.blit(ai_bee_img, (ai_bee_x, ai_bee_y))
        screen.blit(bug_img, (bug_x, bug_y))
        for flower in flowers:
            screen.blit(flower_img, (flower[0], flower[1]))
        show_score()
        pygame.display.flip()
        clock.tick(30)

    # Game over screen
    screen.fill(BLACK)
    show_score(final=True)
    pygame.display.flip()
    pygame.time.wait(2000)  # Display the final score for 2 seconds

    # Wait for restart or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True  # Quit the entire game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return False  # Restart the game
                elif event.key == pygame.K_q:
                    return True  # Quit the game

# Run the game loop until the user decides to quit
while True:
    if main():
        break

pygame.quit()
