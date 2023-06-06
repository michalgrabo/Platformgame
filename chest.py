import pygame

class Chest(pygame.sprite.Sprite):

    def __init__(self, pos, type):
        super().__init__()
        #Creating variables
        self.image = pygame.Surface((60, 60))
        self.image = pygame.image.load("/Users/michalgrabowski/PycharmProjects/platformgame/Graphics/chest/tile000.png")
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.open = False
        #self.image.fill("orange")
        self.rect = self.image.get_rect(topleft = pos)
        self.type = type


    def update(self, x_shift):
        #Making sure the position of the chests stays the same relative to the level map
        self.rect.x += x_shift
