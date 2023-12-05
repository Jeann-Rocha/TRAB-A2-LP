"""
Módulo que contém as classes e métodos para a construção dos tipos de interface do jogo.
"""

import pygame as pg
from pygame.locals import *

# import constants as cst
# import sprites as sp

class Interface:
    """
    Classe que controla os atributos e métodos comuns a cada interface do jogo.
    """
    pass


class Title(Interface):
    """
    Classe que controla a interface de Tela de início do jogo.
    """
    pass


class Settings(Interface):
    """
    Classe que controla a interface de Tela de configurações do jogo.
    """
    pass


class Pause(Interface):
    """
    Classe que controla a interface de Tela de pause do jogo.
    """
    pass


class Reset(Interface):
    """
    Classe que controla a interface de Tela de reset do jogo.
    """
    pass
