import pygame

class Tile(pygame.sprite.Sprite):

    def __init__(self, pos, size):
        #variables
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image = pygame.image.load("/Users/michalgrabowski/PycharmProjects/platformgame/Graphics/Tiles/dungen_tiles (1) (1).png")
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        #Making sure the position of the tile stays the same relative to the level ma
        self.rect.x += x_shift
