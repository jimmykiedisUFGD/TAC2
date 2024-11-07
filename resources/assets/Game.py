import pygame
from .Settings import *
from .Player import Player
from .Objects import Box, Estrela

class NaughtCats:
    def play(self, debug:bool):
        settings.setup(debug)
        player = Player(LARGURA_TELA*0.1, ALTURA_TELA*0.7)

        boxes = pygame.sprite.Group()        
        box = Box(0, ALTURA_TELA)
        boxes.add(box)
        for i in range(7):            
            box = Box(box.size[0]*i, ALTURA_TELA)
            boxes.add(box)

        box = Box(0, ALTURA_TELA-box.size[1]*2)
        boxes.add(box)
        box = Box(box.size[0]*6, ALTURA_TELA-box.size[1])
        boxes.add(box)
        
        estrelas = pygame.sprite.Group()        
        estrelas.add(Estrela(LARGURA_TELA*0.5,ALTURA_TELA-box.size[1]))
        
        while True:
            pygame.event.pump()

            settings.screen.fill(BACKGROUND)
            
            # Draw loop
            player.update(boxes, estrelas)
            boxes.update()
            estrelas.update()


            #player.draw(settings.screen)
            #boxes.draw(settings.screen)
            #for estrela in estrelas:
            #    estrela.draw(settings.screen)

            if settings.debug:
                for estrela in estrelas:
                    estrela.draw(settings.screen)
                for box in boxes:
                    box.draw(settings.screen)
            else:
                boxes.draw(settings.screen)
                estrelas.draw(settings.screen)            
            player.draw(settings.screen)
            
            pygame.display.flip()
            settings.relogio.tick(60)

    def terminar(self):
        # Termina o programa.
        pygame.quit()
        exit()

    def aguardarEntrada(self):
        # Aguarda entrada por teclado ou clique do mouse no “x” da janela.
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    NaughtCats.terminar()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        NaughtCats.terminar()
                    return

    def colocarTexto(self, texto, fonte, janela, x, y):
        # Coloca na posição (x,y) da janela o texto com a fonte passados por argumento.
        objTexto = fonte.render(texto, True, CORTEXTO)
        rectTexto = objTexto.get_rect()
        rectTexto.topleft = (x, y)
        janela.blit(objTexto, rectTexto)
    