import pygame
from pygame.locals import *

pygame.init()

telaLargura = 1000
telaAltura = 1000

tela = pygame.dysplay.set_mode((telaAltura, telaAltura))
pygame.display.set_caption('Naughty Cat 2.1')

cenarioInterior = pygame.image.load ('resources/image/projetoInterior.png')
cenarioExterior = pygame.image.load ('resources/image/projetoExterior.png')

rodando = True
while rodando:
    
    tela.blit(cenarioExterior,(0,0))
    tela.blit(cenarioInterior,(0,0))
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
                
    pygame.display.update()  
                
pygame.quit()
                
                    
