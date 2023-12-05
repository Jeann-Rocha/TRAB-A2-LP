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
    pass


class Boss(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para o boss do jogo.
    """
    pass