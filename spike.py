import pygame

class Spike(pygame.sprite.Sprite):

    def __init__(self, pos):
        #Variables
        super().__init__()
        self.image = pygame.Surface((32, 32))
        #self.image.fill("yellow")
        self.image = pygame.image.load("/Users/michalgrabowski/PycharmProjects/platformgame/Graphics/spikes/image.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect(topleft = pos)
        self.offset = (-40, -30)
        self.hitbox = self.rect.inflate(self.offset[0], self.offset[1])
        self.hitbox.y = pos[1] - 20
        #self.hitbox.y = pos[1] + 30

    def update(self, x_shift):
        #Making sure the position of the spikes stays the same relative to the level map
        self.hitbox.x += x_shift
        self.rect = self.hitbox.inflate(self.offset[0] * -1, self.offset[1] * -1)

    def draw_hitbox_three(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 1)
