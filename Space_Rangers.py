import pygame
import random
import math
from pygame import mixer

pygame.init()

running = True
width_Xaxis = 800
height_Yaxis = 600

game_wind = pygame.display.set_mode((width_Xaxis, height_Yaxis))

try:
    background = pygame.image.load("background.png")
except pygame.error as e:
    print(f"Unable to load background image: {e}")
    running = False

mixer.music.load("background.wav")
mixer.music.play(-1)

pygame.display.set_caption("The Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

PlayerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

bulletImg = pygame.image.load('bullet.png')
bullets = []

bulletY_change = 10  # Define bulletY_change here
bullet_speed = bulletY_change
bullet_spread = 0

score_value = 0
font = pygame.font.Font('OpenSans-BoldItalic.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font("RobotoCondensed-Bold.ttf", 64)

level_value = 1
level_font = pygame.font.Font('OpenSans-BoldItalic.ttf', 32)

lives_value = 3
lives_font = pygame.font.Font('OpenSans-BoldItalic.ttf', 32)

powerupImg = pygame.image.load('icons8-slender-man-16.png')
powerupX = random.randint(0, 736)
powerupY = random.randint(50, 150)
powerup_visible = False
powerup_effect_duration = 15  # seconds
powerup_respawn_time = 60  # seconds
powerup_timer = 0
last_powerup_time = pygame.time.get_ticks()

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    game_wind.blit(score, (x, y))

def show_level(x, y):
    level = level_font.render("Level : " + str(level_value), True, (255, 255, 255))
    game_wind.blit(level, (x, y))

def show_lives(x, y):
    lives = lives_font.render("Lives : " + str(lives_value), True, (255, 255, 255))
    game_wind.blit(lives, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    game_wind.blit(over_text, (200, 250))

def player(x, y):
    game_wind.blit(PlayerImg, (x, y))

def enemy(x, y, i):
    game_wind.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_speed, bullet_spread
    bullets.append({"x": x, "y": y, "state": "fire", "spread": bullet_spread})

def isCollision(x1, y1, x2, y2, distance_threshold=27):
    distance = math.sqrt(math.pow(x1 - x2, 2) + (math.pow(y1 - y2, 2)))
    return distance < distance_threshold

def increase_level():
    global num_of_enemies, enemyX_change, level_value, bullet_speed
    level_value += 1
    for i in range(num_of_enemies):
        enemyX_change[i] += 0.5  # Increase enemy speed
    if num_of_enemies < 12:
        num_of_enemies += 2
        for i in range(num_of_enemies - 2, num_of_enemies):
            enemyImg.append(pygame.image.load('enemy.png'))
            enemyX.append(random.randint(0, 736))
            enemyY.append(random.randint(50, 150))
            enemyX_change.append(4 + level_value * 0.5)  # Increase starting speed with level
            enemyY_change.append(40)

while running:
    game_wind.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                fire_bullet(playerX + 16, playerY + 10)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            lives_value -= 1
            enemyY[i] = random.randint(50, 150)
            if lives_value == 0:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over_text()
                running = False

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4 + level_value * 0.5  # Increase speed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4 - level_value * 0.5  # Increase speed
            enemyY[i] += enemyY_change[i]

        for bullet in bullets:
            if bullet["state"] == "fire" and isCollision(enemyX[i], enemyY[i], bullet["x"], bullet["y"]):
                bullet["state"] = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    for bullet in bullets:
        if bullet["y"] <= 0:
            bullet["state"] = "ready"
        if bullet["state"] == "fire":
            game_wind.blit(bulletImg, (bullet["x"], bullet["y"]))
            bullet["y"] -= bullet_speed  # Update bullet speed

    # Powerup logic
    current_time = pygame.time.get_ticks()
    if (current_time - last_powerup_time) >= powerup_respawn_time * 1000 and not powerup_visible:
        # Calculate opposite side of player for powerup spawn
        if playerX < width_Xaxis / 2:
            powerupX = random.randint(int(width_Xaxis / 2), width_Xaxis - 64)
        else:
            powerupX = random.randint(0, int(width_Xaxis / 2) - 64)
        powerupY = random.randint(50, 150)
        powerup_visible = True
        last_powerup_time = current_time

    if powerup_visible:
        game_wind.blit(powerupImg, (powerupX, powerupY))
        if isCollision(playerX, playerY, powerupX, powerupY, 50):
            # Apply powerup effect
            bullet_spread += 3
            powerup_visible = False

    # Update bullet positions based on modified spread
    for bullet in bullets:
        if bullet["state"] == "fire":
            bullet["x"] += bullet["spread"] // 2  # Adjust spread
            bullet["y"] -= bullet_speed

    player(playerX, playerY)
    show_score(textX, textY)
    show_level(textX, textY + 40)
    show_lives(textX, textY + 80)

    pygame.display.update()


