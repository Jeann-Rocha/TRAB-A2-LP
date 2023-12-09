"""
Módulo que contém as classes e métodos para a construção dos tipos de interface do jogo.
"""

import pygame as pg
from pygame.locals import *

# import constants as cst
# import sprites as sp

class UIElement(ABC):
    """
    Classe abstrata que representa a criação de componentes visuais nas diversas
    interfaces da tela.
    """

    def __init__(self, display: pg.Surface, text: str, font: str, color: tuple, size: int, pos: tuple) -> None:
        self.display = display
        self.text = text
        self.font = pg.font.Font(font, size)
        self.color = color
        self.size = size
        self.pos_x = pos[0]
        self.pos_y = pos[1]

    @abstractmethod
    def draw(self):
        """
        Método abstrato que caracteriza o ato de desenhar coisas na tela.
        """

        pass

class Text(UIElement):
    """
    Classe que desenha textos na tela.
    """

    def __init__(self, display: pg.Surface, text: str, font: str, color: tuple, size: int, pos: tuple) -> None:
        super().__init__(display, text, font, color, size, pos)

    def draw(self) -> None:
        """
        Método que permite o desenho de textos na tela.
        """

        text = self.font.render(self.text, True, self.color)
        text_rect = text.get_rect(center=(self.pos_x, self.pos_y))
        self.display.blit(text, text_rect)

class Button(UIElement):
    """
    Classe que desenha butões (com textos) na tela.
    """

    def __init__(self, display: pg.Surface, text: str, font: str, color: tuple, size: int, pos: tuple, width: int, height: int) -> None:
        super().__init__(display, text, font, color, size, pos)

        self.text_font = font
        self.width = width
        self.height = height
        self.is_pressed = False
        self.color_button = cst.WHITE

    def draw(self) -> None:
        """
        Método que permite o desenho de butões na tela
        """

        # Coleta as posições do mouse
        mouse_x, mouse_y = pg.mouse.get_pos()

        # Condição para trocar de cor caso o mouse colida e verificar se houve click
        if (
            self.pos_x - self.width // 2 - 2 <= mouse_x <= self.pos_x - self.width // 2 + self.width + 2
        ) and (
            self.pos_y - self.height // 2 - 4 <= mouse_y <= self.pos_y - self.height // 2 + self.height + 2
        ):
            self.color_button = cst.BLUE
            if pg.mouse.get_pressed()[0]:
                self.is_pressed = True
            else:
                self.is_pressed = False
        else:
            self.color_button = cst.WHITE

        # Desenha a borda do botão
        pg.draw.rect(self.display, cst.BLACK, (self.pos_x - self.width // 2 - 2, self.pos_y - self.height // 2 - 4, self.width + 4, self.height + 6), 0)

        # Desenha o botão
        pg.draw.rect(self.display, self.color_button, (self.pos_x - self.width // 2, self.pos_y - self.height // 2 - 2, self.width, self.height), 0)

        # Desenha o texto do botão
        text = Text(self.display, self.text, self.text_font, self.color, self.size, [self.pos_x, self.pos_y])
        text.draw()

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
    Classe que controla a interface de Tela de pause do jogo.
    """
    pass


class Reset(Interface):
    """
    Classe que controla a interface de Tela de reset do jogo.
    """
    pass
