import pygame
import sys
from pygame.color import THECOLORS
import pygame as pg

pygame.init()
# цвета
color_sky = (200, 235, 255)
my_color = [0, 255, 0]
# параметры игры
w = 450
h = 700
FPS = 30
screen_size = (w, h)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
running = True
clock = pygame.time.Clock()
circle_pos = [w/2, h/2]  #  поставили в середину
circle_speed = [0, 0, 0, 0]

while running:
        # здесь смотрим,какие события произошли
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # нажатие на крестик: выход
                running = False
            if event.type == pygame.KEYDOWN:  # тип события - нажатие на кнопку
                if event.key == pygame.K_w:  # нажатие на w
                    circle_speed = [0, -5]  # по вертикали -1 - вверх
                if event.key == pygame.K_s:  # нажатие на s
                    circle_speed = [0, 5]
                if event.key == pygame.K_f: # кнопка торможения(особенность геймплея и усложнение его)--> отменяется
                    circle_speed = [0, 0]
                if event.key == pygame.K_a:
                    circle_speed = [-5, 0]
                if event.key == pygame.K_d:
                    circle_speed = [5, 0]
                if event.key == pygame.K_SPACE:
                    print(circle_pos)

        circle_pos[0] += circle_speed[0]  # по горизонтали
        circle_pos[1] += circle_speed[1]  # по вертикали

        # здесь рисуем всех персонажей,фон и так далее
        screen.fill(color_sky)
        pygame.draw.circle(screen, my_color, circle_pos, 20)

        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()