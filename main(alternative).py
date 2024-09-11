import pygame, random
from pygame.locals import *
from sys import exit

pygame.init()

# Variáveis e constantes do jogo
LARGURA_TELA = 640
ALTURA_TELA = 480
VEL = 5
ITERACOES = 30
CORTEXTO = (255, 255, 255)  # Cor do texto (branca)

# Inicialização
janela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Naughty Cat')
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont('arial', 40, True, True)

# Carregar imagens (já copiado)
cenarioInterno = pygame.image.load('./resources/image/projetoInterior.png').convert_alpha()
cenarioExterno = pygame.image.load('./resources/image/projetoExterior.png').convert_alpha()
imagemJogador = pygame.image.load('./resources/image/skinPlayer1.png').convert_alpha()
imagemEstrela = pygame.image.load('./resources/image/estrela.png').convert_alpha()

# Configurando imagens (já copiado)
LARGURA_FUNDO = cenarioInterno.get_width()
ALTURA_FUNDO = cenarioInterno.get_height()
LARGURA_JOGADOR = imagemJogador.get_width()
ALTURA_JOGADOR = imagemJogador.get_height()
LARGURAESTRELA = imagemEstrela.get_width()
ALTURAESTRELA = imagemEstrela.get_height()

# Função para mover o jogador e rolar o fundo (já copiado)
def moverJogador(jogador, teclas, x_fundo, largura_fundo):
    # Atualiza a posição do jogador
    if teclas['esquerda']:
        jogador['objRect'].x -= jogador['vel']
    if teclas['direita']:
        jogador['objRect'].x += jogador['vel']
    if teclas['cima']:
        jogador['objRect'].y -= jogador['vel']
    if teclas['baixo']:
        jogador['objRect'].y += jogador['vel']

    # Mantém o jogador dentro da tela
    jogador['objRect'].x = max(0, min(jogador['objRect'].x, LARGURA_TELA - LARGURA_JOGADOR))
    jogador['objRect'].y = max(0, min(jogador['objRect'].y, ALTURA_TELA - ALTURA_JOGADOR))

    # Movimento do fundo
    if jogador['objRect'].centerx > LARGURA_TELA // 2 and x_fundo > -(largura_fundo - LARGURA_TELA):
        x_fundo -= jogador['vel']
        jogador['objRect'].x -= jogador['vel']
    elif jogador['objRect'].centerx < LARGURA_TELA // 2 and x_fundo < 0:
        x_fundo += jogador['vel']
        jogador['objRect'].x += jogador['vel']

    return x_fundo

def colocarTexto(texto, fonte, janela, x, y):
    objTexto = fonte.render(texto, True, CORTEXTO)
    rectTexto = objTexto.get_rect()
    rectTexto.topleft = (x, y)
    janela.blit(objTexto, rectTexto)

def aguardarEntrada():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                finalizar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    finalizar()
                return

def finalizar():
    pygame.quit()
    exit()

# Ocultando o cursor
pygame.mouse.set_visible(False)

# Configurando o som (já copiado)
somEstrela = pygame.mixer.Sound('./resources/sounds/estrela.mp3')
somMiado = pygame.mixer.Sound('./resources/sounds/miado.mp3')
somTrilha = pygame.mixer.Sound('./resources/sounds/trilha.mp3')
somEstrela.set_volume(0.05)
somTrilha.set_volume(0.1)
somTrilha.play(-1)
somAtivado = True

# Tela de inicio
colocarTexto('Naughty Cats', fonte, janela, LARGURA_TELA / 5, ALTURA_TELA / 3)
colocarTexto('Pressione uma tecla para começar.', fonte, janela, LARGURA_TELA / 20, ALTURA_TELA / 2)
pygame.display.update()
aguardarEntrada()

# Loop principal do jogo
while True:
    relogio.tick(35)

    pontuacao = 0
    estrelas = []
    teclas = {'esquerda': False, 'direita': False, 'cima': False, 'baixo': False}
    numInteracoes = 0

    # Criando jogador (mudar de dicionário para classes)
    jogador = {'objRect': pygame.Rect(300, 100, LARGURA_JOGADOR, ALTURA_JOGADOR), 'imagem': imagemJogador, 'vel': VEL}

    x_fundo = 0  # Posição inicial do fundo
    
    rodando = True

    #recebendo a movimentação do jogador (já copiado)
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                finalizar()
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
            numInteracoes = 0
            posY = random.randint(0, ALTURA_TELA - ALTURAESTRELA)
            posX = random.randint(0, LARGURA_TELA - LARGURAESTRELA)
            estrelas.append({'objRect': pygame.Rect(posX, posY, LARGURAESTRELA, ALTURAESTRELA), 'imagem': imagemEstrela})

        # Movendo o jogador e o fundo
        x_fundo = moverJogador(jogador, teclas, x_fundo, LARGURA_FUNDO)

        # Desenhando o fundo
        janela.blit(cenarioInterno, (x_fundo, 0))

        # Colocando as pontuações
        colocarTexto('Pontuação: ' + str(pontuacao), fonte, janela, 10, 0)

        # Desenhando jogador
        janela.blit(jogador['imagem'], jogador['objRect'])

        # Checando se jogador pegou estrela (já copiado)
        for estrela in estrelas[:]:
            coletouEstrela = jogador['objRect'].colliderect(estrela['objRect'])
            if coletouEstrela:
                estrelas.remove(estrela)
                pontuacao += 50
                if somAtivado:
                    somEstrela.play()
        for estrela in estrelas:
            janela.blit(estrela['imagem'], estrela['objRect'])

        # Atualizando a tela
        pygame.display.update()

        # Definindo o FPS
        relogio.tick(50)

    colocarTexto('GAME OVER', fonte, janela, (LARGURA_TELA / 3), (ALTURA_TELA / 3))
    colocarTexto('Pressione uma tecla para jogar.', fonte, janela, (LARGURA_TELA / 10), (ALTURA_TELA / 2))
    pygame.display.update()

    aguardarEntrada()


'''Jogo(main):
Contém o loop principal.
Inicializa as outras classes (cenário, jogador, estrelas, som, etc.).
Controla o fluxo geral do jogo (iniciar, finalizar, reiniciar).

Texto:
Atributos: fonte, cor.
Métodos: desenhar_texto(mensagem, posicao).

TelaInicial:
Métodos: desenhar(), aguardar_entrada().'''

#esse é um teste
