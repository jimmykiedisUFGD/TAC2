import pygame
from pygame.locals import *
from resources.assets import Sprite, introConfig, jogadorConfig

pygame.init()

telaLargura = 1000
telaAltura = 1000

tela = pygame.display.set_mode((telaAltura, telaAltura))
pygame.display.set_caption('Naughty Cat 2.1')

# Carregando imagens
cenarioInterior = pygame.image.load('./resources/image/projetoInterior.png').convert_alpha()
cenarioExterno = pygame.image.load('./resources/image/projetoExterior.png').convert_alpha()
arquivoJogador = pygame.image.load('./resources/image/projetoPlayer.png').convert_alpha()
arquivoPlataformasCenario = pygame.image.load('./resources/image/projetoPlataformas.png').convert_alpha()
arquivoObjetosCenario = pygame.image.load('./resources/image/projetoObjetos.png').convert_alpha()
arquivoEstrela = pygame.image.load('./resources/image/estrela.png').convert_alpha()

# Criando o carregador de sprites para o jogador
jogadorSpriteLoader = Sprite.SpritesheetLoader(arquivoJogador)
jogadorSprite = jogadorSpriteLoader.cortar_sprites(10, 10)

#criando o carregador de sprites das plataformas de cenário
plataformaSpriteLoader = Sprite.SpritesheetLoader(arquivoPlataformasCenario)
plataformaSprite = plataformaSpriteLoader.cortar_sprites(10, 10)

#criando o carregador de sprites dos objetos de cenário
objetosSpriteLoader = Sprite.SpritesheetLoader(arquivoObjetosCenario)
objetosSprite = objetosSpriteLoader.cortar_sprites(10, 10)


rodando = True
while rodando:
    
    tela.blit(cenarioExterno,(0,0))
    tela.blit(cenarioInterior,(0,0))
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
                
    pygame.display.update()  
                
pygame.quit()
                
                    
