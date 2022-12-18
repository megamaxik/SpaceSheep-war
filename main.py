import pygame
import random
import pygame_menu
from os import path
img_dir = path.join(path.dirname(__file__), 'images')
WIDTH = 1400
HEIGHT = 1000
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bg = pygame.image.load("images\Space.png").convert_alpha()
bg = pygame.transform.scale(bg, (1400, 1000))
player_img = pygame.image.load(path.join(img_dir, "SpaceSheep.png")).convert()
enemy_img = pygame.image.load(path.join(img_dir, "enemy.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "shot.png")).convert()
global dif
dif = 1
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (80, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 10

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.kill()

class enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (160, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 50
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.speedx = -3

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left < 0 + 10:
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.rect.x = WIDTH - 50
            self.speedx = -3



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (160, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH - (WIDTH - 100)
        self.rect.bottom = HEIGHT / 2
        self.speedy = 0
        self.speedx = 0

    def update(self):
        self.speedy = 0
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx + 50, self.rect.bottom - 25)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def dead(self):
        self.kill()


def set_sound(value, sound):
    pass

def set_difficulty(value, difficulty):
    pass



def start_the_game():


    player = Player()
    all_sprites.add(player)
    for i in range(8 * dif):
        m = enemy()
        all_sprites.add(m)
        mobs.add(m)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
        all_sprites.update()
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            m = enemy()
            all_sprites.add(m)
            mobs.add(m)

        hits = pygame.sprite.spritecollide(player, mobs, False)
        if hits:
            player.dead()

            running = False

        screen.blit(bg,(0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

class MainScreen():
    bg = pygame.image.load("images\Space.png").convert_alpha()
    bg = pygame.transform.scale(bg, (1400, 1000))
    player_img = pygame.image.load(path.join(img_dir, "SpaceSheep.png")).convert()
    enemy_img = pygame.image.load(path.join(img_dir, "enemy.png")).convert()
    bullet_img = pygame.image.load(path.join(img_dir, "shot.png")).convert()
    menu = pygame_menu.Menu('   Space Sheep War', 400, 400, theme=pygame_menu.themes.THEME_DARK)
    menu.add.selector("Sound :", [("on", 1), ("off", 2)], onchange=set_sound)
    menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)
    pygame.quit()

MainScreen()