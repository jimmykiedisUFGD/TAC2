import pygame, random       #importa a biblioteca de criação de jogos
from pygame.locals import * #importar as constantes já definidas pelo pygame 
from sys import exit        #importar a função de fechar o jogo

pygame.init()

relogio = pygame.time.Clock()                       #Definindo o parametro para criar o FPS

# finaliza o jogo
def finalizar():
    pygame.quit()
    exit()

# carregando imagens
cenarioInterior = pygame.image.load('./resources/image/projetoInterior.png')
cenarioExterno = pygame.image.load('./resources/image/projetoExterior.png')
imagemJogador = pygame.image.load('./resources/image/skinPlayer1.png')
imagemEstrela = pygame.image.load('./resources/image/estrela.png')

#Criando a janela
janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))   #Criação da tela do jogo
pygame.display.set_caption('Naughty Cat')           #Colocando titulo na janela
fonte = pygame.font.SysFont('arial', 40, True,True) #Criando a fonte para escrever na tela

#carregando imagens
cenarioInterior = cenarioInterior.convert_alpha()
imagemJogador = imagemJogador.convert_alpha()
imagemEstrela = imagemEstrela.convert_alpha()

def colocarTexto(texto, fonte, janela, x, y):
    # Coloca na posição (x,y) da janela o texto com a fonte passados por argumento.
    objTexto = fonte.render(texto, True, CORTEXTO)
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

# Ocultando o cursor e redimensionando a imagem de fundo.
pygame.mouse.set_visible(False)
cenarioInteriorRedim = pygame.transform.scale(cenarioInterior,(LARGURAJANELA, ALTURAJANELA))
            
# Tela de inicio.
colocarTexto('Tutubarão', fonte, janela, LARGURAJANELA / 5, ALTURAJANELA / 3)
colocarTexto('Pressione uma tecla para começar.', fonte, janela, LARGURAJANELA / 20 , ALTURAJANELA / 2)
pygame.display.update()
aguardarEntrada()

while True:                                      #inica o laço do jogo
    relogio.tick(35)                                #o jogo roda a 35 fps
    rodando = True              #variavel para avisar o jogo quando deve fechar

    # Configurando inicio do jogo
    pontuacao = 0
    estrelas = []

    # definindo o dicionario que guardará as direções
    teclas = {'esquerda': False, 'direita': False, 'cima': False, 'baixo': False}
    numInteracoes = 0                               #marca o numero de interações

    # criando jogador
    jogador = {'objRect': pygame.Rect(300, 100, LARGURAJOGADOR, ALTURAJOGADOR), 'imagem': imagemJogador, 'vel': VEL}

    while rodando:
        # checando eventos
        for evento in pygame.event.get():                #inicia o laço dos eventos de entrada do jogo
            # verificando se for quit
            if evento.type == pygame.QUIT:                      #caso clicar no X da tela
                finalizar()

            # Pressionar alguma tecla
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    finalizar()
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas['esquerda'] = True
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas['direita'] = True
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas['cima'] = True
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas['baixo'] = True
                if evento.key == pygame.K_m:
                    if somAtivado:
                        pygame.mixer.music.stop()
                        somAtivado = False
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                        somAtivado = True

            # quando uma tecla é solta
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas['esquerda'] = False
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas['direita'] = False
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas['cima'] = False
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas['baixo'] = False

        numInteracoes += 1
        if numInteracoes >= ITERACOES:
            # adicionando estrela
            numInteracoes = 0
            posY = random.randint(0, ALTURAJANELA - ALTURAESTRELA)
            posX = random.randint(0, LARGURAJANELA - LARGURAESTRELA)
            estrelas.append({'objRect': pygame.Rect(posX, posY,LARGURAESTRELA, ALTURAESTRELA),                                
                        'imagem': imagemEstrela})
        
        # preenchendo o fundo de janela com a sua imagem
        janela.blit(cenarioInterior, (0,0))

        # Colocando as pontuações.
        colocarTexto('Pontuação: ' + str(pontuacao), fonte, janela, 10, 0)

        # movendo o jogador
        moverJogador(jogador, teclas, (LARGURAJANELA, ALTURAJANELA))    

        # desenhando jogador
        janela.blit(jogador['imagem'], jogador['objRect'])


        # mostra tudo o que foi desenhado na tela
        pygame.display.update()

        # definindo o FPS
        relogio.tick(50)

    colocarTexto('GAME OVER', fonte, janela, (LARGURAJANELA / 3), (ALTURAJANELA / 3))
    colocarTexto('Pressione uma tecla para jogar.', fonte, janela, (LARGURAJANELA / 10), (ALTURAJANELA / 2))
    pygame.display.update()

    # Aguardando entrada por teclado para reiniciar o jogo ou sair.
    aguardarEntrada()