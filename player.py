import pygame
from settings import gravity
from bullet import Bullet
from support import import_folder



class Player(pygame.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        #State of player
        self.is_alive = True
        self.won = False
        #Graphics

        self.animations = {}
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.05

        #Player variables
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0)
        self.shots = 0
        self.message = False
        self.speed = 4
        self.jump_speed = -16
        self.bullets = pygame.sprite.Group()
        self.firing = False
        self.status = "idle"
        self.offset = (-40, -11)
        #Creating hitboxes
        self.hitbox = self.rect.inflate(self.offset[0], self.offset[1])
        #Adding jumping music to program
        self.jump_sound = pygame.mixer.Sound("sounds/effects/mixkit-player-jumping-in-a-video-game-2043 (1).wav")
        self.key = False


    def animate(self):
        #Sequence of images usef for animation
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]

    def import_character_assets(self):
        #Adding images to for an animation
        character_path = "graphics/player/"

        self.animations = {"idle":[], "run_right":[], "run_left":[], "jump":[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)


    def get_input(self):
        #Detecting key presses and correspondening game mechnaics

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        if self.direction.y <= 0.8:
            if keys[pygame.K_UP]:
                self.jump()
        if self.shots > 0:
            if keys[pygame.K_SPACE] and not self.firing:
                self.fire()
                self.firing = True
                self.shots -= 1
            elif not keys[pygame.K_SPACE] and self.firing:
                self.firing = False
        else:
            self.message = False

    def get_status(self):
        #Trigger the running of particularanimations
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.x == 0:
            self.status = "idle"
        elif self.direction.x > 0:
            self.status = "run_right"
        else:
            self.status = "run_left"

    def fire(self):
        #Firing bullets
        bullet = Bullet((self.rect.centerx, self.rect.centery), self.direction.x)
        self.bullets.add(bullet)

    def jump(self):
        #Jumping
        #print(self.status, self.direction.x, self.direction.y)
        if self.status != "jump" and self.direction.y == 0:
            self.status = "jump"
            self.direction.y = self.jump_speed
            pygame.mixer.Sound.play(self.jump_sound)


    def horizontal_movement_collision(self, tiles):
        #Collisions with map design horizontally
        self.hitbox.x += self.direction.x * self.speed

        for tile in tiles.sprites():
            if tile.rect.colliderect(self.hitbox):
                if self.direction.x < 0:
                    self.hitbox.left = tile.rect.right
                elif self.direction.x > 0:
                    self.hitbox.right = tile.rect.left

    def vertical_movement_collision(self, tiles):
        #Collisions with map design vertically
        self.apply_gravity()

        for tile in tiles.sprites():
            if tile.rect.colliderect(self.hitbox):
                if self.direction.y > 0:
                    self.hitbox.bottom = tile.rect.top
                    self.direction.y = 0
                if self.direction.y < 0:
                    self.hitbox.top = tile.rect.bottom
                    self.direction.y = 0



    def apply_gravity(self):
        #Adding gravity
        self.direction.y += gravity
        self.hitbox.y += self.direction.y

    def update(self, tiles):
        #Runnign previous functions
        self.horizontal_movement_collision(tiles)
        self.vertical_movement_collision(tiles)
        self.get_input()
        self.rect = self.hitbox.inflate(self.offset[0] * -1, self.offset[1] * -1)
        self.rect.y -= 5
        self.bullets.update()
        #self.draw_hitbox()
        self.get_status()
        self.animate()
        #print(self.speed)


    def draw_hitbox(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.hitbox, 1)

    def draw_bullets(self, surface):
        #Displaying bulets
        self.bullets.draw(surface)
