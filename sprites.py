"""
Módulo que contém as classes e métodos para a construção dos sprites do jogo.
"""

import constants as cst

import pygame as pg
from pygame.locals import *
import random
import threading

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

    def __init__(self, display, scale, path_images, *groups, group_shoot) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        self.timer_shoot = 0
        self.timer_shoot_max = 10
        self.group_shoot = group_shoot
        self.lifes = 3
        self.speed = 30

        self.shooting_enabled = True
        self.reset_timer = None

        self.increase_speed_enabled = True
        self.reset_speed_timer = None

    def update(self):
        """
        Método que atualiza os movimentos e tiros do player.
        """

        self.display.blit(self.image, (self.rect.x, self.rect.y))
        self.keys = pg.key.get_pressed()

        self.animate()
        self.movements()
        self.shoot_player()

    def movements(self):
        """
        Método que atualiza os movimentos do player e limita os mesmos
        para as bordas da tela.
        """

        # diagonal superior esquerda
        if self.keys[K_UP] and self.keys[K_LEFT]:
            self.rect.x -= self.speed
            self.rect.y -= self.speed
        # diagonal superior direita
        elif self.keys[K_UP] and self.keys[K_RIGHT]:
            self.rect.x += self.speed
            self.rect.y -= self.speed
        # diagonal inferior esquerda
        elif self.keys[K_DOWN] and self.keys[K_LEFT]:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        # diagonal inferior direita
        elif self.keys[K_DOWN] and self.keys[K_RIGHT]:
            self.rect.x += self.speed
            self.rect.y += self.speed
        # cima
        elif self.keys[K_UP]:
            self.rect.y -= self.speed
        # baixo
        elif self.keys[K_DOWN]:
            self.rect.y += self.speed
        # esquerda
        elif self.keys[K_LEFT]:
            self.rect.x -= self.speed
        # direita
        elif self.keys[K_RIGHT]:
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

    def shoot_player(self):
        """
        Método que atualiza os tiros do player.
        """

        self.timer_shoot += 1
        if self.timer_shoot > self.timer_shoot_max:
            if self.keys[K_SPACE]:
                self.timer_shoot = 0
                Shoot(self.display, cst.SCALE_SHOOT, cst.SHOOT_PLAYER, self.rect.topright, False, 0, (self.groups[0], self.group_shoot))
                shoot_sound = pg.mixer.Sound(cst.SHOOT_SOUND)
                shoot_sound.play()


    def increase_fire_rate(self):
        """
        Método para aumentar temporariamente a taxa de tiro.
        """
        self.shooting_enabled = False
        self.timer_shoot_max = 2

        # Inicia um temporizador para voltar ao timer_shoot_max após 10 segundos
        self.reset_timer = threading.Timer(10, self._reset_fire_rate)
        self.reset_timer.start()

    def _reset_fire_rate(self):
        """
        Método chamado pelo temporizador para reverter as alterações após a duração.
        """
        self.timer_shoot_max = 10
        self.shooting_enabled = True

    def increase_speed(self):
        """
        Método para aumentar temporariamente a velocidade do player.
        """
        self.increase_speed_enabled = False
        self.speed = 50

        # Inicia um temporizador para voltar ao speed após 10 segundos
        self.reset_speed_timer = threading.Timer(10, self._reset_speed)
        self.reset_speed_timer.start()

    def _reset_speed(self):
        """
        Método chamado pelo temporizador para reverter as alterações após a duração.
        """
        self.speed = 30
        self.increase_speed_enabled = True


class Obstacle(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para os obstáculos do jogo.
    """
    
    is_boss = False
    timer_shoot = 0

    def __init__(self, display, scale, path_images, speed_increment, *groups, group_shoot) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        self.group_shoot = group_shoot
        self.rect.x = self.display.get_width()
        self.rect.y = random.randint(0, display.get_height() - scale[1])
        self.speed_increment = speed_increment
        self.speed = speed_increment / 5 + random.randint(10, 30)


    def update(self):
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
        else:
            self.display.blit(self.image, (self.rect.x, self.rect.y))
            self.animate_explosion()

        if self.rect.right < 0 or self.exploded:
            self.groups[1].remove(self)



class Shoot(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para os disparos (tiros) do jogo.
    """

    def __init__(self, display, scale, path_image, pos, is_obstacle=False, speed_obstacle=0, *groups) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_image, *groups)

        self.is_obstacle = is_obstacle
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        if self.is_obstacle:
            self.speed = speed_obstacle + 5
        else:
            self.speed = 25
    

    def update(self):
        """
        Método que atualiza os movimentos do tiro, que estão
        pré-definidos pelo jogo.
        """

        self.display.blit(self.image, (self.rect.x, self.rect.y))

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
    pass