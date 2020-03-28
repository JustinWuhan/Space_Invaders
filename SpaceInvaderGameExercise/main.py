# https://www.youtube.com/watch?v=FfWpgLFMI7w&t=2032s

import pygame
import random
import math

from pygame import mixer  #mixer is for music

# Initialize the pygame module
pygame.init()  # ALWAYS REQUIRED

# Create screen (width, height) or (x, y)
screen = pygame.display.set_mode((800, 600))

# Background <a href='https://pngtree.com/so/space'>space png from pngtree.com</a>
background = pygame.image.load('background.png')
mixer.music.load('background.wav')
mixer.music.set_volume(0.2) #figured this one out on your own yay!
mixer.music.play(-1) #plays once and stops, add "-1" to play on loop

# Change title and logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('cards.png')
pygame.display.set_icon(icon)

# PLAYER
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

# ENEMY
enemyImg = [] #added each enemy variable as a list in order to create multiple ones
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# BULLET
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# SCORE
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32) #More fonts? www.dafont.com (add tff to file like images)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 32)
play_again_font = pygame.font.Font('freesansbold.ttf', 32)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (300, 250))

# blit method "draws" the image on the screen
# but we call the function inside the game loop
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state  # Read more on global: https://www.programiz.com/python-programming/global-keyword
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2))) #distance algebra
    if distance < 27:
        return True
    else:
        return False


# GAME LOOP
running = True
while running:
    # screen.fill((0, 0, 0))  # removed to add image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():  # event.get will obtain user inputs
        if event.type == pygame.QUIT:  # QUIT = exiting the window
            running = False

        if event.type == pygame.KEYDOWN:  # manipulate the Player Ship
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    mixer.Sound.set_volume(bullet_sound, 0.2) # did this one myself too!
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    # Player Movement
    playerX += playerX_change  # add change to player's X-axis location

    if playerX <= 0:  # making sure they don't go off the screen
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

    # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            mixer.Sound.set_volume(explosion_sound, 0.2)
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i])

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()  # ALWAYS REQUIRED
