import pygame, random
from pygame.locals import *
from sys import exit

pygame.init()

# Variáveis e constantes do jogo
LARGURA_TELA = 800
ALTURA_TELA = 600
VEL = 5
VEL_FUNDO_EXTERNO = 2.2  # Velocidade menor para o fundo externo
ITERACOES = 30
CORTEXTO = (255, 255, 255)  # Cor do texto (branca)

# Inicialização
janela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption('Naughty Cat')
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont('arial', 40, True, True)

# Carregar imagens
cenarioInterno = pygame.image.load('./resources/image/projetoInterior.png').convert_alpha()
cenarioExterno = pygame.image.load('./resources/image/projetoExterior.png').convert_alpha()
imagemJogador = pygame.image.load('./resources/image/skinPlayer1.png').convert_alpha()
imagemEstrela = pygame.image.load('./resources/image/estrela.png').convert_alpha()

# Configurando imagens
LARGURA_FUNDO_INTERNO = cenarioInterno.get_width()
ALTURA_FUNDO_INTERNO = cenarioInterno.get_height()

# Redimensionar o fundo externo para se ajustar à altura da tela
LARGURA_FUNDO_EXTERNO = cenarioExterno.get_width()
ALTURA_FUNDO_EXTERNO = cenarioExterno.get_height()
escala = ALTURA_TELA / ALTURA_FUNDO_EXTERNO
cenarioExterno = pygame.transform.scale(cenarioExterno, (int(LARGURA_FUNDO_EXTERNO * escala), ALTURA_TELA))
LARGURA_FUNDO_EXTERNO = cenarioExterno.get_width()  # Atualizar após o redimensionamento

LARGURA_JOGADOR = imagemJogador.get_width()
ALTURA_JOGADOR = imagemJogador.get_height()
LARGURAESTRELA = imagemEstrela.get_width()
ALTURAESTRELA = imagemEstrela.get_height()

# Função para mover o jogador e rolar os fundos
def moverJogador(jogador, teclas, x_fundo_interno, x_fundo_externo):
    # Atualiza a posição do jogador
    if teclas['esquerda']:
        jogador['objRect'].x -= jogador['vel']
        x_fundo_interno += jogador['vel']
        x_fundo_externo += jogador['vel'] * VEL_FUNDO_EXTERNO / VEL
    if teclas['direita']:
        jogador['objRect'].x += jogador['vel']
        x_fundo_interno -= jogador['vel']
        x_fundo_externo -= jogador['vel'] * VEL_FUNDO_EXTERNO / VEL
    if teclas['cima']:
        jogador['objRect'].y -= jogador['vel']
    if teclas['baixo']:
        jogador['objRect'].y += jogador['vel']

    # Mantém o jogador dentro da tela
    jogador['objRect'].x = max(0, min(jogador['objRect'].x, LARGURA_TELA - LARGURA_JOGADOR))
    jogador['objRect'].y = max(0, min(jogador['objRect'].y, ALTURA_TELA - ALTURA_JOGADOR))

    # Para o fundo quando o jogador chegar ao fim
    if x_fundo_interno <= -LARGURA_FUNDO_INTERNO + LARGURA_TELA:
        x_fundo_interno = -LARGURA_FUNDO_INTERNO + LARGURA_TELA
    if x_fundo_externo <= -LARGURA_FUNDO_EXTERNO + LARGURA_TELA:
        x_fundo_externo = -LARGURA_FUNDO_EXTERNO + LARGURA_TELA
    if x_fundo_interno >= 0:
        x_fundo_interno = 0
    if x_fundo_externo >= 0:
        x_fundo_externo = 0

    return x_fundo_interno, x_fundo_externo

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

# Configurando o som
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

    pontuacao = 0
    estrelas = []
    teclas = {'esquerda': False, 'direita': False, 'cima': False, 'baixo': False}
    numInteracoes = 0

    # Criando jogador
    jogador = {'objRect': pygame.Rect(300, 100, LARGURA_JOGADOR, ALTURA_JOGADOR), 'imagem': imagemJogador, 'vel': VEL}

    x_fundo_interno = 0  # Posição inicial do fundo interno
    x_fundo_externo = 0  # Posição inicial do fundo externo

    rodando = True

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

        # Movendo o jogador e os fundos
        x_fundo_interno, x_fundo_externo = moverJogador(jogador, teclas, x_fundo_interno, x_fundo_externo)

        # Desenhando os fundos (sem repetição)
        janela.blit(cenarioExterno, (x_fundo_externo, 0))  # Fundo externo
        janela.blit(cenarioInterno, (x_fundo_interno, 0))  # Fundo interno

        # Colocando as pontuações
        colocarTexto('Pontuação: ' + str(pontuacao), fonte, janela, 10, 0)

        # Desenhando jogador
        janela.blit(jogador['imagem'], jogador['objRect'])

        # Checando se jogador pegou estrela
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