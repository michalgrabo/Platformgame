import pygame

class Finish(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        #Variables
        self.image = pygame.Surface((64, 32))
        #self.image.fill("white")
        self.image = pygame.image.load("/Users/michalgrabowski/PycharmProjects/platformgame/Graphics/finish_line/finish_line.png")
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        #Making sure the position of the finish line stays the same relative to the level map
        self.rect.x += x_shift
