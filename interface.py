"""
Módulo que contém as classes e métodos para a construção dos tipos de interface do jogo.
"""

# Importando as bibliotecas
import sys
from abc import ABC, abstractmethod

import pygame as pg
from pygame.locals import *

import constants as cst
import sprites as sp


class UIElement(ABC):
    """
    Classe abstrata que representa a criação de componentes visuais nas diversas
    interfaces da tela.
    """

    def __init__(self, display: pg.Surface, text: str, font: str, color: tuple, size: int, pos: tuple) -> None:
        """
        Método constutor da classe UIElement.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        text : str
            Texto que será exibido na tela.
        font : str
            Fonte do texto.
        color : tuple
            Tupla contendo os valores RGB da cor do texto.
        size : int
            Tamanho do texto
        pos : tuple
            Tupla contendo a posição x e y do texto.
        
        Returns
        -------
        None.
        """

        self._display = display
        self.text = text
        self._font = pg.font.Font(font, size)
        self._color = color
        self._size = size
        self._pos_x = pos[0]
        self._pos_y = pos[1]

    @abstractmethod
    def draw(self):
        """
        Método abstrato que caracteriza o ato de desenhar coisas na tela.
        
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        pass



class Text(UIElement):
    """
    Classe que desenha textos na tela.
    """

    def __init__(self, display: pg.Surface, text: str, font: str, color: tuple, size: int, pos: tuple) -> None:
        """
        Método constutor da classe Text.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        text : str
            Texto que será exibido na tela.
        font : str
            Fonte do texto.
        color : tuple
            Tupla contendo os valores RGB da cor do texto.
        size : int
            Tamanho do texto
        pos : tuple
            Tupla contendo a posição x e y do texto.
        
        Returns
        -------
        None.
        """

        super().__init__(display, text, font, color, size, pos)

    def draw(self) -> None:
        """
        Método que permite o desenho de textos na tela.
        
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        text = self._font.render(self.text, True, self._color)
        text_rect = text.get_rect(center=(self._pos_x, self._pos_y))
        self._display.blit(text, text_rect)


