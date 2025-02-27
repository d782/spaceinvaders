import pygame
import random
import math
from pygame import mixer


# initialize
pygame.init()

#create screen
screen=pygame.display.set_mode((800, 600))
#background

background=pygame.image.load('background.png')
#background_sound
mixer.music.load('background.wav')
mixer.music.play(-1)
#title and icon
pygame.display.set_caption("Space invaders")
icon=pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#player
playerImg=pygame.image.load('player.png')
playerX=370
playerY=460
playerX_change=0
def player(x,y):
    screen.blit(playerImg,(x,y))
#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(0.3)
def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

#bullet

bulletImg=pygame.image.load('bullet.png')
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=40
bullet_state="ready"
#score
score=0
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10
def show_score(x,y):
    score_value=font.render("Score :" +str(score),True,(255,255,255))
    screen.blit(score_value,(x,y))


def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX, enemyY,bulletX, bulletY):
    distance=math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance<27:
        return True
    else:
        return False


#game loop
running=True
while running:
     #background_image
    screen.blit(background,(0,0))
    #RGB
    
     #-------
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
    #if key pressed
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                playerX_change=-5
            if event.key==pygame.K_RIGHT:
                playerX_change=5
            if event.key ==pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('explosion.wav')
                    bullet_sound.play()
                    bulletX=playerX
                    fire_bullet(bulletX,bulletY)
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerX_change=0
            
                
    #Boundaries spaceship
    playerX+=playerX_change
    if playerX<=0:
        playerX=0
    elif playerX>=736:
        playerX=736
    for i in range(num_of_enemies):
        enemyX[i]+=enemyY_change[i]
        if enemyX[i]<=0:
            enemyX_change[i]=4
            enemyY[i]+=enemyY_change[i]
        elif enemyX[i]>=736:
            enemyX_change[i]=-4
            enemyY[i]+=enemyY_change[i]
        
        collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explosion=mixer.Sound('explosion.wav')
            explosion.play()
            bulletY=480
            bullet_state="ready"
            score+=1
            print(score)
            enemyX[i]=random.randint(0,800)
            enemyY[i]=random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)
    #bullet movement
    if bulletY<=0:
        bulletY=480
        bullet_state="ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY-=bulletY_change
    #----
    

    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()

