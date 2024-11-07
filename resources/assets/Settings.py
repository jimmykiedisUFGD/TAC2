import pygame

# Variáveis e constantes do jogo
LARGURA_TELA = 1920
ALTURA_TELA = 1080
BACKGROUND = (50, 100, 200)

# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CORTEXTO = (255, 255, 255)  # Cor do texto (branca)

class Settings:
    def setup(self, debug:bool):
        self.debug = debug
        pygame.init()

        # Inicialização
        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.toggle_fullscreen()
        self.relogio = pygame.time.Clock()

        # Ocultando o cursor
        pygame.mouse.set_visible(False)

        # Configurando fonte
        self.fonte = pygame.font.Font(None, 40)

        self.load_images()
        self.load_sound()

    def load_images(self):
        # Carregar imagens
        cenarioInterno = pygame.image.load('resources/image/projetoInterior.png').convert_alpha()
        self.cenarioInterno = pygame.transform.scale(cenarioInterno,(LARGURA_TELA, ALTURA_TELA))

        self.box = pygame.image.load('resources/image/box.jpg').convert_alpha()
        self.box_mask = pygame.mask.from_surface(self.box)

        self.estrela = pygame.image.load('resources/image/estrela.png').convert_alpha()
        self.estrela_mask = pygame.mask.from_surface(self.estrela)

        jogador = pygame.image.load('./resources/image/spriteGato1.png').convert_alpha()
        left = [58,73,92,107,128,147,162,180,199,215,230,251]
        top = [1] * len(left)
        w = [14,18,14,20,17,14,17,18,15,14,20,17]
        h = [47] * len(w)
        self.player_walk, self.player_walk_masks = self.cut_sub_surface(jogador, left, top, w, h, 2)
        self.player_walk_flip, self.player_walk_flip_masks = self.get_flipped(self.player_walk)

        #jump animation
        left = [58,83,106]
        top = [98] * len(left)
        w = [22,22,20]
        h = [45] * len(w)
        self.player_jump, self.player_jump_masks = self.cut_sub_surface(jogador, left, top, w, h, 2)
        self.player_jump_flip, self.player_jump_flip_masks = self.get_flipped(self.player_jump)
        
        #stand animation
        left = [19,86,106,124,141,163,181]
        top = [334,154,151,152,152,153,144] 
        w = [15,19,17,16,18,17,25]
        h = [48,44,47,46,46,45,54] 
        self.player_stand, self.player_stand_masks = self.cut_sub_surface(jogador, left, top, w, h, 2)
        self.player_stand_flip, self.player_stand_flip_masks = self.get_flipped(self.player_stand)

    def load_sound(self):
        # Configurando o som
        somEstrela = pygame.mixer.Sound('./resources/sounds/estrela.mp3')
        #somMiado = pygame.mixer.Sound('./resources/sounds/miado.mp3')
        somTrilha = pygame.mixer.Sound('./resources/sounds/trilha.mp3')
        somEstrela.set_volume(0.05)
        somTrilha.set_volume(0.1)
        somTrilha.play(-1)
        self.somAtivado = True

    def get_flipped(self, surfaces:list):
        list = []
        mask_list = []
        for image in surfaces:
            surf = pygame.transform.flip(image, True, False)
            list.append(surf)
            mask = pygame.mask.from_surface(surf)
            mask_list.append(mask)
        return list, mask_list
    
    def cut_sub_surface(self, surface:pygame.Surface, left, top, w, h, scale):
        list = []
        mask_list = []
        if not (len(left) == len(top) == len(w) == len(h)):
            if self.debug: print('Subsurface empty list!!!')
            return list
        for i in range(len(left)):
            surf = surface.subsurface((left[i],top[i]),(w[i],h[i]))
            surf = pygame.transform.rotozoom(surf,0,scale)
            list.append(surf)
            mask = pygame.mask.from_surface(surf)
            mask_list.append(mask)
        return list, mask_list
    
settings = Settings()