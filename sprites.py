"""
Módulo que contém as classes e métodos para a construção dos sprites do jogo.
"""

import constants as cst

import pygame as pg
from pygame.locals import *
import random
import threading
import time

class Render:
    """
    Classe que renderiza imagens na tela.
    """

    def __init__(self, display: pg.Surface, scale: list, path_images: list, *groups) -> None:
        """
        Método constutor da classe Render.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        scale : list
            Lista contendo os valores x e y da escala do sprite.
        path_images : list
            Lista contendo o conjunto de imagens do sprite.
        groups : 
            Conjunto de grupos que o sprite pertence.
        
        Returns
        -------
        None.
        """

        self._display = display
        if groups:
            self._groups = groups[0]
        self.__images = [pg.image.load(image) for image in path_images] # conjunto de imagens
        self.__images = [pg.transform.scale(image, scale) for image in self.__images] # conjunto de imagens escalonadas na tela
        
        self.image = self.__images[0] # imagem inicial
        self.rect = self.image.get_rect() # definindo o retângulo da imagem
        self._mask = pg.mask.from_surface(self.image) # definindo a mascara de colisão da imagem

        self.__current_frame = 0 # indíce inicial do conjunto de imagens
        self._animation_speed = 5 # velocidade (quantidade de frames por atualização)
        self._animation_timer = 0 # temporizador

        # repetindo algo semelhante ao que está acima, mas para um conjunto de imagens específicas (explosão de sprites)
        self.__explosion_frames = [pg.image.load(image) for image in cst.EXPLOSION]
        self.__explosion_frames = [pg.transform.scale(image, scale) for image in self.__explosion_frames]

        self.__current_explosion_frame = 0
        self.__explosion_speed = 1
        self.__explosion_timer = 0
        self.exploded = False

    def _animate(self) -> None:
        """
        Método que anima os sprites segundo o conjunto de imagens fornecido.
        
        Parameters
        ----------

        Returns
        -------
        None.

        """

        self._animation_timer += 1
        if self._animation_timer >= self._animation_speed:
            self._animation_timer = 0
            self.__current_frame = (self.__current_frame + 1) % len(self.__images) # novo indíce do conjunto de imagens
            self.image = self.__images[self.__current_frame] # nova imagem

    def _animate_explosion(self) -> None:
        """
        Método que anima a explosão que ocorre após a morte dos sprites no jogo.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        # som de explosão
        if self.__current_explosion_frame == 0:
            try:
                explosion_sound = pg.mixer.Sound(cst.EXPLOSION_SOUND)
                explosion_sound.play()
            except pg.error as e:
                raise eg.SoundLoadError(f"Detalhes do erro: {e}")

        if self.__current_explosion_frame < len(self.__explosion_frames):
            self.__explosion_timer += 1
            if self.__explosion_timer >= self.__explosion_speed:
                self.__explosion_timer = 0
                self.image = self.__explosion_frames[self.__current_explosion_frame]
                self.__current_explosion_frame += 1

        # morte do sprite
        if self.__current_explosion_frame == len(self.__explosion_frames):
            self.kill()


class Background(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para o cenário do jogo.
    """

    def __init__(self, display: pg.Surface, scale: list, path_images: list, *groups) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)
        
        self.pos_width = self.display.get_width()
        self.speed = 1 # velocidade de movimento do background

    def update(self) -> None:
        """
        Método que atualiza o background para movimentar-se enquanto o jogador
        estiver jogando para dar um efeito de dinamicidade ao jogo.
        """

        self.display.blit(self.image, (0, 0))

        rel_x = self.pos_width % self.image.get_rect().width # efeito contínuo de deslocamento horizontal
        self.display.blit(self.image, (rel_x - self.image.get_rect().width, 0)) # redesenha a imagem na tela
        if rel_x < cst.WIDTH:
            self.display.blit(self.image, (rel_x, 0))
        self.pos_width -= self.speed


