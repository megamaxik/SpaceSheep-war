import pygame
import random
import pygame_menu
from os import path
from character import Enemy, Player

a = open("score.txt", "r").readline()
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
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
img_dir = path.join(path.dirname(__file__), 'images')
bg = pygame.image.load("images/Space.png").convert_alpha()
bg = pygame.transform.scale(bg, (1400, 1000))
bg2 = pygame.image.load("images/backround_asteroids.png").convert_alpha()
bg2 = pygame.transform.scale(bg2, (1400, 1000))
bg3 = pygame.image.load("images/win.png").convert_alpha()
bg3 = pygame.transform.scale(bg3, (1400, 1000))
bg4 = pygame.image.load("images/game_over.png").convert_alpha()
bg4 = pygame.transform.scale(bg4, (1400, 1000))
player_img = pygame.image.load(path.join(img_dir, "SpaceSheep.png")).convert()
enemy_img = pygame.image.load(path.join(img_dir, "enemy.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "shot.png")).convert()
aster_img = pygame.image.load(path.join(img_dir, "Asteroid.png")).convert()


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
    bar_lenght = 250
    bar_height = 25
    fill = (pct / 100) * bar_lenght
    outline_rect = pygame.Rect(x, y, bar_lenght, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def start_game():
    all_sprites = pygame.sprite.Group()
    player = Player(player_img, 160, 100, (WIDTH - (WIDTH - 100), HEIGHT / 2), 0, 0, 100, all_sprites)
    for _ in range(int(8 * dif)):
        x = random.randint(100, 500)
        if dif == 0.75:
            Enemy(aster_img, 160, 100, (WIDTH - x, random.randrange(HEIGHT - 100)), -3, False, mobs, all_sprites)
        else:
            Enemy(enemy_img, 160, 100, (WIDTH - x, random.randrange(HEIGHT - 100)), -3, True, mobs, all_sprites)
    running = True
    counter, text = 100, "Время до взрыва: 100".rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont(None, 36)
    kills = 0
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if kills != 100 * dif and player.hp > 0:
                    counter -= 1
                    text = "Время до взрыва: " + str(counter).rjust(3) + "  Целей уничтожено: "\
                           + str(kills).rjust(3) if counter > 0 else 'время вышло!'
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if issound:
                        expl_sounds[0].play()
                    player.shoot(bullet_img, bullets, all_sprites)
                if event.key == pygame.K_ESCAPE:
                    running = False
        all_sprites.update((WIDTH, HEIGHT))
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for _ in hits:
            if issound:
                expl_sounds[1].play()
            if kills <= (100 * dif + 1) - (10 * dif):
                if dif == 0.75:
                    Enemy(aster_img, 160, 100, (WIDTH - 50, random.randrange(HEIGHT - 100)),
                          -3, False, mobs, all_sprites)
                else:
                    Enemy(enemy_img, 160, 100, (WIDTH - 50, random.randrange(HEIGHT - 100)),
                          -3, True, mobs, all_sprites)
            kills += 1
        hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_rect_ratio(0.9))
        for _ in hits:
            player.hp -= int(10 * dif)
            if dif == 0.75:
                Enemy(aster_img, 160, 100, (WIDTH - 50, random.randrange(HEIGHT - 100)), -3, False, mobs, all_sprites)
            else:
                Enemy(enemy_img, 160, 100, (WIDTH - 50, random.randrange(HEIGHT - 100)), -3, True, mobs, all_sprites)
            if issound:
                expl_sounds[3].play()
            if player.hp <= 0:
                if issound:
                    expl_sounds[2].play()
                all_sprites.remove(player)
        if dif == 0.75:
            screen.blit(bg2, (0, 0))
        else:
            screen.blit(bg, (0, 0))
        all_sprites.draw(screen)
        if kills != 100 * dif:
            draw_hp_bar(screen, 5, 5, player.hp)
        if kills != 100 * dif:
            screen.blit(font.render(text, True, (180, 0, 0)), (270, 10))
        if kills == 100 * dif or player.hp <= 0:
            if kills == 100 * dif:
                screen.blit(bg3, (0, 0))
            else:
                screen.blit(bg4, (0, 0))
            if int(a) > counter * kills:
                score = a
            else:
                f = open("score.txt", 'w')
                score = counter * kills
                f.write(str(counter * kills))
            screen.blit(font.render(text, True, (0, 180, 0)), (WIDTH // 2 - 200, HEIGHT // 2 - 100))
            screen.blit(font.render("Счет:" + str(counter * kills),
                                    True, (0, 180, 0)), (WIDTH // 2 - 200, HEIGHT // 2 - 50))
            screen.blit(font.render("Рекорд:" + str(score), True, (0, 180, 0)), (WIDTH // 2 - 200, HEIGHT // 2))
            screen.blit(font.render("Нажмите esc для выхода", True, (0, 180, 0)), (WIDTH // 2 - 200, HEIGHT // 2 + 50))

        pygame.display.flip()


def set_sound(value, sound):
    global issound
    issound = sound


def set_difficulty(value, difficulty):
    global dif
    dif = difficulty


def start_menu():
    menu = pygame_menu.Menu('   Space Sheep War', 400, 400, theme=pygame_menu.themes.THEME_DARK)
    menu.add.selector("Звук :", [("вкл.", True), ("выкл.", False)], onchange=set_sound)
    menu.add.selector('Сложность :', [('легко', 0.75), ('средне', 1), ('тяжело', 2)], onchange=set_difficulty)
    menu.add.button('Играть', start_game)
    menu.add.button('Выход', pygame_menu.events.EXIT)
    menu.mainloop(screen)
    pygame.quit()


start_menu()
