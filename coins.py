import pygame

class Coins(pygame.sprite.Sprite):

    def __init__(self, pos):
        #Variables/characteristic
        super().__init__()
        self.image = pygame.Surface((64,64))
        #self.image.fill("yellow")
        self.image = pygame.image.load("/Users/michalgrabowski/PycharmProjects/platformgame/Graphics/coin/monedaNo1_00.png")
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        #Making sure the position of the coins stay the same relative to the level map
        self.rect.x += x_shift


