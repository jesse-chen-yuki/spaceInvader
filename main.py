# This is a sample Python script.
import math
import pygame
import random
from pygame import mixer

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('space.png')

# background sound
mixer.music.load('background.mp3')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('space-invaders.png')
pygame.display.set_icon(icon)

# bullet
# Ready - can't see bullet on screen
# Fire - bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 1.5
bullet_state = "ready"

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
enemySpeed = 0

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 0, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # 16 is for center of ship
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow((enemyX - bulletX), 2) + math.pow((enemyY - bulletY), 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB color fill 0-255
    screen.fill((0, 0, 0))
    # add background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if key stroke is pressed, left or right
        if event.type == pygame.KEYDOWN:
            # print('a key is pressed')
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
                # print("Left arrow is pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
                # print("Right arrow is pressed")
            if event.key == pygame.K_SPACE:
                # fire only when ready
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    # print("space is pressed")

        if event.type == pygame.KEYUP:
            # stop moving when key released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
                # print("key released")

    # draw player
    playerX += playerX_change

    # add boundary
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    enemySpeed += 0.00001
    # enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 0.3 + enemySpeed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -1*(0.3 + enemySpeed)
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # print(score_value)
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
