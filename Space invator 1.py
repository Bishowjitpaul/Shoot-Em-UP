import pygame
import random
import math
from pygame import mixer  # mixer is basically a class that helps us handle all kind of music inside pygame. whether it can be repeating the music

# initialize the Pygame
pygame.init()

# create the screen ((width,height))
screen = pygame.display.set_mode((800, 600))

# Title
pygame.display.set_caption("Space Invader")

# Background Image
background = pygame.image.load("space pic.jpg")

# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)  # for (-1) it gonna play in loop
# Icon
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("a.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
# for multiple enemy , we create a list and append all in list.
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# Creating Bullet For Shooting
'''1. Starting position of the bullet 
    (the X co-ordinate[starting position] of the bullet is always equal to the spaceship)
# 2. decreasing Y co-ordinate.(cz bullet goes to 480 pixels to top [0] pixel)
# 3. bullet is disappearing at the top
# 4. state of the bullet (you cant see the bullet when  bullet's state is at 'READY') 
    ( when you see the bullet the bullet state is going to be at 'FIRE')'''

# Bullet
# Ready- you cant see the bullet on the screen
# Fire - the bullet is currently moving
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480  # For 1
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"


def player(x, y):
    # blit means draw
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    # blit means draw
    screen.blit(enemyImg[i], (x, y))


# bullet_state variable to global variable so it can be accessed inside the function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # for middle fire of the spaceship


# score display
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 40)
textX = 10
textY = 10

# game over text
over_text = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    over = over_text.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over, (200, 250))


def Show_score(x, y):
    score = font.render("KILLS:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# distance betwwen two piont (enemy and bullet)
def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop [(while= true: pass) not closed]
# event is variable
running = True
while running:
    # background color (RGB- RED, GREEN, BLUE)[0-255](tuple)
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            # print("Keystroke is pressed")

            if event.key == pygame.K_LEFT:
                # print("Left key is pressed")

                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                # print("right key is pressed")

                playerX_change = 2

            if event.key == pygame.K_SPACE:
                # print("space is pressed")
                if bullet_state == 'ready':  # bullet cant fire multiple times instead of crossing 0 pixel or top.
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX  # when the spacebar is pressed then we save "the current spaceship X co-ordinate" inside our bullet x varilabe
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            # print("Keystroke is remove")
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # spaceship limited screen or boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # playerX -= 0.1
    playerX += playerX_change

    # enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]

        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            # after collision bullet set the starting position of spaceship
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # print(score)
            # after die enemy  randomly present on the screen
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    # we cnt only fire one bullet. but for many fire bullet we have to set 0 pixels position bullet to 480 pixel position.
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)

    Show_score(textX, textY)

    pygame.display.update()
