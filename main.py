import pygame, random
from pygame.locals import *
from sys import exit
import os

pygame.init()                                       #iniciamos o pygame
largura, altura = 800, 640                          #constante do tamanho da tela
spriteLarg = spiteAltu = 64                         #constante do tamanho das sprite sheets
tela = pygame.display.set_mode((largura, altura))   #criamos a tela do jogo
pygame.display.set_caption('Nautghty Cats')         #demos nomes pra tela do jogo

cenarioInterior = pygame.image.load('./resources/image/projetoInterior.png').convert_alpha()            #carregaremos os cenários
cenarioExterno = pygame.image.load('./resources/image/projetoExterior.png').convert_alpha()             #o externo será util
Jogador = pygame.image.load('./resources/image/resources/image/projetoPlayer.png').convert_alpha()      #carrega a sprite sheet do jogador
plataformasCenario = pygame.load('resources/image/projetoPlataformas.png').convert_alpha()              #carrega a sprite sheet das plataformas do cenário
objetosCenario = pygame.load('resources/image/projetoObjetos.png').convert_alpha()                      #carrega a sprite sheet dos objetos de cenário
Estrelas = pygame.image.load('./resources/image/estrela.png').convert_alpha()                           #carrega as estrelas


def finalizar():                                    #primeiro função que faremos será para finalizar o jogo
    pygame.quit()
    exit()
    
def cortarSprite(spriteSheet, spriteLarg, SpriteAltu, linhas, colunas):
    sprites = []
    for linha in range (linhas):
        for coluna in range (colunas):
            x = colunas * spriteLarg
            y = linhas * SpriteAltu
            imagem = spriteSheet.subsurface(pygame.Rect(x,y,spriteLarg,SpriteAltu))
            sprites.append(imagem)
    return sprites

def carregarSprite():