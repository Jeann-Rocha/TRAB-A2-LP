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
        
    pass


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