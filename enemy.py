import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        #creating variables
        self.image = pygame.image.load("/Users/michalgrabowski/PycharmProjects/platformgame/Graphics/enemies/Hobbit - Idle2.png")
        self.image = pygame.transform.scale(self.image, (130, 130))
        self.rect = self.image.get_rect(topleft = pos)
        self.facing = random.randint(0, 1)
        #Implement random direction
        if self.facing == 0:
            self.direction = pygame.math.Vector2(-1, 0)
        elif self.facing == 1:
            self.direction = pygame.math.Vector2(1, 0)
        self.speed = 2
        self.offset = (-90, -90)
        #Creating hitboxes
        self.hitbox = self.rect.inflate(self.offset[0], self.offset[1])
        self.hitbox.y = pos[1] + 30

    #def movement(self, mov):
        #self.direction.x = mov

    def boundary_collisions(self, boundaries):
        #Implementing changing direction when colliding with barrier
        self.hitbox.x += self.direction.x * self.speed
        for boundary in boundaries.sprites():
            if boundary.rect.colliderect(self.hitbox):
                if self.direction.x > 0:
                    self.hitbox.right = boundary.rect.left
                    self.direction.x = -1
                elif self.direction.x < 0:
                    self.hitbox.left = boundary.rect.right
                    self.direction.x = 1

        """
        self.rect.x += self.direction.x * self.speed
        time.sleep(2)
        self.direction.x = 2
        time.sleep(2)
        self.direction.x = -2
        
        x_shift,
        """

    def update(self, x_shift, boundaries):
        self.hitbox.x += x_shift
        self.boundary_collisions(boundaries)
        self.rect = self.hitbox.inflate(self.offset[0] * -1, self.offset[1] * -1)
        #self.rect.y -= 15

    def draw_hitbox_two(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 1)

