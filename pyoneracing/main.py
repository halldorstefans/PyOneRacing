import pygame, random, math

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('images/BackgroundRoad.png')

# Title and Icon
pygame.display.set_caption("images/PyOneRacing")
icon = pygame.image.load('images/IconCar.png') # Icon made by <a href="https://www.flaticon.com/authors/nikita-golubev" title="Nikita Golubev">Nikita Golubev</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
pygame.display.set_icon(icon)

# Race cars - Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
playerCarImg = pygame.image.load('images/RacingCar1.png')
playerX = 370
playerY = 450
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyY_change = []
num_of_enemies = 2

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/RacingCar2.png'))
    enemyX.append(random.randint(120, 550))
    enemyY.append(-50)
    enemyY_change.append(4)


def game_over():
    game_over_text()
    return 0

def game_over_text():
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x,y):
    screen.blit(playerCarImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def isCollision(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt(math.pow(enemyX - playerX, 2) + (math.pow(enemyY - playerY, 2)))
    if distance < 90:
        return True
    else:
        return False

# Loop game
running = True

while running:
    # RGB - Red, Green, Blue
    screen.fill((0,0,0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_r:
                num_of_enemies = 2

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        
    playerX += playerX_change
    if playerX <= 120:
        playerX = 120
    elif playerX >= 550:
        playerX = 550

    for i in range(num_of_enemies):

        if enemyY[i] > 500:
            enemyX[i] = random.randint(120, 550)
            enemyY[i] = -50
            enemy(enemyX[i], enemyY[i], i)
            break

        collision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if collision:         
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            num_of_enemies = game_over()

        enemyY[i] += enemyY_change[i]

        enemy(enemyX[i], enemyY[i], i)

    if num_of_enemies == 0:
        game_over_text()

    player(playerX, playerY)
    pygame.display.update()