# checando se jogador pegou estrela
for estrela in estrelas[:]:
    coletouEstrela = jogador['objRect'].colliderect(estrela['objRect'])
    if coletouEstrela: 
        estrelas.remove(estrela)
        pontuacao += 50
    if coletouEstrela and somAtivado: somEstrela.play()
# desenhando estrelas
for estrela in estrelas:
    janela.blit(estrela['imagem'], estrela['objRect'])