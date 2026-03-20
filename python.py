import pygame
import random
import math
import os

pygame.init()

WIDTH, HEIGHT = 900, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ULTRA REALISTIC SNAKE 🐍🔥")

clock = pygame.time.Clock()

# Colors
BLACK = (8, 8, 8)
GREEN = (0, 255, 140)
RED = (255, 70, 70)
WHITE = (220, 220, 220)

# Settings
speed = 3
radius = 8

font = pygame.font.SysFont("Arial", 25)

# High Score
def load_high_score():
    if not os.path.exists("highscore.txt"):
        return 0
    return int(open("highscore.txt").read())

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

# Snake 🐍
class Snake:
    def __init__(self):
        self.body = [(WIDTH//2, HEIGHT//2)]
        self.length = 80

        self.angle = 0
        self.target_angle = 0

        self.turn_speed = 0.08  # smooth turning
        self.wave_time = 0
        self.tongue_timer = 0

    def update_direction(self, dx, dy):
        if dx != 0 or dy != 0:
            self.target_angle = math.atan2(dy, dx)

    def move(self):
        # Smooth AI-like turning (LERP)
        diff = (self.target_angle - self.angle)
        diff = (diff + math.pi) % (2 * math.pi) - math.pi
        self.angle += diff * self.turn_speed

        head_x, head_y = self.body[-1]

        new_x = head_x + math.cos(self.angle) * speed
        new_y = head_y + math.sin(self.angle) * speed

        self.body.append((new_x, new_y))

        if len(self.body) > self.length:
            self.body.pop(0)

        self.wave_time += 0.3
        self.tongue_timer += 1

    def draw(self):
        # Draw body with advanced wave
        for i, (x, y) in enumerate(self.body):
            t = self.wave_time + i * 0.4

            offset = math.sin(t) * 6

            perp_angle = self.angle + math.pi / 2

            wave_x = x + math.cos(perp_angle) * offset
            wave_y = y + math.sin(perp_angle) * offset

            glow = int(255 * (i / len(self.body)))
            pygame.draw.circle(screen, (0, glow, 160), (int(wave_x), int(wave_y)), radius)

        # Head
        hx, hy = self.body[-1]
        pygame.draw.circle(screen, (0, 255, 200), (int(hx), int(hy)), radius+2)

        # Eyes 👀
        eye_offset = 4
        perp = self.angle + math.pi/2

        ex1 = hx + math.cos(perp)*eye_offset
        ey1 = hy + math.sin(perp)*eye_offset

        ex2 = hx - math.cos(perp)*eye_offset
        ey2 = hy - math.sin(perp)*eye_offset

        pygame.draw.circle(screen, WHITE, (int(ex1), int(ey1)), 3)
        pygame.draw.circle(screen, WHITE, (int(ex2), int(ey2)), 3)

        # Tongue 👅
        if self.tongue_timer % 50 < 10:
            tx = hx + math.cos(self.angle)*15
            ty = hy + math.sin(self.angle)*15
            pygame.draw.line(screen, RED, (hx, hy), (tx, ty), 2)
def draw_jungle_background(time):
    # Sky / dark base
    screen.fill((5, 20, 10))

    # Moving jungle layers
    for i in range(3):
        color = (10, 40 + i*30, 20)
        for x in range(0, WIDTH, 40):
            y = HEIGHT - 80 - i*40 + int(math.sin(time*0.02 + x*0.05)*10)
            pygame.draw.rect(screen, color, (x, y, 40, HEIGHT))

    # Trees 🌴
    for i in range(10):
        tx = (i * 90 + int(time*0.2)) % WIDTH
        pygame.draw.rect(screen, (60, 30, 10), (tx, HEIGHT-120, 10, 120))  # trunk
        pygame.draw.circle(screen, (20, 80, 20), (tx+5, HEIGHT-120), 30)   # leaves

    # Foreground grass 🌿
    for x in range(0, WIDTH, 15):
        height = random.randint(5, 15)
        pygame.draw.line(screen, (0, 100, 40), (x, HEIGHT), (x, HEIGHT-height), 2)
# Game
def game():
    snake = Snake()

    food_x = random.randint(50, WIDTH-50)
    food_y = random.randint(50, HEIGHT-50)

    score = 0
    high_score = load_high_score()

    running = True
    game_over = False

    while running:

        while game_over:
            draw_jungle_background(pygame.time.get_ticks())

            text = font.render("Press R to Restart | Q to Quit", True, RED)
            screen.blit(text, (250, HEIGHT//2))

            hs = font.render(f"High Score: {high_score}", True, WHITE)
            screen.blit(hs, (330, HEIGHT//2 + 40))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game()
                    if event.key == pygame.K_q:
                        running = False
                        game_over = False

        draw_jungle_background(pygame.time.get_ticks())

        dx, dy = 0, 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1

        snake.update_direction(dx, dy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        snake.move()

        hx, hy = snake.body[-1]

        # Food
        if math.hypot(hx - food_x, hy - food_y) < 10:
            food_x = random.randint(50, WIDTH-50)
            food_y = random.randint(50, HEIGHT-50)
            snake.length += 25
            score += 10

        # Wall
        if hx < 0 or hx > WIDTH or hy < 0 or hy > HEIGHT:
            if score > high_score:
                save_high_score(score)
            game_over = True

        pygame.draw.circle(screen, RED, (food_x, food_y), 6)

        snake.draw()

        sc = font.render(f"Score: {score}", True, WHITE)
        hs = font.render(f"High Score: {high_score}", True, WHITE)

        screen.blit(sc, (10, 10))
        screen.blit(hs, (10, 40))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

game()