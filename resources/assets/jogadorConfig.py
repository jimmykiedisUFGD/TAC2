def moverJogador(jogador, teclas, tela_size):
    if teclas['esquerda']:
        jogador['objRect'].x -= jogador['vel']
    if teclas['direita']:
        jogador['objRect'].x += jogador['vel']

    # Verifique se o jogador está fora da tela e ajuste
    if jogador['objRect'].left < 0:
        jogador['objRect'].left = 0
    if jogador['objRect'].right > tela_size[0]:
        jogador['objRect'].right = tela_size[0]
    if jogador['objRect'].top < 0:
        jogador['objRect'].top = 0
    if jogador['objRect'].bottom > tela_size[1]:
        jogador['objRect'].bottom = tela_size[1]

        
def verificar_colisao_chao(jogador, plataformas):
    jogador['noChao'] = False
    for plataforma in plataformas:
        if jogador['objRect'].colliderect(plataforma['objRect']):
            jogador['noChao'] = True
            jogador['objRect'].bottom = plataforma['objRect'].top
            break