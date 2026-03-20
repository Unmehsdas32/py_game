import pygame
import random
import sys
import os

pygame.init()

# Screen
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultra Flappy Bird Jungle")

clock = pygame.time.Clock()
FPS = 60

# Colors
SKY = (120, 200, 255)
GROUND_COLOR = (200, 170, 120)
PIPE_COLOR = (20, 180, 20)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,50,50)

# Bird (SLOW + SMOOTH)
bird_x = 80
bird_y = HEIGHT // 2
velocity = 0
gravity = 0.35
jump_power = -6.5

# Animation
wing_state = 0
wing_timer = 0

# Pipes
pipe_width = 70
gap = 170
pipe_speed = 2.2
pipes = []

# Ground
ground_y = HEIGHT - 80

# Score
score = 0
high_score = 0

font = pygame.font.SysFont("Arial", 28)
big_font = pygame.font.SysFont("Arial", 40)

# Game state
game_over = False

# Load high score
if os.path.exists("flappy.txt"):
    with open("highscore.txt", "r") as f:
        try:
            high_score = int(f.read())
        except:
            high_score = 0

# 🌿 Bamboo particles
particles = []

def add_particles(x, y):
    for _ in range(2):
        particles.append([
            x, y,
            random.uniform(-0.5, 0.5),
            random.uniform(0.5, 1.5),
            random.randint(4,8)
        ])

def update_particles():
    for p in particles:
        p[0] += p[2]
        p[1] += p[3]
        p[4] -= 0.15
    return [p for p in particles if p[4] > 0]

def draw_bamboo_particles():
    for p in particles:
        x, y, vx, vy, size = p

        # bamboo body
        pygame.draw.rect(screen, (34,139,34),
                         (int(x), int(y), int(size/2), int(size*2)))

        # bamboo joints
        pygame.draw.line(screen, (0,100,0),
                         (int(x), int(y + size)),
                         (int(x + size/2), int(y + size)), 2)

# Save high score
def save_highscore():
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))

# Create pipes
def create_pipe():
    height = random.randint(120, 380)
    return {
        "top": pygame.Rect(WIDTH, 0, pipe_width, height),
        "bottom": pygame.Rect(WIDTH, height + gap, pipe_width, HEIGHT),
        "passed": False
    }

# Draw bird
def draw_bird(x, y, vel):
    angle = max(-30, min(30, -vel * 3))
    surf = pygame.Surface((40,40), pygame.SRCALPHA)

    pygame.draw.circle(surf, (255,255,0), (20,20), 15)

    # wing animation
    pygame.draw.ellipse(surf, (255,200,0),
                        (5, 15 + wing_state*5, 20, 10))

    # eye
    pygame.draw.circle(surf, WHITE, (25,15), 5)
    pygame.draw.circle(surf, BLACK, (25,15), 2)

    # beak
    pygame.draw.polygon(surf, (255,150,0),
                        [(30,20),(40,25),(30,30)])

    rotated = pygame.transform.rotate(surf, angle)
    rect = rotated.get_rect(center=(x,y))
    screen.blit(rotated, rect)

# Pipes
def draw_pipes():
    for p in pipes:
        pygame.draw.rect(screen, PIPE_COLOR, p["top"])
        pygame.draw.rect(screen, PIPE_COLOR, p["bottom"])

def move_pipes():
    for p in pipes:
        p["top"].x -= pipe_speed
        p["bottom"].x -= pipe_speed
    return [p for p in pipes if p["top"].x > -pipe_width]

# Collision
def check_collision(rect):
    if rect.top <= 0 or rect.bottom >= ground_y:
        return True
    for p in pipes:
        if rect.colliderect(p["top"]) or rect.colliderect(p["bottom"]):
            return True
    return False

# Reset
def reset():
    global bird_y, velocity, pipes, score, game_over, high_score

    if score > high_score:
        high_score = score
        save_highscore()

    bird_y = HEIGHT // 2
    velocity = 0
    pipes.clear()
    score = 0
    game_over = False

# Buttons
def draw_buttons():
    restart_btn = pygame.Rect(100, 300, 200, 50)
    quit_btn = pygame.Rect(100, 380, 200, 50)

    pygame.draw.rect(screen, (0,200,0), restart_btn)
    pygame.draw.rect(screen, RED, quit_btn)

    screen.blit(font.render("Restart", True, BLACK), (150, 310))
    screen.blit(font.render("Quit", True, WHITE), (170, 390))

    return restart_btn, quit_btn

# Game loop
spawn_timer = 0
running = True

while running:
    clock.tick(FPS)
    screen.fill(SKY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_highscore()
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                velocity = jump_power

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = pygame.mouse.get_pos()
            restart_btn, quit_btn = draw_buttons()

            if restart_btn.collidepoint(mouse_pos):
                reset()
            elif quit_btn.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()

    if not game_over:
        # Physics
        velocity += gravity
        bird_y += velocity

        bird_rect = pygame.Rect(bird_x-15, int(bird_y-15), 30, 30)

        # Wing animation
        wing_timer += 1
        if wing_timer > 8:
            wing_state = (wing_state + 1) % 3
            wing_timer = 0

        # Pipes
        spawn_timer += 1
        if spawn_timer > 110:
            pipes.append(create_pipe())
            spawn_timer = 0

        pipes = move_pipes()

        # Score
        for p in pipes:
            if not p["passed"] and p["top"].x < bird_x:
                score += 1
                p["passed"] = True

        # Particles 🌿
        add_particles(bird_x, bird_y)
        particles[:] = update_particles()

        # Draw
        draw_pipes()
        draw_bamboo_particles()
        draw_bird(bird_x, bird_y, velocity)

        # Collision
        if check_collision(bird_rect):
            game_over = True

    else:
        # Game Over screen
        screen.blit(big_font.render("GAME OVER", True, BLACK), (90, 200))
        restart_btn, quit_btn = draw_buttons()

    # Ground
    pygame.draw.rect(screen, GROUND_COLOR, (0, ground_y, WIDTH, 80))

    # Score
    screen.blit(font.render(f"Score: {score}", True, BLACK), (10,10))
    screen.blit(font.render(f"High: {high_score}", True, BLACK), (10,40))

    pygame.display.update()