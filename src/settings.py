# Dimensões da tela do jogo
WIDTH = 768  # Largura da tela em pixels
HEIGTH = 768  # Altura da tela em pixels

# Taxa de quadros por segundo
FPS = 60  # Define a quantidade de quadros por segundo

# Alfa das camadas de humano e fantasma
HUMAN_ALPHA = 255  # Opacidade total do humano
GHOST_ALPHA = 128  # Opacidade para os fantasmas (mais transparente)

# Tamanho das tiles no mapa
TILESIZE = 48  # Tamanho de cada tile no jogo (em pixels)

# Velocidade de movimento do jogador
PLAYER_SPEED = 4  # A quantidade de pixels que o jogador se move a cada atualização de quadro

# Brilho e intensidade do brilho (para o sistema de iluminação)
BRIGHT_DEFAULT = 50  # Valor padrão de brilho

# Velocidade das partículas
PARTICLE_SPEED = 5  # Velocidade de movimento das partículas no jogo

# Fator de escala para objetos ou gráficos
SCALE_FACTOR = 2  # Multiplica o tamanho dos objetos/gráficos

# Configurações dos inimigos no jogo
ENEMY_SETTINGS = {
    "manga": {
        "speed": 3,  # Velocidade de movimento
        "casting_cooldown": 450,  # Tempo de espera para o próximo ataque (em milissegundos)
        "health": 8,  # Saúde do inimigo
        "attack_radius": 7,  # Distância máxima para o inimigo atacar
        "persecute_radius": 10,  # Distância máxima para o inimigo perseguir o jogador
        "evade_radius": 3,  # Distância máxima para o inimigo desviar de ataques
    },
    "rat": {
        "speed": 6,  # Velocidade de movimento
        "casting_cooldown": 500,  # Tempo de espera para o próximo ataque
        "health": 3,  # Saúde do inimigo
        "attack_radius": 4,  # Distância máxima para o inimigo atacar
        "persecute_radius": 10,  # Distância máxima para o inimigo perseguir o jogador
        "evade_radius": 1,  # Distância máxima para o inimigo desviar de ataques
    },
    "bafao_shaman": {
        "speed": 4,  # Velocidade de movimento
        "casting_cooldown": 550,  # Tempo de espera para o próximo ataque
        "health": 6,  # Saúde do inimigo
        "attack_radius": 6,  # Distância máxima para o inimigo atacar
        "persecute_radius": 10,  # Distância máxima para o inimigo perseguir o jogador
        "evade_radius": 2,  # Distância máxima para o inimigo desviar de ataques
    },
    "bafao_chefe": {
        "speed": 4,  # Velocidade de movimento
        "casting_cooldown": 550,  # Tempo de espera para o próximo ataque
        "health": 6,  # Saúde do inimigo
        "attack_radius": 6,  # Distância máxima para o inimigo atacar
        "persecute_radius": 10,  # Distância máxima para o inimigo perseguir o jogador
        "evade_radius": 2,  # Distância máxima para o inimigo desviar de ataques
    },
}