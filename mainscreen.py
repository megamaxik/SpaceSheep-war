import pygame
import sys
import pygame_menu
from pygame.color import THECOLORS

w = 450
h = 700
FPS = 30
clock = pygame.time.Clock()
pygame.init()
surface = pygame.display.set_mode((600, 400))

class MainScreen():
    def set_difficulty(value, difficulty):
        # Do the job here !
        pass

    def start_the_game():
        pass

    def set_sound(value, sound):
        pass

    menu = pygame_menu.Menu('   Space Sheep War', 400, 400, theme=pygame_menu.themes.THEME_DARK)
    menu.add.selector("Sound :", [("on", 1), ("off", 2)], onchange=set_sound)
    menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
    menu.add.button('Play', start_the_game)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(surface)
    pygame.quit()

MainScreen()