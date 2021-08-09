import pygame
import random
import math
from pygame import mixer

# initialise the pygame modules
pygame.init()

# game state
game_state = 'play'

# create the screen
screen = pygame.display.set_mode((800, 600))

#  title and icon
pygame.display.set_caption('Space Invadors')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('space.jpg')
# play background music
mixer.music.load('musicloop.wav')
mixer.music.play(-1)

# player 
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
# create a fixed number of enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletY_change = 10
# ready state = bullet is not visible on screen
# fire state = bullet is visisble and moves up on the screen
bullet_state = 'ready'

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

# calculate collision between objects
def isCollision(enemyX, enemyY, bulletX, bulletY):
    # equasion √(x2 - x1)**2 + (y2 -y1)**2
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# game loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if key is pressed check if it is right or left
        if event.type == pygame.KEYDOWN and game_state == 'play':
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    # play shooting sound when firing the bullet
                    bullet_sound = mixer.Sound('shoot.wav')
                    bullet_sound.play()
                    # get the curretnt x coordinate of the spaceship
                    bulletX = playerX
                    # fire the bullet
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # player movement        
    playerX += playerX_change
    # stop spaceship when it reaches the edge of screen
    if playerX <= 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # enemy movement
    for  i in range(num_of_enemies):
        # game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            game_state = 'over'
            
            break

        enemyX[i] += enemyX_change[i]
        # move the enemy down if it hits the edge of the screen
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # play enemy hit sound
            collision_sound = mixer.Sound('hit.wav')
            collision_sound.play()
            # reset the bullet 
            bulletY = 480
            bullet_state = 'ready'
            # increase score by 1
            score_value += 1
            # generate a new enemy position
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    

    player(playerX, playerY)
    show_score(textX, textY)
    
   
    pygame.display.update()