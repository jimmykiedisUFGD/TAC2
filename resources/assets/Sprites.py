import pygame
from .Game import settings

class Sprite(pygame.sprite.Sprite):
    def __init__(self, image:pygame.Surface, mask:pygame.Mask, startx:int, starty:int):
        '''General sprite for all objects
            Starting image and position x,y
        '''
        super().__init__()

        self.image:pygame.Surface = image
        self.mask:pygame.Mask = mask
         # return a width and height of an image
        self.size = self.image.get_size() 
        
        self.rect = self.image.get_rect()
        self.rect.bottomleft = [startx, starty]  
        
        self.walk_animation_index = 0
        self.jump_animation_index = 0
        self.stand_animation_index = 0
        
        self.walk_count = 0 
        self.jump_count = 0 
        self.stand_count = 0       

    def update(self):
        pass

    def draw(self, screen):        
        # draw bigger image to screen at x,y position
        screen.blit(self.image, self.rect)
        
        #mask debug       
        if settings.debug: screen.blit(self.mask.to_surface(), self.rect)
        
    def animation(self, images:list, masks:list, delay:int, type='stand'):
        '''Enter with surface list and its masks
        plus max delay to change surface and type:
        "stand" or "jump" or "walk"
        '''     
        if type == 'stand':
             index = self.stand_animation_index 
             counter = self.stand_count  
        if type == 'jump':
             index = self.jump_animation_index 
             counter = self.jump_count 
        if type == 'walk':
             index = self.walk_animation_index 
             counter = self.walk_count  
                  
        # change img and mask after delay
        self.image = images[index]         
        self.mask = masks[index]   
        if index < len(images)-1:
            counter += 1
            if counter > delay:                
                index += 1
                counter = 0
        else:
           index = 0  
                   
        if type == 'stand':
             self.stand_animation_index = index
             self.stand_count = counter 
        if type == 'jump':
             self.jump_animation_index = index
             self.jump_count = counter 
        if type == 'walk':
             self.walk_animation_index = index
             self.walk_count = counter 
        
        