import pygame
from settings import tile_size, screen_width
from tileone import Tile
from player import Player
from enemy import Enemy
from boundary import Boundary
from coins import Coins
from chest import Chest
from finish import Finish
from spike import Spike

class Level:

    def __init__(self, level_data, surface):

        self.score = 0
        self.display_surface = surface
        self.tiles = pygame.sprite.Group()
        self.boundaries = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemy = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.chest = pygame.sprite.Group()
        self.finish = pygame.sprite.GroupSingle()
        self.spike = pygame.sprite.Group()
        self.setup_level(level_data)
        self.update_speed = 8
        pygame.mixer.music.load("sounds/music/audio_hero_Astral-Journey_SIPML_J-0201.mp3")
        pygame.mixer.music.play(-1)

        self.world_shift = 0


    def setup_level(self, layout):

        for row_index, row in enumerate(layout):
            for cell_index, cell in enumerate(row):
                x = cell_index * tile_size
                y = row_index * tile_size
                if cell == "x":
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == "p":
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                elif cell == "e":
                    enemy_sprite = Enemy((x, y))
                    self.enemy.add(enemy_sprite)
                elif cell == "b":
                    boundary = Boundary((x, y))
                    self.boundaries.add(boundary)
                elif cell == "c":
                    coin = Coins((x, y))
                    self.coins.add(coin)
                elif cell == "t":
                    chest = Chest((x, y), 1)
                    self.chest.add(chest)
                elif cell == "k":
                    chest = Chest((x, y), 0)
                    self.chest.add(chest)
                elif cell == "f":
                    finish = Finish((x, y))
                    self.finish.add(finish)
                elif cell == "s":
                    spike_sprite = Spike((x, y))
                    self.spike.add(spike_sprite)

#Figure out logic

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x > screen_width - (screen_width/5) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        elif player_x < screen_width/5 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = self.update_speed

    def run(self):
        if self.player.sprite.is_alive == True:

            self.tiles.update(self.world_shift)
            self.tiles.draw(self.display_surface)
            self.boundaries.update(self.world_shift)
            self.boundaries.draw(self.display_surface)
            self.chest.update(self.world_shift)
            self.chest.draw(self.display_surface)
            self.finish.draw(self.display_surface)
            self.finish.update(self.world_shift)
            self.player.update(self.tiles)
            self.player.draw(self.display_surface)
            #self.player.sprite.draw_hitbox(self.display_surface)
            """
            for e in self.enemy:
                e.draw_hitbox_two(self.display_surface)
            """
            self.coins.update(self.world_shift)
            self.coins.draw(self.display_surface)
            self.enemy.update(self.world_shift, self.boundaries)
            self.enemy.draw(self.display_surface)
            self.scroll_x()
            self.player.sprite.draw_bullets(self.display_surface)
            self.spike.update(self.world_shift)
            self.spike.draw(self.display_surface)
            """
            for s in self.spike:
                s.draw_hitbox_three(self.display_surface)
            """
            #Player chest collisions
            chest_collision = pygame.sprite.spritecollide(self.player.sprite, self.chest, False)
            for chest in chest_collision:
                if not chest.open:
                    if chest.type == 1:
                        chest.open = True
                        self.player.sprite.message = True
                        self.player.sprite.shots = 2
                        chest.image = pygame.image.load("/Users/michalgrabowski/PycharmProjects/platformgame/Graphics/chest/tile005.png")
                        chest.image = pygame.transform.scale(chest.image, (70, 70))
                    else:
                        chest.open = True
                        chest.image = pygame.image.load("/Users/michalgrabowski/PycharmProjects/platformgame/Graphics/chest/tile005.png")
                        chest.image = pygame.transform.scale(chest.image, (70, 70))
                        self.player.sprite.key = True

            #Checking if player is eligible for bullets
            if self.player.sprite.message:
                font3 = pygame.font.Font("freesansbold.ttf", 32)
                text2 = font3.render("Bullets: " + str(self.player.sprite.shots), True, (0, 250, 0))
                self.display_surface.blit(text2, (800,0))

            #Checking if player has key
            if self.player.sprite.key:
                font4 = pygame.font.Font("freesansbold.ttf", 20)
                text3 = font4.render("You got the key !", True, (0, 250, 0))
                self.display_surface.blit(text3, (400, 400))

            #Checking coin collection by the player
            coin_collection = pygame.sprite.spritecollide(self.player.sprite, self.coins, True)
            for coins in coin_collection:
                self.score += 1

            #Looking for enemy player collisions
            for e in self.enemy:
                collided_with = pygame.Rect.colliderect(self.player.sprite.hitbox, e.hitbox)
                if collided_with:
                    self.player.sprite.is_alive = False
                    e.kill()

            #Looking for enemy spikes collsisions
            for s in self.spike:
                collided_with_spike = pygame.Rect.colliderect(self.player.sprite.hitbox, s.hitbox)
                if collided_with_spike:
                    self.player.sprite.is_alive = False
                    s.kill()

            #Checking if finish line was reached
            collided_with_finish = pygame.Rect.colliderect(self.player.sprite.hitbox, self.finish.sprite.rect)
            if collided_with_finish:
                if self.player.sprite.key:
                    self.player.sprite.is_alive = False
                    self.player.sprite.won = True
                else:
                    self.player.sprite.hitbox.right = self.finish.sprite.rect.left
                    font4 = pygame.font.Font("freesansbold.ttf", 20)
                    text4 = font4.render("Did you forget the key?", True, (0, 250, 0))
                    self.display_surface.blit(text4, (400, 400))

            #Checking enemy bullet collisions
            bullet_collided_with_enemy = pygame.sprite.groupcollide(self.player.sprite.bullets, self.enemy, False, True)

            #Checking bullet collisions with wall
            collided_with_wall = pygame.sprite.groupcollide(self.player.sprite.bullets, self.tiles, True, False)

            font = pygame.font.Font("freesansbold.ttf", 32)
            text = font.render("Score: " + str(self.score), True, (0, 255, 0))
            self.display_surface.blit(text, (0,0))

        else:
            if not self.player.sprite.won:
                font1 = pygame.font.Font("freesansbold.ttf", 32)
                text1 = font1.render("You died", True, (255, 0, 0))
                text2 = font1.render("Press 'r' to continue", True, (255, 0, 0))
                self.display_surface.blit(text1, (550, 250))
                self.display_surface.blit(text2, (470, 300))
            else:
                font1 = pygame.font.Font("freesansbold.ttf", 32)
                text1 = font1.render("You won", True, (0, 255, 0))
                text2 = font1.render("Press 'r' to continue", True, (0, 255, 0))
                self.display_surface.blit(text1, (550, 250))
                self.display_surface.blit(text2, (470, 300))

