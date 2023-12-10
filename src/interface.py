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
import exception_game as eg


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

    def __init__(self, display: pg.Surface, text: str, font: str, color: tuple, size: int, pos: tuple, width: int, height: int, is_selected=True) -> None:
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
        not_click : bool
            Instância que informa se o botão é ou não selecionável.

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
        self._is_selected = is_selected

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
        """
        Método constutor da classe Interface.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        
        Returns
        -------
        None.
        """

        self._display = display
        self._width, self._height = display.get_width(), display.get_height() 
        self.waiting_player = True
        self._clock = pg.time.Clock()
        self.active_credit = False
        self.active_reset = False

    @abstractmethod
    def run(self) -> None:
        """
        Método abstrato que atualiza a interface.
        
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        pass

    def _load_background(self, background_path: str) -> None:
        """
        Método que renderiza um background para a interface.
        
        Parameters
        ----------
        background_path : str
            Caminho do background que será carregado.

        Returns
        -------
        None.
        """

        try:
            background = sp.Background(self._display, cst.SCALE_BACKGROUND, [background_path])
        except ValueError as ve:
            raise eg.SpriteInstanceError(f"Detalhes do erro: {ve}")
        self._display.blit(background.image, (0, 0))

    def _quit(self) -> None:
        """
        Método que fecha o jogo.
        
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        pg.quit()
        sys.exit()

    def handle_button_press(self, button: Button) -> None:
        """
        Método que verifica o tipo de butão que foi pressionado e
        faz a devida alteração a depender do tipo de butão.
        
        Parameters
        ----------
        button : Button
            Butão que será pressionado.
        
        Returns
        -------
        None.
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
        """
        Método constutor da classe Text.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        
        Returns
        -------
        None.
        """

        super().__init__(display)

    def run(self) -> None:
        """
        Método que atualiza a interface da Tela de Início.
        Método constutor da classe Text.

        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        if not pg.mixer.music.get_busy():
            try:
                pg.mixer.music.load(cst.MUSIC_TITLE)
                pg.mixer.music.play(-1)
            except pg.error as e:
                raise eg.MusicLoadError(f"Detalhes do erro: {e}")

        text_title = Text(self._display, "SPACIAL GAME", cst.FONT, cst.GREEN, 90, [self._width // 2, 200])
        play_button = Button(self._display, "PLAY", cst.FONT, cst.GREEN, 20, [self._width // 2, self._height - 250], 150, 30)
        credits_button = Button(self._display, "CREDITS", cst.FONT, cst.GREEN, 20, [self._width // 2, self._height - 180], 150, 30)
        exit_button = Button(self._display, "EXIT", cst.FONT, cst.GREEN, 20, [self._width // 2, self._height - 110], 150, 30)

        while self.waiting_player:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._quit()

            self.handle_button_press(play_button)
            self.handle_button_press(credits_button)
            self.handle_button_press(exit_button)

            self._load_background(cst.BACKGROUND_TITLE)

            text_title.draw()
            play_button.draw()
            credits_button.draw()
            exit_button.draw()

            self._clock.tick(cst.FPS)
            try:
                pg.display.update()
            except pg.error as e:
                raise eg.UpdateScreenError(f"Detalhes do erro: {e}")


class Credits(Interface):
    """
    Classe que controla a interface de Créditos do jogo.
    """

    def __init__(self, display: pg.Surface) -> None:
        """
        Método constutor da classe Credits.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        
        Returns
        -------
        None.
        """

        super().__init__(display)

    def run(self) -> None:
        """
        Método que atualiza a interface para a Tela de Créditos.

        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        text_colaboradores = Text(self._display, "COLABORADORES", cst.FONT, cst.BLACK, 60, [self._width // 2, 100])
        colaborador_1 = Text(self._display, "Alessandra Bello", cst.FONT, cst.WHITE, 30, [self._width // 2, 170])
        colaborador_2 = Text(self._display, "Edgard Junio", cst.FONT, cst.WHITE, 30, [self._width // 2, 240])
        colaborador_3 = Text(self._display, "Gilherme Ferrari", cst.FONT, cst.WHITE, 30, [self._width // 2, 310])
        colaborador_4 = Text(self._display, "Jeann Rocha", cst.FONT, cst.WHITE, 30, [self._width // 2, 380])
        exit_button = Button(self._display, "RETURN TO MENU", cst.FONT, cst.GREEN, 20, [self._width // 2, self._height - 110], 220, 30)

        while self.waiting_player:
            for event in pg.event.get():
                if event.type == QUIT:
                    self._quit()
            self.handle_button_press(exit_button)
            self._load_background(cst.BACKGROUND_PAUSE)

            text_colaboradores.draw()
            colaborador_1.draw()
            colaborador_2.draw()
            colaborador_3.draw()
            colaborador_4.draw()
            exit_button.draw()

            self._clock.tick(cst.FPS)
            try:
                pg.display.update()
            except pg.error as e:
                raise eg.UpdateScreenError(f"Detalhes do erro: {e}")


class Pause(Interface):
    """
    Classe que controla a interface de Tela de Pause do jogo.
    """

    def __init__(self, display: pg.Surface) -> None:
        """
        Método constutor da classe Pause.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        
        Returns
        -------
        None.
        """

        super().__init__(display)

    def run(self) -> None:
        """
        Método que atualiza a interface da Tela de Pause.
                
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        text_pause = Text(self._display, "PAUSE", cst.FONT, cst.GREEN, 90, [self._width // 2, 200])
        return_game_button = Button(self._display, "RETURN TO GAME", cst.FONT, cst.GREEN, 20, [self._width // 2, self._height - 250], 220, 30)
        return_menu_button = Button(self._display, "RETURN TO MENU", cst.FONT, cst.GREEN, 20, [self._width // 2, self._height - 180], 220, 30)

        while self.waiting_player:

            for event in pg.event.get():
                if event.type == QUIT:
                    self._quit()

            self.handle_button_press(return_game_button)
            self.handle_button_press(return_menu_button)

            self._load_background(cst.BACKGROUND_PAUSE)

            text_pause.draw()
            return_game_button.draw()
            return_menu_button.draw()

            self._clock.tick(cst.FPS)
            try:
                pg.display.update()
            except pg.error as e:
                raise eg.UpdateScreenError(f"Detalhes do erro: {e}")


class Reset(Interface):
    """
    Classe que controla a interface de Tela de Reset do jogo.
    """

    def __init__(self, display: pg.Surface, score: int) -> None:
        """
        Método constutor da classe Reset.

        Parameters
        ----------
        display : pg.Surface
            Tela onde acontece o jogo.
        score : int
            Score do jogador após o gameover
        
        Returns
        -------
        None.
        """

        super().__init__(display)
        self.__score = score

    def run(self) -> None:
        """
        Método que atualiza a interface da Tela de Reset.
                
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        text_tryagain = Text(self._display, "DESEJA JOGAR DE NOVO?", cst.FONT, cst.GREEN, 70, [self._width // 2, 150])
        score_button = Button(self._display, f"SCORE: {self.__score}", cst.FONT, cst.GREEN, 20, [self._width // 2, self._height - 440], 220, 30, is_selected=False)
        return_menu_button = Button(self._display, "RETURN TO MENU", cst.FONT, cst.GREEN, 20, [self._width // 2, self._height - 370], 220, 30)
        exit_button = Button(self._display, "EXIT", cst.FONT, cst.GREEN, 20, [self._width // 2, self._height - 300], 220, 30)

        while self.waiting_player:
            for event in pg.event.get():
                if event.type == QUIT:
                    self._quit()

            self.handle_button_press(return_menu_button)
            self.handle_button_press(exit_button)

            self._load_background(cst.BACKGROUND_GAMEOVER)

            text_tryagain.draw()
            score_button.draw()
            return_menu_button.draw()
            exit_button.draw()

            self._clock.tick(cst.FPS)
            try:
                pg.display.update()
            except pg.error as e:
                raise eg.UpdateScreenError(f"Detalhes do erro: {e}")
