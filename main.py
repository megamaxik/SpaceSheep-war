import pygame
import random
import pygame_menu
from os import path
from character import Enemy, Player


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
img_dir = path.join(path.dirname(__file__), 'images')
bg = pygame.image.load("images\Space.png").convert_alpha()
bg = pygame.transform.scale(bg, (1400, 1000))
#bg2 = pygame.image.load("images/backround_asteroids.png").convert_alpha()
#bg2 = pygame.transform.scale(bg, (1400, 1000))
#Asteroids = pygame.image.load(path.join(img_dir, "Asteroid.png")).convert()
player_img = pygame.image.load(path.join(img_dir, "SpaceSheep.png")).convert()
enemy_img = pygame.image.load(path.join(img_dir, "enemy.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "shot.png")).convert()


def load_music_files(*list_names):
    expl_sounds = []
    snd_dir = path.join(path.dirname(__file__), 'sound')
    for name in list_names:
        expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, name)))
    return expl_sounds


expl_sounds = [*load_music_files('shoot.mp3', 'expl1.mp3', 'expl2.wav', 'expl3.mp3')]


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


issound = True


def start_game():
    player = Player(player_img, 160, 100, (WIDTH - (WIDTH - 100), HEIGHT / 2), 0, 0, 100, all_sprites)
    for _ in range(int(8 * dif)):
        Enemy(enemy_img, 160, 100, (WIDTH - 50, random.randrange(HEIGHT - 100)), -3, mobs, all_sprites)
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
                    if issound:
                        expl_sounds[0].play()
                    player.shoot(bullet_img, bullets, all_sprites)
        all_sprites.update((WIDTH, HEIGHT))
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for _ in hits:
            if issound:
                Enemy(enemy_img, 160, 100, (WIDTH - 50, random.randrange(HEIGHT - 100)), -3, mobs, all_sprites)
                expl_sounds[1].play()

        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_rect_ratio(0.6))
        for _ in hits:
            player.hp -= int(10 * dif)
            Enemy(enemy_img, 160, 100, (WIDTH - 50, random.randrange(HEIGHT - 100)), -3, mobs, all_sprites)
            if issound:
                expl_sounds[3].play()
            if player.hp <= 0:
                if issound:
                    expl_sounds[2].play()
                all_sprites.remove(player)
                running = False
        #if dif == 0.75:
            #screen.blit(bg2, (0, 0))
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        screen.blit(font.render(text, True, (180, 0, 0)), (550, 10))
        draw_hp_bar(screen, 5, 5, player.hp)
        pygame.display.flip()


def set_sound(value, sound):
    global issound
    issound = sound


def set_difficulty(value, difficulty):
    global dif
    dif = difficulty


def start_menu():
    bg = pygame.image.load("images\Space.png").convert_alpha()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    player_img = pygame.image.load(path.join(img_dir, "SpaceSheep.png")).convert()
    enemy_img = pygame.image.load(path.join(img_dir, "enemy.png")).convert()
    bullet_img = pygame.image.load(path.join(img_dir, "shot.png")).convert()
    menu = pygame_menu.Menu('   Space Sheep War', 400, 400, theme=pygame_menu.themes.THEME_DARK)
    menu.add.selector("Sound :", [("on", True), ("off", False)], onchange=set_sound)
    menu.add.selector('Difficulty :', [('Easy', 0.75), ('normal', 1), ('Hard', 2)], onchange=set_difficulty)
    menu.add.button('Play', start_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)
    pygame.quit()


start_menu()
