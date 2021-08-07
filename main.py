import pygame
import random
import math
from pygame import mixer



# Initialize pygame
pygame.init()

# Create Game Screen               X , Y
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space-Invaders")
icon = pygame.image.load('asset/tdsloane.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('asset/space-background.jpg')

# Background Music
mixer.music.load('asset/bensound-extremeaction.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 25)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Game Over
gg_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over_txt():
    gg_txt = gg_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gg_txt, (200, 250))


# Player
playerImg = pygame.image.load('asset/playership.png')
playerX = 370
playerY = 480
playerX_change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Alien
alienImg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_aliens = 6

for i in range(num_aliens):
    alienImg.append(pygame.image.load('asset/alien.png'))
    alienX.append(random.randint(0, 736))
    alienY.append(random.randint(20, 150))
    alienX_change.append(0.2)
    alienY_change.append(40)


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y,))

def alienChange(collision):
    global alienImg
    fallen = 0
    if collision:
        fallen += 1
        if (fallen%2) == 0:
            alienImg = pygame.image.load('alien.png')
        else:
            alienImg = pygame.image.load('alien2.png')

# Bullet
bulletImg = pygame.image.load('asset/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"  # Ready = bullet not on screen | Fire = bullet is moving


def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt((math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # Drawing to Screen - RGB
    screen.fill((0, 0, 0))
    # Background
    screen.blit(background, (0, 0))
    # Allow the window to close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fireBullet(bulletX, bulletY)
                    bullet_sound = mixer.Sound('asset/lazer.mp3')
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Player placement and boundaries
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Alien movement and boundaries
    for i in range(num_aliens):

        # Game Over
        if alienY[i] > 420:
            for j in range(num_aliens):
                alienY[j] = 2000
            game_over_txt()
            break

        alienX[i] += alienX_change[i]

        if alienX[i] <= 0:
            alienX_change[i] = 0.2
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -0.2
            alienY[i] += alienY_change[i]

        # Collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            explosion_sound = mixer.Sound('asset/explosion.mp3')
            explosion_sound.play()
            bullet_state = "ready"
            score_value += 100
            print(score_value)
           # alienChange(collision)    Left for later
            alienX[i] = random.randint(0, 736)
            alienY[i] = random.randint(20, 150)

        alien(alienX[i], alienY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(textX, textY)

    # Update the screen
    pygame.display.update()
