"""
Módulo que contém as classes e métodos para a construção dos sprites do jogo.
"""

import constants as cst

import pygame as pg
from pygame.locals import *
import random

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
    pass


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
        self.timer_shoot_max = 2 

    def increase_speed(self):
        self.speed = 40 


class Obstacle(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para os obstáculos do jogo.
    """
    pass


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