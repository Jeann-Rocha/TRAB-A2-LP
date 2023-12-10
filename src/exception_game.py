"""
Módulo que contém as exceções próprias para o jogo.
"""

class MusicLoadError(Exception):
    """
    Classe que detecta se houve erro ao carregar música.
    """

    def __init__(self, message="Erro ao carregar música.") -> None:
        """
        Método construtor da classe MusicLoadError.

        Parameters
        ----------
        message: str (Opcional)
            Mensagem de erro.

        Returns
        -------
        None.
        """

        self.message = message
        super().__init__(self.message)


class SoundLoadError(Exception):
    """
    Classe que detecta se houve erro ao carregar efeito sonoro.
    """

    def __init__(self, message="Erro ao carregar efeito sonoro.") -> None:
        """
        Método construtor da classe SoundLoadError.

        Parameters
        ----------
        message: str (Opcional)
            Mensagem de erro.

        Returns
        -------
        None.
        """
        
        self.message = message
        super().__init__(self.message)


class SpriteGroupError(Exception):
    """
    Classe que detecta se houve erro ao criar grupos de sprites.
    """
    
    def __init__(self, message="Erro ao criar grupos de sprites.") -> None:
        """
        Método construtor da classe SpriteGroupError.

        Parameters
        ----------
        message: str (Opcional)
            Mensagem de erro.

        Returns
        -------
        None.
        """
        
        self.message = message
        super().__init__(self.message)


class GameLoopError(Exception):
    """
    Classe que detecta se houve erro durante a execução do gameloop.
    """
    
    def __init__(self, message="Erro durante a execução do gameloop.") -> None:
        """
        Método construtor da classe GameLoopError.

        Parameters
        ----------
        message: str (Opcional)
            Mensagem de erro.

        Returns
        -------
        None.
        """
        
        self.message = message
        super().__init__(self.message)


class SpriteInstanceError(Exception):
    """
    Classe que detecta se houve erro ao criar instâncias de sprites.
    """
    
    def __init__(self, message="Erro ao criar instâncias de sprites.") -> None:
        """
        Método construtor da classe SpriteInstanceError.

        Parameters
        ----------
        message: str (Opcional)
            Mensagem de erro.

        Returns
        -------
        None.
        """
        
        self.message = message
        super().__init__(self.message)


class CollisionError(Exception):
    """
    Classe que detecta se houve erro durante a colisão de sprites.
    """

    def __init__(self, message="Erro durante a colisão de sprites.") -> None:
        """
        Método construtor da classe CollisionError.

        Parameters
        ----------
        message: str (Opcional)
            Mensagem de erro.

        Returns
        -------
        None.
        """
        
        self.message = message
        super().__init__(self.message)


class UpdateScreenError(Exception):
    """
    Classe que detecta se houve erro durante a atualização da tela.
    """

    def __init__(self, message="Erro durante a atualização da tela.") -> None:
        """
        Método construtor da classe UpdateScreenError.

        Parameters
        ----------
        message: str (Opcional)
            Mensagem de erro.

        Returns
        -------
        None.
        """
        
        self.message = message
        super().__init__(self.message)
    