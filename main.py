# This is a sample Python script.

import pygame
import random

# initialize pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('space.png')

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
bulletY_change = 10
bullet_state = "ready"

# player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# enemy

enemyImg = pygame.image.load('alien.png')
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_change = 0.3
enemyY_change = 40


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # 16 is for center of ship
    screen.blit(bulletImg, (x + 16, y + 10))


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
                fire_bullet(playerX, bulletY)
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

    # enemy
    enemyX += enemyX_change

    # enemy movement
    if enemyX < 0:
        enemyX_change = 0.3
        enemyY += enemyY_change

    elif enemyX > 736:
        enemyX_change = -0.3
        enemyY += enemyY_change

    # bullet movement
    if bullet_state is "fire":
        fire_bullet(playerX,bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
