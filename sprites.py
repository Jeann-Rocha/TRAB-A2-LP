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

    def __init__(self, display, scale, path_image, *groups) -> None:
        self.display = display
        if groups:
           self.groups = groups[0]
        self.image = pg.image.load(path_image)
        self.image = pg.transform.scale(self.image, scale)
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)


class Background(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para o cenário do jogo.
    """
    def __init__(self, display, scale, path_images, *groups) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)
        
        self.pos_width = self.display.get_width()
        self.speed = 1


    def update(self):
        """
        Método que atualiza o background para movimentar-se enquanto o jogador
        estiver jogando para dar um efeito de dinamicidade ao jogo.
        """

        self.display.blit(self.image, (0, 0))

        rel_x = self.pos_width % self.image.get_rect().width
        self.display.blit(self.image, (rel_x - self.image.get_rect().width, 0))
        if rel_x < 1200:
            self.display.blit(self.image, (rel_x, 0))
        self.pos_width -= self.speed


class Player(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para o player (jogador) do jogo.
    """

    def __init__(self, display: pg.Surface, scale: list, path_images: list, *groups, group_shoot: pg.sprite.Group) -> None:
        """
        Método constutor da classe Player.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        scale : list
            Lista contendo os valores x e y da escala do sprite.
        path_images : list
            Lista contendo o conjunto de imagens do sprite.
        groups : pg.sprite.Group
            Conjunto de grupos que o sprite pertence.
        group_shoot: pg.sprite.Group
            Sprite do tiro que será utilizado pelo player.
        
        Returns
        -------
        None.
        """
        
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        # posição inicial do player
        self.rect.x = 0
        self.rect.y = self._display.get_height() // 2

        self.__timer_shoot = 0
        self.__timer_shoot_max = 8
        self.__group_shoot = group_shoot

        self.shooting_enabled = True
        self.increase_speed_enabled = True

        self.damaged = False # indicador de que o player levou dano
        self.lifes = 3
        self.__speed = 30
        self._animation_speed = 10

    def update(self) -> None:
        """
        Método que atualiza os movimentos e tiros do player.
                
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

        self.__keys = pg.key.get_pressed()

        self._animate()
        if self._animation_speed >= 2:
            self._animation_speed -= 0.05 # efetio contínuo de aumento da velocidade
        self.__movements()
        self.__shoot_player()
        self.__draw_lifes()

    def __movements(self) -> None:
        """
        Método que atualiza os movimentos do player e limita os mesmos
        para as bordas da tela.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        # Diagonal superior esquerda
        if self.__keys[K_w] and self.__keys[K_a]:
            self.rect.x -= self.__speed
            self.rect.y -= self.__speed
        # Diagonal superior direita
        elif self.__keys[K_w] and self.__keys[K_d]:
            self.rect.x += self.__speed
            self.rect.y -= self.__speed
        # Diagonal inferior esquerda
        elif self.__keys[K_s] and self.__keys[K_a]:
            self.rect.x -= self.__speed
            self.rect.y += self.__speed
        # Diagonal inferior direita
        elif self.__keys[K_s] and self.__keys[K_d]:
            self.rect.x += self.__speed
            self.rect.y += self.__speed
        # Cima
        elif self.__keys[K_w]:
            self.rect.y -= self.__speed
        # Baixo
        elif self.__keys[K_s]:
            self.rect.y += self.__speed
        # Esquerda
        elif self.__keys[K_a]:
            self.rect.x -= self.__speed
        # Direita
        elif self.__keys[K_d]:
            self.rect.x += self.__speed
        # Borda superior
        if self.rect.top < 0:
            self.rect.top = 0
        # Borda inferior
        if self.rect.bottom > self._display.get_height():
            self.rect.bottom = self._display.get_height()
        # Borda lateral esquerda
        if self.rect.left < 0:
            self.rect.left = 0
        # Borda lateral direita
        if self.rect.right > self._display.get_width():
            self.rect.right = self._display.get_width()

    def __draw_lifes(self) -> None:
        """
        Método que desenha no canto superior esquerdo da tela as vidas que o player tem.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        life = Render(self._display, cst.SCALE_LIFE, cst.ITEM_LIFE, self._groups[0])

        for n in range(self.lifes):
            life._display.blit(life.image, (20 + 50 * n, 20))

    def __shoot_player(self) -> None:
        """
        Método que atualiza os tiros do player.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        self.__timer_shoot += 1
        if self.__timer_shoot > self.__timer_shoot_max:
            if self.__keys[K_j]:
                self.__timer_shoot = 0
                Shoot(self._display, cst.SCALE_SHOOT, cst.SHOOT_PLAYER, self.rect.topright, self.__speed, False, (self._groups[0], self.__group_shoot))

    def increase_fire_rate(self) -> None:
        """
        Método para aumentar temporariamente a taxa de tiro.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        self.shooting_enabled = False
        self.__timer_shoot_max = 1

        # Inicia um temporizador para voltar ao tempo de tiro original após 15 segundos
        self.reset_timer = threading.Timer(15, self.__reset_fire_rate)
        self.reset_timer.start()

    def __reset_fire_rate(self) -> None:
        """
        Método chamado pelo temporizador para reverter as alterações após a duração.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        self.__timer_shoot_max = 8
        self.shooting_enabled = True

    def increase_speed(self) -> None:
        """
        Método para aumentar temporariamente a velocidade do player.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        self.increase_speed_enabled = False
        self.__speed = 60
        self._animation_speed = 1

        # Inicia um temporizador para voltar a velocidade original após 15 segundos
        self.reset_speed_timer = threading.Timer(15, self.__reset_speed)
        self.reset_speed_timer.start()

    def __reset_speed(self) -> None:
        """
        Método chamado pelo temporizador para reverter as alterações após a duração.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        self.__speed = 30
        self.increase_speed_enabled = True
        self._animation_speed = 2

    def increase_hearth(self) -> None:
        """
        Método para aumentar a vida do player.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        self.lifes += 1


class Obstacle(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para os obstáculos do jogo.
    """

    is_boss = False # atríbuto global para indicar se há um boss (obstáculos e boss não atuam simultaneamente)

    def __init__(self, display: pg.Surface, scale: list, path_images: list, speed_increment: float, *groups, group_shoot: pg.sprite.Group) -> None:
        """
        Método constutor da classe Obstacle.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        scale : list
            Lista contendo os valores x e y da escala do sprite.
        path_images : list
            Lista contendo o conjunto de imagens do sprite.
        speed_increment : float
            Incremento na velocidade do obstáculo.
        groups : pg.sprite.Group
            Conjunto de grupos que o sprite pertence.
        group_shoot: pg.sprite.Group
            Sprite do tiro que será utilizado pelo obstáculo.
        
        Returns
        -------
        None.
        """
        
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        self.__group_shoot = group_shoot
        self.rect.x = self._display.get_width()
        self.rect.y = random.randint(0, display.get_height() - scale[1]) # posição aleatória em relação a altura da tela

        self.timer_shoot = 0
        self.__timer_shoot_max = 50
        self.__min_speed, self.__max_speed = 20, 30 # constantes que randomizam a velocidade dos obstáculos
        self.__speed_increment = speed_increment
        self.speed = self.__speed_increment / 5 + random.randint(self.__min_speed, self.__max_speed)

    def update(self) -> None:
        """
        Método que atualiza os movimentos dos obstáculos, que estão
        pré-definidos pelo jogo.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        if not self.rect.right < 0 and not self.exploded:
            self._display.blit(self.image, (self.rect.x, self.rect.y))

            self.rect.x -= self.speed

            if not self.is_boss:
                self.__new_obstacles()
            self.__shoot_obstacles()
            self._animate()
        elif self.exploded: # o surgimento do boss explode os obstáculos existentes na tela
            self._display.blit(self.image, (self.rect.x, self.rect.y))
            self._animate_explosion()

        if self.rect.right < 0 or self.exploded:
            self._groups[1].remove(self)

    def __new_obstacles(self) -> None:
        """
        Método que gera (aleatoriamente) novos obstáculos.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        new_obstacles = random.randint(1, 4) # quantidade aleatória entre 1 e 4 obstáculos a ser gerada
        if len(self._groups[1].sprites()) <= 2: # condição para ter mais obstáculos (veja que o máximo tem que ser 2 + 4 = 6)
            if random.random() < 0.03: # probabilidade de 3% de gerar mais obstáculos
                for _ in range(new_obstacles):
                    Obstacle(self._display, cst.SCALE_OBSTACLE, cst.OBSTACLE, self.__speed_increment, (self._groups[0], self._groups[1]), group_shoot=self.__group_shoot)

    def __shoot_obstacles(self) -> None:
        """
        Método que atualiza os tiros do obstáculo.
                
        Parameters
        ----------

        Returns
        -------
        None.
        """

        self.timer_shoot += 1
        if self.timer_shoot > self.__timer_shoot_max:
            self.timer_shoot = 0
            obstacles_choice = random.sample(self._groups[1].sprites(), random.randint(0, len(self._groups[1].sprites()))) # escolhe uma amostra da quantidade de obstáculos na tela para atirar
            for oc in obstacles_choice:
                Shoot(self._display, cst.SCALE_SHOOT, cst.SHOOT_OBSTACLE, (oc.rect.left, oc.rect.centery), oc.speed, True, (self._groups[0], self.__group_shoot))
            for ob in self._groups[1].sprites():
                ob.timer_shoot = 0


class Shoot(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para os disparos (tiros) do jogo.
    """

    def __init__(self, display, scale, path_images, pos, speed_sprite, is_obstacle=False, *groups) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        self.is_obstacle = is_obstacle
        self.obstacle = None
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        shoot_sound = pg.mixer.Sound(cst.SHOOT_SOUND)
        shoot_sound.play()

        self.speed = speed_sprite + 5
    

    def update(self):
        """
        Método que atualiza os movimentos do tiro, que estão
        pré-definidos pelo jogo.
        """

        self.display.blit(self.image, (self.rect.x, self.rect.y))

        self.animate()

        if self.is_obstacle:
            self.rect.x -= self.speed

            if self.rect.right < 0:
                self.kill()
        else:
            self.rect.x += self.speed

            if self.rect.left > self.display.get_width():
                self.kill()


class Boss(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para o boss do jogo.
    """

    speedx = 5

    def __init__(self, display, scale, path_images, speed_increment, *groups, group_shoot) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        self.animation_speed = 10
        self.lifes = 10
        self.rect.x = self.display.get_width()
        self.rect.y = 0
        self.speedy = speed_increment / 5 + 20
        self.verificate_speedy = "DOWN"
        self.speed = speed_increment / 5

        self.group_shoot = group_shoot
        self.last_shoot_time = 0
        self.start_time = time.time()
        boss_sound = pg.mixer.Sound(cst.BOSS_SOUND_1)
        boss_sound.play()


    def shoot_boss(self):
        current_time = time.time() + 2
        time_on_screen = current_time - self.start_time

        if time_on_screen >= 5 and current_time - self.last_shoot_time >= 2:
                self.last_shoot_time = current_time
                Shoot(self.display, cst.SCALE_SHOOT_BOSS, cst.SHOOT_BOSS, (self.rect.left, random.uniform(self.rect.top, self.rect.bottom)), self.speed, True, (self.groups[0], self.group_shoot))


    def update(self):
        """
        Método que atualiza os movimentos do boss, que estão
        pré-definidos pelo jogo.
        """

        if self.rect.right < 0 or self.exploded:
            self.groups[1].remove(self)

        self.display.blit(self.image, (self.rect.x, self.rect.y))

        self.rect.x -= self.speedx

        if self.rect.right <= self.display.get_width():
            self.speedx = 0

        if self.speedx == 0:
            if not self.exploded:
                if self.rect.top < 0:
                    self.verificate_speedy = "DOWN"
                if self.rect.bottom > self.display.get_height():
                    self.verificate_speedy = "UP"
                if self.verificate_speedy == "DOWN":
                    self.rect.y += self.speedy
                elif self.verificate_speedy == "UP":
                    self.rect.y -= self.speedy
                self.animate()
            else:
                self.display.blit(self.image, (self.rect.x, self.rect.y))
                self.animate_explosion()

        if self.lifes <= 0:
            self.exploded = True
            self.groups[1].empty()
        self.shoot_boss()

