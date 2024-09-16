import pygame
import os

# Criar uma instância da classe SpritesheetLoader para o jogador
largura_sprite = 64  # Largura de cada sprite
altura_sprite = 64   # Altura de cada sprite
linhas = 10          # Número de linhas na spritesheet
colunas = 10         # Número de colunas na spritesheet

class SpritesheetLoader:
    def __init__(self, imagem):
        """
        Inicializa o carregador de spritesheet.
        
        :param imagem: Imagem carregada (spritesheet) já passada como variável.
        :param largura_sprite: Largura de cada sprite.
        :param altura_sprite: Altura de cada sprite.
        """
        self.spritesheet = imagem
        self.largura_sprite = largura_sprite
        self.altura_sprite = altura_sprite

    def cortar_sprites(self, linhas, colunas):
        """
        Corta a spritesheet em sprites individuais.
        
        :param linhas: Número de linhas na spritesheet.
        :param colunas: Número de colunas na spritesheet.
        :return: Lista de sprites cortados.
        """
        sprites = []
        for linha in range(linhas):
            for coluna in range(colunas):
                x = coluna * self.largura_sprite
                y = linha * self.altura_sprite
                sprite = self.spritesheet.subsurface(pygame.Rect(x, y, self.largura_sprite, self.altura_sprite))
                sprites.append(sprite)
        return sprites
