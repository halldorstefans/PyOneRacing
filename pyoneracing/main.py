import pygame

# import random for random numbers!
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/RacingCar_1.png")
        self.rect = self.surf.get_rect()
        self.rect.left = 370
        self.rect.right = 370
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
        self.surf = pygame.image.load("images/RacingCar_2.png")
        self.rect = self.surf.get_rect(
            center=(random.randint(180, 615), random.randint(-650, -50))

        )
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.bottom > 600:
            self.kill()

def show_score():
    font = pygame.font.Font('freesansbold.ttf', 32)
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (10, 10))


def game_over(score_value):
    global final_score
    if score_value != 0:
        final_score = score_value
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    score_font = pygame.font.Font('freesansbold.ttf', 32)
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    score_text = score_font.render("Final score: " + str(final_score), True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    screen.blit(score_text, (275, 350))
    return 0

# initialize pygame
pygame.init()

# create the screen object
# here we pass it a size of 800x600
screen = pygame.display.set_mode((800, 600))

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 800)

# create our 'player', right now he's just a rectangle
player = Player()

background = pygame.image.load('images/BackgroundRoad.png')
pygame.display.set_caption("PyOneRacing")
icon = pygame.image.load('images/IconCar.png') # Icon made by <a href="https://www.flaticon.com/authors/nikita-golubev" title="Nikita Golubev">Nikita Golubev</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>
pygame.display.set_icon(icon)

final_score = 0
score_value = 0

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                player = Player()
                all_sprites.add(player)
        elif event.type == pygame.QUIT:
            running = False        
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
        player.kill()
        game_over(score_value)
        score_value = 0
    
    if not all_sprites.has(player):
        game_over(score_value)
    else:
        score_value += 1

    pygame.display.flip()