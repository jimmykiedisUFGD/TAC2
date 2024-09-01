import pygame               #importa a biblioteca de criação de jogos
from pygame.locals import * #importar as constantes já definidas pelo pygame 
from sys import exit        #importar a função de fechar o jogo

pygame.init()               #inicia a bibliote

rodando = True              #variavel para avisar o jogo quando deve fechar

largura = 640               #definimos a largura da tela
altura = 480                #definimos a altura da tela

pontos = 0                  #declaramos a pontuação do jogo (ps. zerar quando quando der gameover)

tela = pygame.display.set_mode((largura, altura))   #Criação da tela do jogo
pygame.display.set_caption('Naughty Cat')           #Colocando titulo na janela
fonte = pygame.font.SysFont('arial', 40, True,True) #Criando a fonte para escrever na tela

relogio = pygame.time.Clock()                       #Definindo o parametro para criar o FPS

while rodando:                                      #inica o laço do jogo
    relogio.tick(24)                                #o jogo roda a 24 fps
    tela.fill((255,255,255))

    for event in pygame.event.get():                #inicia o laço dos eventos de entrada do jogo
        if event.type == QUIT:                      #caso clicar no X da tela
            rodando = False                         #nosso laço para
            pygame.quit()                           #nosso jogo para
            exit()                                  #a janela fecha

    pygame.display.update()                         #tela atualiza 24x por segundo