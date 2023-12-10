"""
Módulo que contém as classe principal do jogo, onde ocorrem os eventos,
criação de sprites e o funcionamento do gameloop.
"""

# Importando as bibliotecas
import time
import random

import pygame as pg
from pygame.locals import *

import constants as cst
import interface as intf
import sprites as sp
import exception_game as eg


class SpacialGame:
    """
    Classe principal do Jogo.
    """

    def __init__(self) -> None:
        """
        Método construtor da classe SpacialGame.
        
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        # Inicializando o Pygame
        pg.init()
        pg.mixer.init()
        pg.mixer.set_num_channels(100) # número de canais de som

        # Criando a Tela de Jogo
        self.__display = pg.display.set_mode((cst.WIDTH, cst.HEIGHT), pg.FULLSCREEN)
        pg.display.set_caption(cst.TITLE)

        # Criando o Relógio de FPS
        self.__clock = pg.time.Clock()

        self.__beginning()

    def __beginning(self):
        """
        Método que constrói a tela de início e encaminha para o início do jogo,
        criando os sprites, score e o gameloop.
        
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        # Criando uma pontuação para o jogador
        self.__score = 0

        # Criando variável que indicará se um item temporário ainda está ativo
        self.__item_effect_active = None 

        # Criando o GameLoop para o jogo
        self.__gameloop = True

        # Iniciando a Tela de Início do jogo
        title_screen = intf.Title(self.__display)
        title_screen.run()

        # Colocando a interface de Créditos caso esta seja chamada
        if title_screen.active_credit:
            credits = intf.Credits(self.__display)
            credits.run()
            if credits.active_reset:
                self.__beginning()

        # Delay para a mudança: Tela de Início -> Jogo
        time.sleep(0.25)

        # Iniciando os sprites (e os grupos) e o jogo
        self.__start_sprites()
        self.__playing()

    def __start_sprites(self):
        """
        Método onde se definem os objetos (sprites) do jogo.
        
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        # Criando os grupos para os sprites
        try:
            self.__objectGroup = pg.sprite.Group() # contém todos os sprites
            self.__playerGroup = pg.sprite.GroupSingle()
            self.__obstacleGroup = pg.sprite.Group()
            self.__shootPlayerGroup = pg.sprite.Group()
            self.__shootObstacleGroup = pg.sprite.Group()
            self.__bossGroup = pg.sprite.Group()
            self.__shootBossGroup = pg.sprite.Group()
            self.__itemGroup = pg.sprite.Group()
        except pg.error as e:
            raise eg.SpriteGroupError(f"Detalhes do erro: {e}")

        # Criando o Background e o Player do jogo.
        try:
            sp.Background(self.__display, cst.SCALE_BACKGROUND, cst.BACKGROUND_GAME, self.__objectGroup)
            self.__player = sp.Player(self.__display, cst.SCALE_PLAYER, cst.PLAYER, (self.__objectGroup, self.__playerGroup), group_shoot=self.__shootPlayerGroup)
        except ValueError as ve:
            raise eg.SpriteGroupError(f"Detalhes do erro: {ve}")

    def __playing(self):
        """
        Método onde se constrói a jogabilidade do jogo.
        
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        # Iniciar a musica do jogo
        try:
            pg.mixer.music.load(cst.MUSIC_GAME)
            pg.mixer.music.set_volume(0.5)
            pg.mixer.music.play(-1)
        except pg.error as e:
            raise eg.MusicLoadError(f"Detalhes do erro: {e}")

        # Variáveis úteis para a criação e definição dos parâmetros do boss
        is_boss = False
        life_boss = 5
        count_boss_died = 0 # quanto mais boss mortos, maior a vida e velocidade do próximo boss

        try:
            while self.__gameloop:
                self.__clock.tick(cst.FPS)
                self.__keys = pg.key.get_pressed()

                # Evento: sair do jogo
                for event in pg.event.get():
                    if event.type == QUIT:
                        self.__gameloop = False

                # Geração de obstáculos (caso não haja nenhum na tela e não haja boss)
                if len(self.__obstacleGroup.sprites()) == 0 and not is_boss:
                    try:
                        sp.Obstacle(self.__display, cst.SCALE_OBSTACLE, cst.OBSTACLE, self.__score, (self.__objectGroup, self.__obstacleGroup), group_shoot=self.__shootObstacleGroup)
                    except ValueError as ve:
                        raise eg.SpriteInstanceError(f"Detalhes do erro: {ve}")

                # Colisão de (player com obstáculo) ou (player com tiro do obstáculo) ou (player com tiro do boss)
                try:
                    if pg.sprite.groupcollide(self.__playerGroup, self.__obstacleGroup, False, True, pg.sprite.collide_mask) or pg.sprite.groupcollide(self.__playerGroup, self.__shootObstacleGroup, False, True, pg.sprite.collide_mask) or pg.sprite.groupcollide(self.__playerGroup, self.__bossGroup, False, False, pg.sprite.collide_mask) or pg.sprite.groupcollide(self.__playerGroup, self.__shootBossGroup, False, True, pg.sprite.collide_mask):
                        self.__player.lifes -= 1
                        self.__player.damaged = True
                except pg.error as e:
                    raise eg.CollisionError(f"Detalhes do erro: {e}")

                # Colisão de tiro do player com obstáculo
                try:
                    if pg.sprite.groupcollide(self.__shootPlayerGroup, self.__obstacleGroup, False, False, pg.sprite.collide_mask):
                        collisions = pg.sprite.groupcollide(self.__shootPlayerGroup, self.__obstacleGroup, True, False, pg.sprite.collide_mask)
                        for shoot in collisions:
                            obstacle_list = collisions[shoot]
                            for obstacle in obstacle_list:
                                obstacle.exploded = True
                        self.__score += 1
                except pg.error as e:
                    raise eg.CollisionError(f"Detalhes do erro: {e}")
                
                # Colisão de tiros
                try:
                    pg.sprite.groupcollide(self.__shootPlayerGroup, self.__shootObstacleGroup, True, True, pg.sprite.collide_mask) # player e obstáculo
                    pg.sprite.groupcollide(self.__shootPlayerGroup, self.__shootBossGroup, True, False, pg.sprite.collide_mask) # player e boss
                except pg.error as e:
                    raise eg.CollisionError(f"Detalhes do erro: {e}")
                
                # Condição para o surgimento de itens (de 15 em 15 pontos)
                if self.__score != 0 and self.__score % 15 == 0 and len(self.__itemGroup) == 0 and not is_boss:
                    item = random.choice(cst.ITEMS)
                    try:
                        sp.Items(self.__display, item[0], item[1], item[2], (self.__objectGroup, self.__itemGroup), player=self.__player)
                    except ValueError as ve:
                        raise eg.SpriteInstanceError(f"Detalhes do erro: {ve}")

                # Colisão de player com item: o player adquire as propriedades do item
                try:
                    if pg.sprite.groupcollide(self.__playerGroup, self.__itemGroup, False, False, pg.sprite.collide_mask):
                        collisions = pg.sprite.groupcollide(self.__playerGroup, self.__itemGroup, False, True, pg.sprite.collide_mask)
                        try:
                            take_item_sound = pg.mixer.Sound(cst.ITEM_SOUND)
                            take_item_sound.play()
                        except pg.error as e:
                            raise eg.SoundLoadError(f"Detalhes do erro: {e}")
                        item = list(collisions.values())[0][0]
                        self.__item_effect_active = item
                        item.apply_effect()
                except pg.error as e:
                    raise eg.CollisionError(f"Detalhes do erro: {e}")

                # Tela de pause
                if self.__keys[K_p]:
                    pause_screen = intf.Pause(self.__display)
                    pause_screen.run()
                    if pause_screen.active_reset:
                        self.__reset()

                # Condição para o surgimento do boss (de 20 em 20 pontos)
                if self.__score != 0 and self.__score % 20 == 0 and len(self.__bossGroup.sprites()) == 0:
                    is_boss = True
                    for _ in range(15):
                        for og in self.__obstacleGroup.sprites():
                            og.exploded = True
                        self.__kill_sprites(self.__shootObstacleGroup)
                        self.__kill_sprites(self.__shootPlayerGroup)
                        self.__objectGroup.draw(self.__display)
                        self.__objectGroup.update()
                        try:
                            pg.display.update()
                        except pg.error as e:
                            raise eg.UpdateScreenError(f"Detalhes do erro: {e}")
                    
                    try:
                        boss = sp.Boss(self.__display, cst.SCALE_BOSS, cst.BOSS, self.__score, life_boss + count_boss_died * 5, (self.__objectGroup, self.__bossGroup), group_shoot=self.__shootBossGroup)
                    except ValueError as ve:
                        raise eg.SpriteInstanceError(f"Detalhes do erro: {ve}")
                    while boss.speedx > 0:
                        self.__clock.tick(cst.FPS)
                        self.__bossGroup.draw(self.__display)
                        self.__bossGroup.update()
                        try:
                            pg.display.update()
                        except pg.error as e:
                            raise eg.UpdateScreenError(f"Detalhes do erro: {e}")
                        continue

                # Colisão de tiro do player com o boss
                try:
                    if pg.sprite.groupcollide(self.__shootPlayerGroup, self.__bossGroup, True, False, pg.sprite.collide_mask):
                        boss.lifes -= 1
                        boss.damaged = True
                        if boss.lifes == 0:
                            self.__score += 1
                            is_boss = False
                            count_boss_died += 1
                except pg.error as e:
                    raise eg.CollisionError(f"Detalhes do erro: {e}")

                # Atualizando a verificação de existência de boss para a criação de novos obstáculos
                sp.Obstacle.is_boss = is_boss

                # Desenhar os objetos na tela
                self.__objectGroup.draw(self.__display)
                self.__objectGroup.update()
                if self.__item_effect_active and (not self.__player.shooting_enabled or not self.__player.increase_speed_enabled):
                    # Exibir a imagem do item no topo da tela
                    self.__display.blit(self.__item_effect_active.image, (cst.WIDTH // 2 - self.__item_effect_active.rect.width // 2, 10))
                text_score = intf.Text(self.__display, f"SCORE: {self.__score}", cst.FONT, cst.GREEN, 30, [cst.WIDTH - 150, 50])
                text_score.draw()
                try:
                    pg.display.update()
                except pg.error as e:
                    raise eg.UpdateScreenError(f"Detalhes do erro: {e}")

                # Evento: você perdeu
                if self.__player.lifes == 0:
                    self.__gameover()
                try:
                    pg.display.update()
                except pg.error as e:
                    raise eg.UpdateScreenError(f"Detalhes do erro: {e}")
        except Exception as e:
            raise eg.GameLoopError(f"Detalhes do erro: {e}")

    

    def __kill_sprites(self, group):
        """
        Método onde se destroem todos os objetos (sprites) de um grupo e da tela.
        
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        for sprite in group.sprites():
            sprite.kill()

    def __reset(self):
        """
        Método onde se destroem todos os objetos (sprites) do jogo e, logo em
        seguida, efetua o reinício do mesmo.
        
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        # Removendo todos os sprites
        self.__kill_sprites(self.__objectGroup)

        # Redefinir o estado do efeito dos itens
        self.__item_effect_active = None

        # Reiniciando o jogo (retornando ao beginning())
        self.__beginning()

    def __gameover(self) -> None:
        """
        Método que atualiza um texto de gameover na tela e encaminha
        para a interface de reset.
        
        Parameters
        ----------
        
        Returns
        -------
        None.
        """

        # Texto: gameover
        pg.mixer.music.stop()
        text_gameover = intf.Text(self.__display, "GAME OVER", cst.FONT, cst.RED, 120, [cst.WIDTH // 2, cst.HEIGHT // 2])
        text_gameover.draw()
        try:
            pg.display.update()
        except pg.error as e:
            raise eg.UpdateScreenError(f"Detalhes do erro: {e}")

        # Efeitos sonoros para o gameover
        try:
            exterminate_sound = pg.mixer.Sound(cst.EXTERMINATE_SOUND)
            exterminate_sound.play()
            gameover_sound = pg.mixer.Sound(cst.GAMEOVER_SOUND)
            gameover_sound.play()
        except pg.error as e:
            raise eg.SoundLoadError(f"Detalhes do erro: {e}")

        time.sleep(3)
        self.__gameloop = False

        # Construindo a tela de reset
        reset_screen = intf.Reset(self.__display, self.__score)
        reset_screen.run()

        # Encaminhando para o reinício do jogo
        self.__reset()
