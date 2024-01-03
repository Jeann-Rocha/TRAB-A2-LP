from os.path import join
"""
Módulo das constantes que setão utlilizadas no decorrer do código (Variáveis Globais)
"""

# Dimensões
WIDTH, HEIGHT = 1280, 720

# Título
TITLE = "Spacial Game"

# Cores
RED = (255, 0, 0) # red
GREEN = (0, 255, 0) # verde
BLUE = (0, 0, 255) # azul
BLACK = (0, 0, 0) # preto
WHITE = (255, 255, 255) # branco
GRAY = (128, 128, 128) # cinza

# Fontes
FONT = join("src","assets","fonts","space_invaders.ttf")

# Caminhos (Paths): Imagens
# TELA DE FUNDO
BACKGROUND_GAME = [join("src","assets","sprites","background.jpg")]
BACKGROUND_TITLE = join("src","assets","sprites","display_title.jpg")
BACKGROUND_PAUSE = join("src","assets","sprites","display_pause.jpg")
BACKGROUND_GAMEOVER = join("src","assets","sprites","display_gameover.jpg")
# ENTIDADES
PLAYER = [join("src","assets","sprites","player__00.png"), join("src","assets","sprites","player__01.png"), join("src","assets","sprites","player__02.png"),
          join("src","assets","sprites","player__03.png")]
OBSTACLE = [join("src","assets","sprites","obstacle.png")]
BOSS = [join("src","assets","sprites","boss__0.png"), join("src","assets","sprites","boss__1.png"),
        join("src","assets","sprites","boss__2.png"), join("src","assets","sprites","boss__3.png")]
# TIROS
SHOOT_PLAYER = [join("src","assets","sprites","shoot.png")]
SHOOT_OBSTACLE = [join("src","assets","sprites","shoot_obstacle.png")]
SHOOT_BOSS = [join("src","assets","sprites","shoot_boss.png")]
# OUTROS (ITENS, VIDA E EXPLOSÃO)
ITEM_LIFE = [join("src","assets","sprites","life.png")]
ITEM_FIRE = [join("src","assets","sprites","fire__00.png"), join("src","assets","sprites","fire__01.png"), join("src","assets","sprites","fire__02.png"),
             join("src","assets","sprites","fire__03.png")]
ITEM_SPEED = [join("src","assets","sprites","speed__00.png"), join("src","assets","sprites","speed__01.png"), join("src","assets","sprites","speed__02.png"),
              join("src","assets","sprites","speed__03.png"), join("src","assets","sprites","speed__04.png")]
EXPLOSION = [join("src","assets","sprites","explosion__00.png"), join("src","assets","sprites","explosion__01.png"), join("src","assets","sprites","explosion__02.png"),
             join("src","assets","sprites","explosion__03.png"), join("src","assets","sprites","explosion__04.png"), join("src","assets","sprites","explosion__05.png"),
             join("src","assets","sprites","explosion__07.png"), join("src","assets","sprites","explosion__08.png"), join("src","assets","sprites","explosion__09.png"),
             join("src","assets","sprites","explosion__10.png")]

# Caminhos (Paths): Músicas
MUSIC_TITLE = join("src","assets","music","music_title.mp3")
MUSIC_GAME = join("src","assets","music","music_game.mp3")

# Caminhos (Paths): Sons de Efeito
SHOOT_SOUND = join("src","assets","sound_effect","shoot_sound.wav")
GAMEOVER_SOUND = join("src","assets","sound_effect","game_over.wav")
EXPLOSION_SOUND = join("src","assets","sound_effect","explosion_sound.wav")
EXTERMINATE_SOUND = join("src","assets","sound_effect","exterminate_sound.mp3")
ITEM_SOUND = join("src","assets","sound_effect","take_item_sound.mp3")
BOSS_SOUND = join("src","assets","sound_effect","sound_boss_appear.mp3")

# Frames por Segundo
FPS = 20

# Escalas de tamanho para os Sprites
SCALE_BACKGROUND = [WIDTH, HEIGHT]
SCALE_PLAYER = [74, 125]
SCALE_OBSTACLE = [175, 175]
SCALE_SHOOT = [24, 12]
SCALE_BOSS = [500, 500]
SCALE_ITEM = [75, 75]
SCALE_SHOOT_BOSS = [144, 72]
SCALE_LIFE = [50, 50]

# Tipos de Itens
ITEMS =  [(SCALE_ITEM, ITEM_LIFE, "hearth"), (SCALE_ITEM, ITEM_FIRE, "fire_rate"), (SCALE_ITEM, ITEM_SPEED, "speed")]
