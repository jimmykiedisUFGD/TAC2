import pygame, numpy
from .Sprites import Sprite
from pygame.locals import *
from .Game import settings
import sys

class Player(Sprite):
    def __init__(self, startx, starty):
        super().__init__(settings.player_stand[0], settings.player_stand_masks[0], startx, starty)
        self.stand_image = self.image
        
        # jump
        self.jump_cycle = settings.player_jump
        self.jump_cycle_masks = settings.player_jump_masks
        self.jump_cycle_flip = settings.player_jump_flip
        self.jump_cycle_flip_masks = settings.player_jump_flip_masks
        
        #stand
        self.stand_cycle = settings.player_stand
        self.stand_cycle_masks = settings.player_stand_masks
        self.stand_cycle_flip = settings.player_stand_flip
        self.stand_cycle_flip_masks = settings.player_stand_flip_masks
        
        #walk       
        self.walk_cycle = settings.player_walk
        self.walk_cycle_masks = settings.player_walk_masks
        self.walk_cycle_flip = settings.player_walk_flip
        self.walk_cycle_flip_masks = settings.player_walk_flip_masks
        
        self.facing_left = False

        self.speed = 4
        self.jumpspeed = 11
        self.vsp = 0
        self.gravity = 2.8
        self.min_jumpspeed = 3   
        self.walk_delay = 7    
        self.jump_delay = 40   
        self.stand_delay = 10  
        self.idle = 200
        self.count_idle = 0        
        self.prev_key = pygame.key.get_pressed()

    def update(self, boxes, estrelas):
        self.hsp = 0
        onground = self.check_collision(0, 1, boxes)
        self.check_keys(onground)
        
        # gravity
        if self.vsp < 10 and not onground:  # 9.8 rounded up
            if self.facing_left:               
                self.animation(self.jump_cycle_flip, self.jump_cycle_flip_masks,
                               self.jump_delay, 'jump')
            else:
                self.animation(self.jump_cycle, self.jump_cycle_masks,
                               self.jump_delay, 'jump')
            self.walk_count += 1
            if self.walk_count > self.walk_delay:
                self.vsp += self.gravity
                self.walk_count = 0

        if onground and self.vsp > 0:
            self.vsp = 0

        # movement
        self.move(self.hsp, self.vsp, boxes)
        
        #collide estrela
        self.collide_estrela(estrelas)          
        
    
    def collide_estrela(self, estrelas:pygame.sprite.Group):
        #collide = False
        for estrela in estrelas:
            if self.rect.colliderect(estrela.rect):
                offset = (estrela.rect.x - self.rect.x, estrela.rect.y - self.rect.y)
                collide = self.mask.overlap(estrela.mask, offset) 
                if collide:
                    estrela.kill() 
        #return collide      


    def check_keys(self, onground):
        # check keys
        key = pygame.key.get_pressed()
        # if user clicks on cross button, close the game 
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and
                                        event.key == K_ESCAPE): 
                pygame.quit() 
                sys.exit()         
        if key[pygame.K_LEFT]:
            self.facing_left = True
            self.count_idle = 0
            if onground:
                self.animation(self.walk_cycle_flip, self.walk_cycle_flip_masks,
                               self.walk_delay, 'walk')
            self.hsp = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            self.count_idle = 0
            if onground:
                self.animation(self.walk_cycle, self.walk_cycle_masks,self.walk_delay, 'walk')
            self.hsp = self.speed
        else:
            self.image = self.stand_image
            self.mask = settings.player_stand_masks[0]            
            self.count_idle += 1
            if self.count_idle > self.idle:
                #correct sprite position
                #self.rect.bottomleft = settings.player_stand[0].get_rect().bottomleft
                if self.facing_left:
                    self.animation(self.stand_cycle_flip, self.stand_cycle_flip_masks, self.stand_delay)
                else:
                    self.animation(self.stand_cycle, self.stand_cycle_masks,self.stand_delay)

        if key[pygame.K_UP] and onground:
            self.count_idle = 0
            self.vsp = -self.jumpspeed

        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed
        self.prev_key = key


    def move(self, x, y, boxes):
        dx = x
        dy = y
        while self.check_collision(0, dy, boxes):
            dy -= numpy.sign(dy)
        while self.check_collision(dx, dy, boxes):
            dx -= numpy.sign(dx)
        self.rect.move_ip([dx, dy])


    def check_collision(self, x, y, grounds):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, grounds)        
        self.rect.move_ip([-x, -y])
        return collide