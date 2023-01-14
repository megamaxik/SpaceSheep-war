import pygame
import random
import pygame_menu
from os import path
img_dir = path.join(path.dirname(__file__), 'images')
snd_dir = path.join(path.dirname(__file__), 'sound')
WIDTH = 1400
HEIGHT = 1000
FPS = 60
issound = True
dif = 0.75
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
bg = pygame.image.load("images/Space.png").convert_alpha()
bg = pygame.transform.scale(bg, (1400, 1000))
player_img = pygame.image.load(path.join(img_dir, "SpaceSheep.png")).convert()
enemy_img = pygame.image.load(path.join(img_dir, "enemy.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "shot.png")).convert()
expl_sounds = []
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'shoot.mp3'))
expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, 'expl1.mp3')))
expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, 'expl2.wav')))
expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, 'expl3.mp3')))


def draw_hp_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 500
    BAR_HEIGHT = 50
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def newenemy():
    m = enemy()
    all_sprites.add(m)
    mobs.add(m)



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
        self.hp = 100

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

issound = True
def set_sound(value, sound):
    global issound
    issound = sound
    pass

def set_difficulty(value, difficulty):
    global dif
    dif = difficulty
    pass



def start_the_game():
    global issound
    global dif
    player = Player()
    all_sprites.add(player)
    for i in range(int(8 * dif)):
        m = enemy()
        all_sprites.add(m)
        mobs.add(m)
    running = True
    counter, text = 300, "300".rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont(None, 72)
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                counter -= 1
                text = "Время до взрыва: " + str(counter).rjust(3) if counter > 0 else 'время вышло!'
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if issound == True:
                        shoot_sound.play()
                    player.shoot()
        all_sprites.update()
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            if issound == True:
                expl_sounds[0].play()

            newenemy()

        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_rect_ratio(0.6))
        for hit in hits:
            player.hp -= int(10 * dif)
            if issound == True:
                expl_sounds[2].play()
            newenemy()
            if player.hp <= 0:
                if issound == True:
                    expl_sounds[1].play()
                all_sprites.remove(player)
                running = False
        screen.blit(bg,(0, 0))
        all_sprites.draw(screen)
        screen.blit(font.render(text, True, (180, 0, 0)), (550, 10))
        draw_hp_bar(screen, 5, 5, player.hp)
        pygame.display.flip()


class MainScreen():
    bg = pygame.image.load("images\Space.png").convert_alpha()
    bg = pygame.transform.scale(bg, (1400, 1000))
    player_img = pygame.image.load(path.join(img_dir, "SpaceSheep.png")).convert()
    enemy_img = pygame.image.load(path.join(img_dir, "enemy.png")).convert()
    bullet_img = pygame.image.load(path.join(img_dir, "shot.png")).convert()
    menu = pygame_menu.Menu('   Space Sheep War', 400, 400, theme=pygame_menu.themes.THEME_DARK)
    menu.add.selector("Sound :", [("on", True), ("off", False)], onchange=set_sound)
    menu.add.selector('Difficulty :', [('Easy', 0.75), ('normal', 1), ('Hard', 2)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)
    pygame.quit()

MainScreen()