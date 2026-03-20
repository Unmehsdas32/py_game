import pygame
import random
import sys
import math

pygame.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fixed Car Racing")

clock = pygame.time.Clock()

WHITE = (255,255,255)
GRAY = (40,40,40)
RED = (220,50,50)
BLUE = (50,150,255)
BLACK = (0,0,0)
YELLOW = (255,220,0)

MENU, PLAYING, GAME_OVER = 0,1,2
state = MENU

player_x = WIDTH//2
player_y = HEIGHT - 120
player_speed = 0
max_speed = 7
angle = 0

enemy_x = random.randint(60, WIDTH-60)
enemy_y = -100
enemy_speed = 6

shake = 0
time = 0
score = 0
font = pygame.font.SysFont(None, 40)

def reset():
    global player_x, player_y, enemy_x, enemy_y, score, player_speed, angle
    player_x = WIDTH//2
    player_y = HEIGHT - 120
    enemy_x = random.randint(60, WIDTH-60)
    enemy_y = -100
    score = 0
    player_speed = 1   # 🔥 FIX: start with small speed
    angle = 0

def draw_text(text, x, y, color=WHITE):
    t = font.render(text, True, color)
    screen.blit(t, (x,y))

def draw_road(offset):
    screen.fill(GRAY)
    for i in range(-40, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 5, i + offset, 10, 20))
    pygame.draw.rect(screen, YELLOW, (0, 0, 5, HEIGHT))
    pygame.draw.rect(screen, YELLOW, (WIDTH-5, 0, 5, HEIGHT))

def draw_car(surface, x, y, color, angle):
    car = pygame.Surface((60, 100), pygame.SRCALPHA)
    pygame.draw.rect(car, color, (10, 20, 40, 60), border_radius=10)
    pygame.draw.rect(car, (180,200,255), (15, 25, 30, 25), border_radius=6)
    pygame.draw.rect(car, BLACK, (5, 25, 8, 20))
    pygame.draw.rect(car, BLACK, (47, 25, 8, 20))
    pygame.draw.rect(car, BLACK, (5, 60, 8, 20))
    pygame.draw.rect(car, BLACK, (47, 60, 8, 20))

    rotated = pygame.transform.rotate(car, angle)
    rect = rotated.get_rect(center=(x,y))
    surface.blit(rotated, rect)

def menu():
    screen.fill(BLACK)
    draw_text("CAR RACING", 110, 200)
    draw_text("ENTER = Start", 90, 300)

def game_over():
    screen.fill(BLACK)
    draw_text("GAME OVER", 100, 200, RED)
    draw_text("Score: " + str(score), 130, 260)
    draw_text("R = Restart", 100, 320)

reset()

while True:
    clock.tick(60)
    time += 0.1

    offset_x = random.randint(-shake, shake)
    offset_y = random.randint(-shake, shake)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    reset()
                    state = PLAYING

        elif state == GAME_OVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset()
                    state = PLAYING

    if state == MENU:
        menu()

    elif state == PLAYING:
        keys = pygame.key.get_pressed()

        # Speed control
        if keys[pygame.K_UP]:
            player_speed += 0.25
        else:
            player_speed -= 0.1

        player_speed = max(1.5, min(player_speed, max_speed))  # 🔥 FIX: minimum speed

        # Steering (independent feel)
        steer_speed = max(3, player_speed)  # 🔥 FIX

        if keys[pygame.K_LEFT]:
            player_x -= steer_speed
            angle = 10
        elif keys[pygame.K_RIGHT]:
            player_x += steer_speed
            angle = -10
        else:
            angle *= 0.9

        player_x = max(40, min(WIDTH-40, player_x))

        # Enemy
        enemy_y += enemy_speed
        if enemy_y > HEIGHT:
            enemy_y = -100
            enemy_x = random.randint(60, WIDTH-60)
            score += 1

        # Collision
        player_rect = pygame.Rect(player_x-25, player_y-40, 50, 80)
        enemy_rect = pygame.Rect(enemy_x-25, enemy_y-40, 50, 80)

        if player_rect.colliderect(enemy_rect):
            shake = 12
            state = GAME_OVER

        wave = math.sin(time * 4) * 2

        draw_road(offset_y)

        draw_car(screen, player_x + offset_x + wave, player_y + offset_y, BLUE, angle)
        draw_car(screen, enemy_x + offset_x, enemy_y + offset_y, RED, 0)

        draw_text("Score: " + str(score), 10, 10)

        if shake > 0:
            shake -= 1

    elif state == GAME_OVER:
        game_over()

    pygame.display.update()