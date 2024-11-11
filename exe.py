import pygame
from pygame.locals import *

pygame.init()

telaLargura = 1000
telaAltura = 1000

screen = pygame.dysplay.set_mode((telaAltura, telaAltura))
pygame.display.set_caption('Naughty Cat 2.1')

def finalizar(self):
    # Termina o programa.
    pygame.quit()
    exit()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            finalizar()
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                finalizar()
                
                    
