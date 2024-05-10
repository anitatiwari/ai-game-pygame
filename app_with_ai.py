#!/opt/homebrew/bin/python3
import pygame
import random
from ai_bee import AIBee

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bee and Flowers")

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLACK = (0,0,0)

# Define the bee
bee_img = pygame.image.load('bee.png')  # Load bee image
bee_size = 50
bee_x = WIDTH // 2
bee_y = HEIGHT // 2
bee_speed = 5
bee_img = pygame.transform.scale(bee_img, (bee_size, bee_size))

# Define the bug
bug_img = pygame.image.load('bug.png')  # Load bug image
bug_size = 50
bug_x = random.randint(0, WIDTH - bug_size)
bug_y = random.randint(0, HEIGHT - bug_size)
bug_speed = 1
bug_img = pygame.transform.scale(bug_img, (bug_size, bug_size))


# Define flower
flower_img = pygame.image.load('flower.png')  # Load flower image
flower_size = 30
flowers = []
flower_img = pygame.transform.scale(flower_img, (flower_size, flower_size))


# Game variables
score = 0
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()
game_over = False

# Function to display score


# Function to check collision
def check_collision(x1, y1, x2, y2, size):
    if (x1 >= x2 and x1 < x2 + size) or (x2 >= x1 and x2 < x1 + size):
        if (y1 >= y2 and y1 < y2 + size) or (y2 >= y1 and y2 < y1 + size):
            return True
    return False



screen.fill(WHITE)
welcome_text = font.render("Press any key to start", True, BLACK)
screen.blit(welcome_text, (WIDTH // 2 - 150, HEIGHT // 2))
pygame.display.flip()

# Wait for any key press to start the game
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            waiting = False


grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
for flower in flowers:
    flower_x, flower_y = flower
    grid[flower_y][flower_x] = 1
    
ai_bee = AIBee(bee_x, bee_y, bee_size, bee_speed, grid)

def show_score():
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))
    ai_bee_score_text = font.render("AI Bee Score: " + str(ai_bee.score), True, WHITE)
    screen.blit(ai_bee_score_text, (10, 40))


# Main game loop
while not game_over:
    
    
    #ai_bee.grid = grid

        
    screen.fill((0, 0, 0))
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    # Move the bee
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and bee_x > bee_speed:
        bee_x -= bee_speed
    if keys[pygame.K_RIGHT] and bee_x < WIDTH - bee_size - bee_speed:
        bee_x += bee_speed
    if keys[pygame.K_UP] and bee_y > bee_speed:
        bee_y -= bee_speed
    if keys[pygame.K_DOWN] and bee_y < HEIGHT - bee_size - bee_speed:
        bee_y += bee_speed

    # Move the bug towards the bee
    if bee_x < bug_x:
        bug_x -= bug_speed
    elif bee_x > bug_x:
        bug_x += bug_speed
    if bee_y < bug_y:
        bug_y -= bug_speed
    elif bee_y > bug_y:
        bug_y += bug_speed
        
    for flower in flowers:
        flower_x, flower_y = flower
        ai_bee.update(flower_x, flower_y)
        
    screen.blit(bee_img, (ai_bee.x, ai_bee.y))


    # Check collision with bug
    if check_collision(bee_x, bee_y, bug_x, bug_y, bee_size):
        game_over = True

    # Check collision with flowers
    for flower in flowers:
        flower_x, flower_y = flower
        if check_collision(bee_x, bee_y, flower[0], flower[1], bee_size):
            flowers.remove(flower)
            score += 1
            # flower_sound = pygame.mixer.Sound('flower_sound.wav')
            # flower_sound.play()
        if check_collision(ai_bee.x, ai_bee.y, flower[0], flower[1], bee_size):
            flowers.remove(flower)
            ai_bee.score += 1
            
            
    
    
        
    #ai_bee.update_grid(grid)
    

    # Add new flowers
    if len(flowers) < 5:
        flower_x = random.randint(0, WIDTH - flower_size)
        flower_y = random.randint(0, HEIGHT - flower_size)
        flowers.append((flower_x, flower_y))

    # Draw the bee, bug, flowers, and score
    screen.blit(bee_img, (bee_x, bee_y))
    screen.blit(bug_img, (bug_x, bug_y))
    for flower in flowers:
        screen.blit(flower_img, flower)
    show_score()

    pygame.display.flip()
    clock.tick(30)
    

# Game over screen
screen.fill(RED)
game_over_text = font.render("Game Over!", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
final_score_text = font.render("Final Score: " + str(score), True, WHITE)
screen.blit(final_score_text, (WIDTH // 2 - 120, HEIGHT // 2))
pygame.display.flip()

# Wait for a moment before closing
pygame.time.wait(2000)
pygame.quit()
