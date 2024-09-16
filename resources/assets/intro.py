import pygame
from sys import exit 

def finalizar():                                    #primeiro função que faremos será para finalizar o jogo
    pygame.quit()
    exit()

def colocarTexto(texto, fonte, janela, x, y):
    # Coloca na posição (x,y) da janela o texto com a fonte passados por argumento.
    objTexto = fonte.render(texto, True, (255,255,255))
    rectTexto = objTexto.get_rect()
    rectTexto.topleft = (x, y)
    janela.blit(objTexto, rectTexto)
    
def aguardarEntrada():
    # Aguarda entrada por teclado ou clique do mouse no “x” da janela.
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                finalizar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    finalizar()
                return