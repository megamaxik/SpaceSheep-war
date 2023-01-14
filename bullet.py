import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, x, y, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(bullet_img, (80, 40))
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = 10

    def update(self, *args):
        self.rect.x += self.speedx
        if args:
            if self.rect.right > args[0][0]:
                self.kill()