class Button(UIElement):
    """
    Classe que desenha butões (com textos) na tela.
    """

    def __init__(self, display: pg.Surface, text: str, font: str, color: tuple, size: int, pos: tuple, width: int, height: int) -> None:
        """
        Método constutor da classe Button.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        text : str
            Texto que será exibido na tela.
        font : str
            Fonte do texto.
        color : tuple
            Tupla contendo os valores RGB da cor do texto.
        size : int
            Tamanho do texto
        pos : tuple
            Tupla contendo a posição x e y do texto.
        width : int
            Comprimento do botão.
        height : int
            Largura do botão.

        Returns
        -------
        None.
        """

        super().__init__(display, text, font, color, size, pos)

        self._text_font = font
        self._width = width
        self._height = height
        self._color_button = cst.WHITE
        self.is_pressed = False

    def draw(self) -> None:
        """
        Método que permite o desenho de butões na tela
        
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        # Coleta as posições do mouse
        mouse_x, mouse_y = pg.mouse.get_pos()

        # Condição para trocar de cor caso o mouse colida e verificar se houve click
        if (
            self._pos_x - self._width // 2 - 2 <= mouse_x <= self._pos_x - self._width // 2 + self._width + 2
        ) and (
            self._pos_y - self._height // 2 - 4 <= mouse_y <= self._pos_y - self._height // 2 + self._height + 2
        ):
            self._color_button = cst.BLUE
            if pg.mouse.get_pressed()[0]:
                self.is_pressed = True
            else:
                self.is_pressed = False
        else:
            self._color_button = cst.WHITE

        # Desenha a borda do botão
        pg.draw.rect(self._display, cst.BLACK, (self._pos_x - self._width // 2 - 2, self._pos_y - self._height // 2 - 4, self._width + 4, self._height + 6), 0)

        # Desenha o botão
        pg.draw.rect(self._display, self._color_button, (self._pos_x - self._width // 2, self._pos_y - self._height // 2 - 2, self._width, self._height), 0)

        # Desenha o texto do botão
        text = Text(self._display, self.text, self._text_font, self._color, self._size, [self._pos_x, self._pos_y])
        text.draw()


class Interface(ABC):
    """
    Classe abstrata que controla a interface de Tela de início do jogo.
    """

    def __init__(self, display: pg.Surface) -> None:
        self.display = display
        self.width, self.height = display.get_width(), display.get_height() 
        self.waiting_player = True
        self.clock = pg.time.Clock()
        self.active_credit = False
        self.active_reset = False

    @abstractmethod
    def run(self) -> None:
        """
        Método abstrato que atualiza a interface.
        """

        pass

    def load_background(self, background_path: str) -> None:
        """
        Método que renderiza um background para a interface.
        """

        background = sp.Background(self.display, cst.SCALE_BACKGROUND, [background_path])
        self.display.blit(background.image, (0, 0))

    def quit(self) -> None:
        """
        Método que fecha o jogo.
        """

        pg.quit()
        sys.exit()

    def handle_button_press(self, button: Button) -> None:
        """
        Método que verifica o tipo de butão que foi pressionado e
        faz a devida alteração a depender do tipo de butão.
        """

        if button.is_pressed:
            if button.text == "PLAY": # específico da Tela de Início
                pg.mixer.music.stop()
            elif button.text == "RETURN TO MENU": # específico da Tela de Pause e de Reset
                pg.mixer.music.stop()
                self.active_reset = True # ativa a variável que permite o resetamento do jogo
            elif button.text == "CREDITS": # específico da Tela de Início
                self.active_credit = True # ativa a variável que permite a entrada nos créditos
            elif button.text == "RETURN TO GAME": # específico da Tela de Pause
                pass
            elif button.text == "EXIT": # específico da Tela de Início e de Reset
                self.quit()

            self.waiting_player = False # comum a todas as condições acima


class Title(Interface):
    """
    Classe que controla a interface de Tela de Início do jogo.
    """

    def __init__(self, display) -> None:
        super().__init__(display)

    def run(self) -> None:
        """
        Método que atualiza a interface da Tela de Início.
        """

        if not pg.mixer.music.get_busy():
            pg.mixer.music.load(cst.MUSIC_TITLE)
            pg.mixer.music.play(-1)

        text_title = Text(self.display, "SPACIAL GAME", cst.FONT, cst.GREEN, 90, [self.width // 2, 200])
        play_button = Button(self.display, "PLAY", cst.FONT, cst.GREEN, 20, [self.width // 2, self.height - 250], 150, 30)
        credits_button = Button(self.display, "CREDITS", cst.FONT, cst.GREEN, 20, [self.width // 2, self.height - 180], 150, 30)
        exit_button = Button(self.display, "EXIT", cst.FONT, cst.GREEN, 20, [self.width // 2, self.height - 110], 150, 30)

        while self.waiting_player:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

            self.handle_button_press(play_button)
            self.handle_button_press(credits_button)
            self.handle_button_press(exit_button)

            self.load_background(cst.BACKGROUND_TITLE)

            text_title.draw()
            play_button.draw()
            credits_button.draw()
            exit_button.draw()

            self.clock.tick(cst.FPS)
            pg.display.update()


class Credits(Interface):
    """
    Classe que controla a interface de Créditos do jogo.
    """

    def __init__(self, display: pg.Surface) -> None:
        super().__init__(display)

    def run(self) -> None:
        """
        Método que atualiza a interface para a Tela de Créditos.
        """
        text_colaboradores = Text(self.display, "COLABORADORES", cst.FONT, cst.BLACK, 60, [self.width // 2, 100])
        colaborador_1 = Text(self.display, "Alessandra Bello", cst.FONT, cst.WHITE, 30, [self.width // 2, 170])
        colaborador_2 = Text(self.display, "Edgard Junio", cst.FONT, cst.WHITE, 30, [self.width // 2, 240])
        colaborador_3 = Text(self.display, "Gilherme Ferrari", cst.FONT, cst.WHITE, 30, [self.width // 2, 310])
        colaborador_4 = Text(self.display, "Jeann Rocha", cst.FONT, cst.WHITE, 30, [self.width // 2, 380])
        exit_button = Button(self.display, "RETURN TO MENU", cst.FONT, cst.GREEN, 15, [self.width // 2, self.height - 110], 150, 30)

        while self.waiting_player:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()
            self.handle_button_press(exit_button)
            self.load_background(cst.BACKGROUND_PAUSE)

            text_colaboradores.draw()
            colaborador_1.draw()
            colaborador_2.draw()
            colaborador_3.draw()
            colaborador_4.draw()
            exit_button.draw()

            self.clock.tick(cst.FPS)
            pg.display.update()  


class Pause(Interface):
    """
    Classe que controla a interface de Tela de Pause do jogo.
    """

    def __init__(self, display: pg.Surface) -> None:
        super().__init__(display)

    def run(self) -> None:
        """
        Método que atualiza a interface da Tela de Pause.
        """

        text_pause = Text(self.display, "PAUSE", cst.FONT, cst.GREEN, 90, [self.width // 2, 200])
        return_game_button = Button(self.display, "RETURN TO GAME", cst.FONT, cst.GREEN, 20, [self.width // 2, self.height - 250], 220, 30)
        return_menu_button = Button(self.display, "RETURN TO MENU", cst.FONT, cst.GREEN, 20, [self.width // 2, self.height - 180], 220, 30)

        while self.waiting_player:

            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()

            self.handle_button_press(return_game_button)
            self.handle_button_press(return_menu_button)

            self.load_background(cst.BACKGROUND_PAUSE)

            text_pause.draw()
            return_game_button.draw()
            return_menu_button.draw()

            self.clock.tick(cst.FPS)
            pg.display.update()


class Reset(Interface):
    """
    Classe que controla a interface de Tela de Reset do jogo.
    """

    def __init__(self, display: pg.Surface) -> None:
        super().__init__(display)

    def run(self) -> None:
        """
        Método que atualiza a interface da Tela de Reset.
        """

        text_tryagain = Text(self.display, "DESEJA JOGAR DE NOVO?", cst.FONT, cst.GREEN, 70, [self.width // 2, 150])
        return_menu_button = Button(self.display, "RETURN TO MENU", cst.FONT, cst.GREEN, 20, [self.width // 2, self.height - 370], 220, 30)
        exit_button = Button(self.display, "EXIT", cst.FONT, cst.GREEN, 20, [self.width // 2, self.height - 300], 220, 30)

        while self.waiting_player:
            for event in pg.event.get():
                if event.type == QUIT:
                    self.quit()

            self.handle_button_press(return_menu_button)
            self.handle_button_press(exit_button)

            self.load_background(cst.BACKGROUND_GAMEOVER)

            text_tryagain.draw()
            return_menu_button.draw()
            exit_button.draw()

            self.clock.tick(cst.FPS)
            pg.display.update()