class Player(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para o player (jogador) do jogo.
    """

    def __init__(self, display: pg.Surface , scale: list, path_images: list, *groups, group_shoot: pg.sprite.Group) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        # posição inicial do player
        self.rect.x = 0
        self.rect.y = self.display.get_height() // 2

        self.timer_shoot = 0
        self.timer_shoot_max = 10
        self.group_shoot = group_shoot

        self.damaged = False # indicador de que o player levou dano
        self.lifes = 3
        self.speed = 30
        self.animation_speed = 10

        self.shooting_enabled = True
        self.reset_timer = None

        self.increase_speed_enabled = True
        self.reset_speed_timer = None

    def update(self) -> None:
        """
        Método que atualiza os movimentos e tiros do player.
        """

        if self.damaged:
            self.damaged = False
            # colocar som de dano no player...
        else:
            self.display.blit(self.image, (self.rect.x, self.rect.y))

        self.keys = pg.key.get_pressed()

        self.animate()
        if self.animation_speed >= 2:
            self.animation_speed -= 0.05 # efetio contínuo de aumento da velocidade
        self.movements()
        self.shoot_player()
        self.draw_lifes()

    def movements(self) -> None:
        """
        Método que atualiza os movimentos do player e limita os mesmos
        para as bordas da tela.
        """

        # diagonal superior esquerda
        if self.keys[K_w] and self.keys[K_a]:
            self.rect.x -= self.speed
            self.rect.y -= self.speed
        # diagonal superior direita
        elif self.keys[K_w] and self.keys[K_d]:
            self.rect.x += self.speed
            self.rect.y -= self.speed
        # diagonal inferior esquerda
        elif self.keys[K_s] and self.keys[K_a]:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        # diagonal inferior direita
        elif self.keys[K_s] and self.keys[K_d]:
            self.rect.x += self.speed
            self.rect.y += self.speed
        # cima
        elif self.keys[K_w]:
            self.rect.y -= self.speed
        # baixo
        elif self.keys[K_s]:
            self.rect.y += self.speed
        # esquerda
        elif self.keys[K_a]:
            self.rect.x -= self.speed
        # direita
        elif self.keys[K_d]:
            self.rect.x += self.speed

        # borda superior
        if self.rect.top < 0:
            self.rect.top = 0
        # borda inferior
        if self.rect.bottom > self.display.get_height():
            self.rect.bottom = self.display.get_height()
        # borda lateral esquerda
        if self.rect.left < 0:
            self.rect.left = 0
        # borda lateral direita
        if self.rect.right > self.display.get_width():
            self.rect.right = self.display.get_width()

    def draw_lifes(self) -> None:
        """
        Método que desenha no canto superior esquerdo da tela as vidas que o player tem.
        """

        life = Render(self.display, cst.SCALE_LIFE, cst.LIFE, self.groups[0])

        for n in range(self.lifes):
            life.display.blit(life.image, (20 + 50 * n, 20))

    def shoot_player(self) -> None:
        """
        Método que atualiza os tiros do player.
        """

        self.timer_shoot += 1
        if self.timer_shoot > self.timer_shoot_max:
            if self.keys[K_j]:
                self.timer_shoot = 0
                Shoot(self.display, cst.SCALE_SHOOT, cst.SHOOT_PLAYER, self.rect.topright, self.speed, False, (self.groups[0], self.group_shoot))


    def increase_fire_rate(self) -> None:
        """
        Método para aumentar temporariamente a taxa de tiro.
        """
        self.shooting_enabled = False
        self.timer_shoot_max = 2

        # Inicia um temporizador para voltar ao timer_shoot_max após 10 segundos
        self.reset_timer = threading.Timer(10, self._reset_fire_rate)
        self.reset_timer.start()

    def _reset_fire_rate(self) -> None:
        """
        Método chamado pelo temporizador para reverter as alterações após a duração.
        """
        self.timer_shoot_max = 10
        self.shooting_enabled = True

    def increase_speed(self) -> None:
        """
        Método para aumentar temporariamente a velocidade do player.
        """
        self.increase_speed_enabled = False
        self.speed = 50
        self.animation_speed = 1

        # Inicia um temporizador para voltar ao speed após 10 segundos
        self.reset_speed_timer = threading.Timer(10, self._reset_speed)
        self.reset_speed_timer.start()

    def _reset_speed(self) -> None:
        """
        Método chamado pelo temporizador para reverter as alterações após a duração.
        """
        self.speed = 30
        self.increase_speed_enabled = True

    def increase_hearth(self) -> None:
        """
        Método para aumentar a vida do player.
        """
        self.lifes += 1


class Obstacle(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para os obstáculos do jogo.
    """
    
    is_boss = False # atríbuto global para indicar se há um boss (obstáculos e boss não atuam simultaneamente)

    def __init__(self, display: pg.Surface, scale: list, path_images: list, speed_increment: float, *groups, group_shoot: pg.sprite.Group) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        self.group_shoot = group_shoot
        self.rect.x = self.display.get_width()
        self.rect.y = random.randint(0, display.get_height() - scale[1]) # posição aleatória em relação a altura da tela
        self.timer_shoot = 0
        self.timer_shoot_max = 50
        self.min_speed, self.max_speed = 20, 30 # constantes que randomizam a velocidade dos obstáculos
        self.speed_increment = speed_increment
        self.speed = speed_increment / 5 + random.randint(self.min_speed, self.max_speed)


    def update(self) -> None:
        """
        Método que atualiza os movimentos dos obstáculos, que estão
        pré-definidos pelo jogo.
        """

        if not self.rect.right < 0 and not self.exploded:
            self.display.blit(self.image, (self.rect.x, self.rect.y))

            self.rect.x -= self.speed

            if not self.is_boss:
                self.new_obstacles()
            self.shoot_obstacles()
            self.animate()
        elif self.exploded: # o surgimento do boss explode os obstáculos existentes na tela
            self.display.blit(self.image, (self.rect.x, self.rect.y))
            self.animate_explosion()

        if self.rect.right < 0 or self.exploded:
            self.groups[1].remove(self)

    def new_obstacles(self) -> None:
        """
        Método que gera (aleatoriamente) novos obstáculos.
        """

        new_obstacles = random.randint(1, 4) # quantidade aleatória entre 1 e 4 obstáculos a ser gerada
        if len(self.groups[1].sprites()) <= 2: # condição para ter mais obstáculos (veja que o máximo tem que ser 2 + 4 = 6)
            if random.random() < 0.03: # probabilidade de 3% de gerar mais obstáculos
                for _ in range(new_obstacles):
                    Obstacle(self.display, cst.SCALE_OBSTACLE, cst.OBSTACLE, self.speed_increment, (self.groups[0], self.groups[1]), group_shoot=self.group_shoot)


    def shoot_obstacles(self) -> None:
        """
        Método que atualiza os tiros do obstáculo.
        """

        self.timer_shoot += 1
        if self.timer_shoot > self.timer_shoot_max:
            self.timer_shoot = 0
            obstacles_choice = random.sample(self.groups[1].sprites(), random.randint(0, len(self.groups[1].sprites()))) # escolhe uma amostra da quantidade de obstáculos na tela para atirar
            for oc in obstacles_choice:
                Shoot(self.display, cst.SCALE_SHOOT, cst.SHOOT_OBSTACLE, (oc.rect.left, oc.rect.centery), oc.speed, True, (self.groups[0], self.group_shoot))
            for ob in self.groups[1].sprites():
                ob.timer_shoot = 0


class Shoot(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para os disparos (tiros) do jogo.
    """

    def __init__(self, display: pg.Surface, scale: int, path_images: list, pos: tuple, speed_sprite: float, is_obstacle=False, *groups) -> None:
        """
        Método constutor da classe Shoot.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        scale : list
            Lista contendo os valores x e y da escala do sprite.
        path_images : list
            Lista contendo o conjunto de imagens do sprite.
        pos : tuple
            Tupla contendo as posições x e y do sprite.
        speed_sprite: float
            Velocidade do sprite que terá o tiro.
        is_obstacle: bool (Opcional)
            Instância que verifica que se o sprite não é o player.
        groups : pg.sprite.Group
            Conjunto de grupos que o sprite pertence.
        
        Returns
        -------
        None.
        """

        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        self.__is_obstacle = is_obstacle # deve ser verdadeiro para obstáculos ou boss
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        # som do tiro
        try:
            shoot_sound = pg.mixer.Sound(cst.SHOOT_SOUND)
            shoot_sound.play()
        except pg.error as e:
            raise eg.SoundLoadError(f"Detalhes do erro: {e}")

        self.__speed = speed_sprite + 5

    def update(self) -> None:
        """
        Método que atualiza os movimentos do tiro, que estão
        pré-definidos pelo jogo.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        self._display.blit(self.image, (self.rect.x, self.rect.y))

        self._animate()

        if self.__is_obstacle: # tiro do obstáculo ou do boss
            self.rect.x -= self.__speed

            if self.rect.right < 0:
                self.kill()
        else: # tiro do player
            self.rect.x += self.__speed

            if self.rect.left > self._display.get_width():
                self.kill()


class Boss(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para o boss do jogo.
    """

    def __init__(self, display: pg.Surface, scale: list, path_images: list, speed_increment: float, lifes: int, *groups, group_shoot: pg.sprite.Group) -> None:
        """
        Método constutor da classe Boss.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        scale : list
            Lista contendo os valores x e y da escala do sprite.
        path_images : list
            Lista contendo o conjunto de imagens do sprite.
        speed_increment : float
            Incremento na velocidade do boss.
        lifes: int
            Vidas do boss.
        groups : pg.sprite.Group
            Conjunto de grupos que o sprite pertence.
        group_shoot: pg.sprite.Group
            Sprite do tiro que será utilizado pelo boss.
        
        Returns
        -------
        None.
        """

        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        self.rect.x = self._display.get_width()
        self.rect.y = 0

        self.speedx = 5 # velocidade de entrada
        self.__speedy = speed_increment / 5 + 20 # velocidade de continuação
        self.__verificate_speedy = "DOWN" # verifica se o boss já apareceu completamente na tela
        self.__speed = speed_increment / 5
        self._animation_speed = 8

        self.__group_shoot = group_shoot
        self.__last_shoot_time = 0
        self.__start_time = time.time()

        self.lifes = lifes
        self.damaged = False # indicador de que o boss levou dano

        # som de entrada do boss
        try:
            boss_sound = pg.mixer.Sound(cst.BOSS_SOUND)
            boss_sound.play()
        except pg.error as e:
            raise eg.SoundLoadError(f"Detalhes do erro: {e}")

    def __draw_life(self) -> None:
        """
        Método que desenha no canto inferior direito da tela uma barra vermelha com a vida do boss.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        bar_life_width = int((self.lifes / 10) * 200)
        pg.draw.rect(self._display, cst.RED, (self._display.get_width() - bar_life_width - 10, self._display.get_height() - 50, bar_life_width, 10))

    def __shoot_boss(self) -> None:
        """
        Método que atualiza os tiros do boss.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """
        
        current_time = time.time() + 2
        time_on_screen = current_time - self.__start_time

        if time_on_screen >= 5 and current_time - self.__last_shoot_time >= 2:
                self.__last_shoot_time = current_time
                Shoot(self._display, cst.SCALE_SHOOT_BOSS, cst.SHOOT_BOSS, (self.rect.left, random.uniform(self.rect.top, self.rect.bottom)), self.__speed, True, (self._groups[0], self.__group_shoot))

    def update(self) -> None:
        """
        Método que atualiza os movimentos do boss, que estão
        pré-definidos pelo jogo.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        if self.damaged:
            self.damaged = False
        else:
            self._display.blit(self.image, (self.rect.x, self.rect.y))

        self.rect.x -= self.speedx

        if self.rect.right <= self._display.get_width(): # enquanto ocorre a entrada do boss
            self.speedx = 0

        if self.speedx == 0: # após a entrada do boss (movimento de vai-e-vem para cima e para baixo)
            if not self.exploded:
                if self.rect.top < 0:
                    self.__verificate_speedy = "DOWN"
                if self.rect.bottom > self._display.get_height():
                    self.__verificate_speedy = "UP"
                if self.__verificate_speedy == "DOWN":
                    self.rect.y += self.__speedy
                elif self.__verificate_speedy == "UP":
                    self.rect.y -= self.__speedy
                self._animate()
                self.__draw_life()
                self.__shoot_boss()
            else:
                self._display.blit(self.image, (self.rect.x, self.rect.y))
                self._animate_explosion()

        if self.lifes <= 0:
            self.exploded = True
            self._groups[1].empty()

        if self.exploded:
            self._groups[1].remove(self)
            

class Items(pg.sprite.Sprite, Render):
    """
    Classe de sprite(s) para os itens do jogo.
    """

    def __init__(self, display: pg.Surface, scale: list, path_images: list, item_type: str, *groups, player: pg.sprite.Group) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)
        
        self.rect.x = self.display.get_width()
        self.rect.y = random.randint(0, display.get_height() - scale[1])

        self.speed = 5
        self.animation_speed = 1

        self.player = player
        self.item_type = item_type # pode ser "fire_rate", "speed" ou "hearth"

    def apply_effect(self) -> None:
        """
        Método que aplica o efeito do item (que pode ser temporário) ao jogador
        """

        if self.item_type == "fire_rate": # efeito de cadência no tiro (efeito temporário)
            self.player.increase_fire_rate()
        elif self.item_type == "speed": # efeito de velocidade no player (efeito temporário)
            self.player.increase_speed()
        elif self.item_type == "hearth": # efeito de escudo no player (efeito permanente)
            self.player.increase_hearth()

    def update(self) -> None:
        """
        Método que atualiza a geração de um item no decorrer do jogo.
        """

        self.display.blit(self.image, (self.rect.x, self.rect.y))

        self.rect.x -= self.speed

        self.animate()

        if self.rect.right < 0:
            self.kill()
