import pygame, sys
from settings import *
from levelone import Level

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)
background_img = pygame.image.load("/Users/michalgrabowski/PycharmProjects/platformgame/Graphics/background/background_layer_1.png")
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

#Game loop
while True:
    screen.blit(background_img,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            level = Level(level_map, screen)

    level.run()
    pygame.display.update()
    clock.tick(fps)
