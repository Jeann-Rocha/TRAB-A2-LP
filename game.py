"""
Módulo que contém as classe principal do jogo, onde ocorrem os eventos,
criação de sprites e o funcionamento do gameloop.
"""

import constants as cst
import interface as intf
import sprites as sp

import pygame as pg
from pygame.locals import *
import time


class SpacialGame:
    """
    Classe principal do Jogo.
    """

    def __init__(self) -> None:
        # Inicializando o Pygame
        pg.init()
        pg.mixer.init()

        # Criando a Tela de Jogo
        self.display = pg.display.set_mode((cst.WIDTH, cst.HEIGHT), pg.FULLSCREEN)
        pg.display.set_caption(cst.TITLE)

        # Criando o Relógio de FPS
        self.clock = pg.time.Clock()

        self.beginning()

    def beginning(self):
        """
        Método que constrói a tela de início e encaminha para o início do jogo,
        criando os sprites, score e o gameloop.
        """


    def start_sprites(self):
        """
        Método onde se definem os objetos (sprites) do jogo.
        """

        # Criando os Grupos para os sprites
        self.objectGroup = pg.sprite.Group()
        self.playerGroup = pg.sprite.Group()
        self.obstacleGroup = pg.sprite.Group()
        self.shootPlayerGroup = pg.sprite.Group()
        self.shootObstacleGroup = pg.sprite.Group()
        self.bossGroup = pg.sprite.Group()
        self.shootBossGroup = pg.sprite.Group()
        self.itemGroup = pg.sprite.Group()

        # Criando o Background e o Player do Jogo.
        sp.Background(self.display, cst.SCALE_BACKGROUND, cst.BACKGROUND_GAME, self.objectGroup)
        self.player = sp.Player(self.display, cst.SCALE_PLAYER, cst.PLAYER, (self.objectGroup, self.playerGroup), group_shoot=self.shootPlayerGroup)

    def playing(self):
        """
        Método onde se constrói a jogabilidade do jogo.
        """
        pass
    

    def kill_sprites(self, group):
        """
        Método onde se destroem todos os objetos (sprites) de um grupo e da tela.
        """

        for sprite in group.sprites():
            sprite.kill()

    def kill_all_sprites(self):
        """
        Método onde se removem todos os objetos (sprites) do jogo, 
        inclusive os grupos.
        """

        # removendo os Grupos para os sprites
        self.kill_sprites(self.objectGroup)
        self.kill_sprites(self.playerGroup)
        self.kill_sprites(self.obstacleGroup)
        self.kill_sprites(self.shootPlayerGroup)
        self.kill_sprites(self.shootObstacleGroup)
        self.kill_sprites(self.bossGroup)


    def gameover(self) -> None:
        """
        Método que atualiza um texto de gameover na tela e encaminha
        para a interface de reset.
        """
        pass

