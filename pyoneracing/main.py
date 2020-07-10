import pygame, random, sys

# Initialize pygame
pygame.init()

# Create the screen object
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set background, caption, icon and sounds
background = pygame.image.load('resources/images/BackgroundRoad.png')
pygame.display.set_caption("PyOneRacing")
icon = pygame.image.load('resources/images/IconCar.png')
pygame.display.set_icon(icon)
pygame.mixer.music.load("resources/sounds/cinematicTrack.wav")
pygame.mixer.music.play(-1)
explosionSound = pygame.mixer.Sound("resources/sounds/bump.wav")

# Initialize scores and other properties
final_score = 0
score_value = 0
top_score = 0
fontType = 'freesansbold.ttf'
newEnemyTimer = 800

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("resources/images/RacingCar_1.png")
        self.rect = self.surf.get_rect()
        self.rect.left = 440
        self.rect.right = 440
        self.rect.top = 550
        self.rect.bottom = 550

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.left < 140:
            self.rect.left = 140
        elif self.rect.right > 650:
            self.rect.right = 650
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("resources/images/RacingCar_2.png")
        self.rect = self.surf.get_rect(center=(random.randint(180, 615), random.randint(-650, -50)))
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > 600:
            self.kill()

def terminate():
    pygame.quit()
    sys.exit()

def show_score():
    font = pygame.font.Font(fontType, 32)
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (10, 10))


def game_over(score_value):
    global final_score
    global top_score
    if score_value != 0:
        final_score = score_value
        if top_score < final_score:
            top_score = final_score
    over_font = pygame.font.Font(fontType, 64)
    score_font = pygame.font.Font(fontType, 32)
    restart_font = pygame.font.Font(fontType, 16)
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    score_text = score_font.render("Final score: " + str(final_score), True, (255, 255, 255))
    topScore_text = score_font.render("Top score: " + str(top_score), True, (255, 255, 255))
    restart_text = restart_font.render("Press 'R' to restart the game", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    screen.blit(score_text, (280, 350))
    screen.blit(topScore_text, (280, 200))
    screen.blit(restart_text, (295, 425))
    return 0

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                return

def StartScreen():
    over_font = pygame.font.Font(fontType, 24)
    over_text = over_font.render("Press any key to start the game", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, newEnemyTimer)

# Create player
player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

font = pygame.font.SysFont(None, 30)
StartScreen()
pygame.display.update()
waitForPlayerToPressKey()

# Run game
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                terminate()
            if event.key == pygame.K_r:
                player = Player()
                all_sprites.add(player)
                pygame.time.set_timer(ADDENEMY, newEnemyTimer)
        elif event.type == pygame.QUIT:
            terminate()
        elif(event.type == ADDENEMY):
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
    screen.blit(background, (0, 0))
    pressed_keys = pygame.key.get_pressed()
    if all_sprites.has(player):
        player.update(pressed_keys)
    enemies.update()
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    show_score()

    if pygame.sprite.spritecollideany(player, enemies):
        if all_sprites.has(player):            
            explosionSound.play()
        player.kill()
        for enemy in all_sprites:
            enemy.kill()
        pygame.time.set_timer(ADDENEMY, 0)
        game_over(score_value)
        score_value = 0
    
    if not all_sprites.has(player):
        game_over(score_value)
    else:
        score_value += 1

    pygame.display.flip()