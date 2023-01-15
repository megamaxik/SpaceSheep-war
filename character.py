import pygame
import random
from bullet import Bullet

Anim_player = [pygame.image.load("images/animations/player/1pl.png"), pygame.image.load("images/animations/player/2pl.png"),
        pygame.image.load("images/animations/player/3pl.png")]
Anim_enemy = [pygame.image.load("images/animations/enemy/1en.png"), pygame.image.load("images/animations/enemy/2en.png"),
        pygame.image.load("images/animations/enemy/3en.png")]

class Character(pygame.sprite.Sprite):
    def __init__(self, image, w, h, *groups):
        super().__init__(*groups)
        self.w = w
        self.h = h
        self.image = pygame.transform.scale(image, (w, h))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.tick = 0
    def update(self, *args):
        pass


class Enemy(Character):
    def __init__(self, image, w, h, coords, speed_x, *groups):
        super().__init__(image, w, h, *groups)
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.speed_x = speed_x

    def move(self, screen_size):
        self.rect.x += self.speed_x
        if self.rect.left < 0 + 10:
            self.rect.y = random.randrange(screen_size[1] - self.rect.height)
            self.rect.x = screen_size[0] - 50

    def update(self, *args):
        if args:
            self.move(args[0])
            if self.rect.left < 0 + 10:
                self.rect.y = random.randrange(args[1] - self.rect.height)
                self.rect.x = args[0] - 50
                self.speedx = -3
        if self.tick <= 10:
            self.image = pygame.transform.scale(Anim_enemy[0], (self.w, self.h))
        if self.tick > 10 and self.tick <= 20:
            self.image = pygame.transform.scale(Anim_enemy[1], (self.w, self.h))
        if self.tick > 20 and self.tick <= 30:
            self.image = pygame.transform.scale(Anim_enemy[2], (self.w, self.h))
            self.tick = 0
        self.tick += 1

class Player(Character):
    def __init__(self, image, w, h, coords, speed_x, speed_y, hp, *groups):
        super().__init__(image, w, h, *groups)
        self.rect.centerx = coords[0]
        self.rect.bottom = coords[1]
        self.speed_y = speed_y
        self.speed_x = speed_x
        self.hp = hp

    def update(self, *args):
        if args:
            self.move(args[0])
        if self.tick <= 10:
            self.image = pygame.transform.scale(Anim_player[0], (self.w, self.h))
        if self.tick > 10 and self.tick <= 20:
            self.image = pygame.transform.scale(Anim_player[1], (self.w, self.h))
        if self.tick > 20 and self.tick <= 30:
            self.image = pygame.transform.scale(Anim_player[2], (self.w, self.h))
            self.tick = 0
        self.tick += 1



    def move(self, screen_size):
        self.speed_y = 0
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -8
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 8
        if keystate[pygame.K_UP]:
            self.speed_y = -8
        if keystate[pygame.K_DOWN]:
            self.speed_y = 8
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > screen_size[0]:
            self.rect.right = screen_size[0]
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > screen_size[1]:
            self.rect.bottom = screen_size[1]
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self, bullet_img, bullets_group, all_sprites):
        Bullet(bullet_img, self.rect.centerx + 50, self.rect.bottom - 25, bullets_group, all_sprites)

    def dead(self):
        self.kill()



