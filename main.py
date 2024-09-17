import pygame, random
from pygame.locals import *
from sys import exit
from resources.assets import spritesCreate, introConfig, jogadorConfig

pygame.init()                                       #iniciamos o pygame
relogio = pygame.time.Clock()                       #Definindo o parametro para criar o FPS
largura, altura = 800, 640                          #constante do tamanho da tela
tela = pygame.display.set_mode((largura, altura))   #criamos a tela do jogo
pygame.display.set_caption('Naughty Cats')          #demos nomes pra tela do jogo
fonte = pygame.font.SysFont('arial', 40, True, True)#Criando a fonte para escrever na tela
pygame.mouse.set_visible(False)                     #setando o mouse pra invisivel
ITERACOES = 30                                      #uma constante aqui só para debug
GRAVIDADE = 0.5                                     #constante para criar a gravidade
FORCA_PULO = 15                                     # Força do pulo aumentada para 12

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

#gerar as mascaras
jogadorMasc = pygame.mask.from_surface(jogadorSprite[0])

# Sons
somEstrela = pygame.mixer.Sound('resources/sounds/estrela.mp3')
somMiado = pygame.mixer.Sound('./resources/sounds/miado.mp3')
somTrilha = pygame.mixer.Sound('resources/sounds/trilha.mp3')
somEstrela.set_volume(0.05)
somAtivado = True

# Exibe o texto inicial e aguarda a entrada
introConfig.colocarTexto('Naughty Cats', fonte, tela, largura / 3, altura / 2)
introConfig.colocarTexto('Pressione uma tecla para começar.', fonte, tela, largura / 5, altura / 3)
pygame.display.update()
introConfig.aguardarEntrada()

while True:                                         #inica o laço do jogo
    relogio.tick(24)                                #o jogo roda a 24 fps
    rodando = True    

    pontuacao = 0                                   #inicia a pontuação
    estrelas = []                                   #a lista de entrelas é iniciada
    
    teclas = {'esquerda': False, 'direita': False, 'cima': False, 'baixo': False}                       #definindo o dicionario que guardará as direções
    numInteracoes = 0                                                                                   #marca o numero de interações
    
    jogador = {                                                                                         # criando jogador
    'objRect': pygame.Rect(300, 100, 64, 64),
    'imagem': jogadorSprite[0],
    'vel': 0.6,
    'velY': 0,
    'noChao': True,
    'pulando': False,
    'forca_pulo': 10,
    'tempo_pulo': 0
    }
    
    plataformas = [{'objRect': pygame.Rect(0, altura - 50, largura, 50)}]  # Plataforma no fundo da tela
    
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                introConfig.finalizar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    introConfig.finalizar()

                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas['esquerda'] = True
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas['direita'] = True
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    if jogador['noChao']:  # Só pular se estiver no chão
                        jogador['velY'] = -FORCA_PULO
                        jogador['noChao'] = False  # Após o pulo, o jogador já não está mais no chão
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas['baixo'] = True
                if evento.key == pygame.K_m:
                    if somAtivado:
                        somTrilha.stop()
                        somAtivado = False 
                    else:
                        somTrilha.play(-1, 0)
                        somAtivado = True
                        
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas['esquerda'] = False
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas['direita'] = False
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas['baixo'] = False

        # Aplicando gravidade
        if not jogador['noChao']:
            jogador['velY'] += GRAVIDADE
        
        # Atualizando a posição vertical do jogador
        jogador['objRect'].y += jogador['velY']

        # Verificar se o jogador colidiu com o chão (plataforma)
        jogadorConfig.verificar_colisao_chao(jogador, plataformas)
        
        # Atualizando o movimento do jogador no eixo X
        jogadorConfig.moverJogador(jogador, teclas, (largura, altura))

        numInteracoes += 1
        if numInteracoes >= ITERACOES:
            numInteracoes = 0                                                                       # adicionando estrela
            posY = random.randint(0, altura - 64)
            posX = random.randint(0, largura - 64)
            estrelas.append({'objRect': pygame.Rect(posX, posY, 64, 64), 'imagem': arquivoEstrela})

        tela.blit(cenarioExterno, (0, 0))
        tela.blit(cenarioInterior, (0, 0))                                                          # preenchendo o fundo de janela com a sua imagem
        
        introConfig.colocarTexto('Pontuação: ' + str(pontuacao), fonte, tela, 10, 0)                      # Colocando as pontuações.

        tela.blit(jogador['imagem'], jogador['objRect'])                                             # desenhando jogador
        
        for estrela in estrelas[:]:                                                                 # checando se jogador pegou estrela
            deslocamento = (estrela['objRect'].x - jogador['objRect'].x, estrela['objRect'].y - jogador['objRect'].y)
            if jogadorMasc.overlap(pygame.mask.from_surface(arquivoEstrela), deslocamento):
                estrelas.remove(estrela)
                pontuacao += 50
                if somAtivado:
                    somEstrela.play()

        for estrela in estrelas:                                                                    # desenhando estrelas
            tela.blit(estrela['imagem'], estrela['objRect'])

        pygame.display.update()                                                                     # mostra tudo o que foi desenhado na tela

    introConfig.colocarTexto('GAME OVER', fonte, tela, (largura / 3), (altura / 3))
    
    introConfig.colocarTexto('Pressione uma tecla para jogar.', fonte, tela, (largura / 0), (altura / 2))
    pygame.display.update()
    
    introConfig.aguardarEntrada()                                                                         # Aguardando entrada por teclado para reiniciar o jogo ou sair.