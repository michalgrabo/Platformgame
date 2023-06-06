import pygame
from settings import screen_width

class Bullet(pygame.sprite.Sprite):

    def __init__(self, pos, direction):
        super().__init__()
        #self.image = pygame.Surface((30, 10))
        #self.image.fill("red")
        self.image = pygame.image.load("/Users/michalgrabowski/PycharmProjects/platformgame/Graphics/fire_ball/firebal_pixel.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(topleft=pos)
        if direction == 0:
            direction = 1
        self.speed = 10
        self.direction = pygame.math.Vector2(direction * self.speed, 0)

    def update(self):
        self.rect.x += self.direction.x
        if self.rect.x > screen_width or self.rect.x < 0:
            self.kill()
