import pygame, random
from pygame.locals import *
from sys import exit
from resources.assets import spritesCreate, intro

pygame.init()                                       #iniciamos o pygame
relogio = pygame.time.Clock()                       #Definindo o parametro para criar o FPS
largura, altura = 800, 640                          #constante do tamanho da tela
tela = pygame.display.set_mode((largura, altura))   #criamos a tela do jogo
pygame.display.set_caption('Naughty Cats')          #demos nomes pra tela do jogo
fonte = pygame.font.SysFont('arial', 40, True, True)#Criando a fonte para escrever na tela
pygame.mouse.set_visible(False)                     #setando o mouse pra invisivel
ITERACOES = 30                                      #uma constante aqui só para debug

# Carregando imagens
cenarioInterior = pygame.image.load('./resources/image/projetoInterior.png').convert_alpha()
cenarioExterno = pygame.image.load('./resources/image/projetoExterior.png').convert_alpha()
arquivoJogador = pygame.image.load('./resources/image/projetoPlayer.png').convert_alpha()
arquivoPlataformasCenario = pygame.image.load('./resources/image/projetoPlataformas.png').convert_alpha()
arquivoObjetosCenario = pygame.image.load('./resources/image/projetoObjetos.png').convert_alpha()
arquivoEstrela = pygame.image.load('./resources/image/estrela.png').convert_alpha()

# Criando o carregador de sprites para o jogador
jogadorSpriteLoader = spritesCreate.SpritesheetLoader(arquivoJogador)
jogadorSprite = jogadorSpriteLoader.cortar_sprites(10, 10)

#criando o carregador de sprites das plataformas de cenário
plataformaSpriteLoader = spritesCreate.SpritesheetLoader(arquivoPlataformasCenario)
plataformaSprite = plataformaSpriteLoader.cortar_sprites(10, 10)

#criando o carregador de sprites dos objetos de cenário
objetosSpriteLoader = spritesCreate.SpritesheetLoader(arquivoObjetosCenario)
objetosSprite = objetosSpriteLoader.cortar_sprites(10, 10)

# Sons
somEstrela = pygame.mixer.Sound('resources/sounds/estrela.mp3')
somMiado = pygame.mixer.Sound('./resources/sounds/miado.mp3')
somTrilha = pygame.mixer.Sound('resources/sounds/trilha.mp3')
somEstrela.set_volume(0.05)
somAtivado = True

# Exibe o texto inicial e aguarda a entrada
intro.colocarTexto('Naughty Cats', fonte, tela, largura / 3, altura / 2)
intro.colocarTexto('Pressione uma tecla para começar.', fonte, tela, largura / 5, altura / 3)
pygame.display.update()
intro.aguardarEntrada()

# Função para mover o jogador
def moverJogador(jogador, teclas, limites):
    if teclas['esquerda'] and jogador['objRect'].left > 0:
        jogador['objRect'].x -= jogador['vel']
    if teclas['direita'] and jogador['objRect'].right < limites[0]:
        jogador['objRect'].x += jogador['vel']
    if teclas['cima'] and jogador['objRect'].top > 0:
        jogador['objRect'].y -= jogador['vel']
    if teclas['baixo'] and jogador['objRect'].bottom < limites[1]:
        jogador['objRect'].y += jogador['vel']

while True:                                         #inica o laço do jogo
    relogio.tick(24)                                #o jogo roda a 24 fps
    rodando = True    

    pontuacao = 0                                   #inicia a pontuação
    estrelas = []                                   #a lista de entrelas é iniciada
    
    teclas = {'esquerda': False, 'direita': False, 'cima': False, 'baixo': False}                       #definindo o dicionario que guardará as direções
    numInteracoes = 0                                                                                   #marca o numero de interações
    
    jogador = {'objRect': pygame.Rect(300, 100, 64, 64), 'imagem': jogadorSprite[0], 'vel': 0.6}       # criando jogador
    
    while rodando:
        for evento in pygame.event.get():                       #inicia o laço dos eventos de entrada do jogo
            if evento.type == pygame.QUIT:                      #caso clicar no X da tela
                intro.finalizar()                               # verificado, ele fecha

            if evento.type == pygame.KEYDOWN:                   # Pressionar alguma tecla
                if evento.key == pygame.K_ESCAPE:
                    intro.finalizar()
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
                        somTrilha.stop()
                        somAtivado = False 
                    else:
                        somTrilha.play(-1, 0)  # '-1' para repetir indefinidamente
                        somAtivado = True
                           
              
            if evento.type == pygame.KEYUP:                     # quando uma tecla é solta
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
            numInteracoes = 0                                                                       # adicionando estrela
            posY = random.randint(0, altura - 64)
            posX = random.randint(0, largura - 64)
            estrelas.append({'objRect': pygame.Rect(posX, posY, 64, 64), 'imagem': arquivoEstrela})

        tela.blit(cenarioExterno, (0, 0))
        tela.blit(cenarioInterior, (0, 0))                                                          # preenchendo o fundo de janela com a sua imagem
        
        intro.colocarTexto('Pontuação: ' + str(pontuacao), fonte, tela, 10, 0)                      # Colocando as pontuações.
        
        moverJogador(jogador, teclas, (largura, altura))                                             # movendo o jogador

        tela.blit(jogador['imagem'], jogador['objRect'])                                             # desenhando jogador
        
        for estrela in estrelas[:]:                                                                 # checando se jogador pegou estrela
            coletouEstrela = jogador['objRect'].colliderect(estrela['objRect'])
            if coletouEstrela: 
                estrelas.remove(estrela)
                pontuacao += 50
            if coletouEstrela and somAtivado: somEstrela.play()

        for estrela in estrelas:                                                                    # desenhando estrelas
            tela.blit(estrela['imagem'], estrela['objRect'])

        pygame.display.update()                                                                     # mostra tudo o que foi desenhado na tela

    intro.colocarTexto('GAME OVER', fonte, tela, (largura / 3), (altura / 3))
    
    intro.colocarTexto('Pressione uma tecla para jogar.', fonte, tela, (largura / 0), (altura / 2))
    pygame.display.update()
    
    intro.aguardarEntrada()                                                                         # Aguardando entrada por teclado para reiniciar o jogo ou sair.