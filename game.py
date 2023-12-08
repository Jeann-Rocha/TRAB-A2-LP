"""
Módulo que contém as classe principal do jogo, onde ocorrem os eventos,
criação de sprites e o funcionamento do gameloop.
"""

# importando as bibliotecas
import constants as cst
import interface as intf
import sprites as sp

import pygame as pg
from pygame.locals import *
import time
import random


class SpacialGame:
    """
    Classe principal do Jogo.
    """

    def __init__(self) -> None:
        # Inicializando o Pygame
        pg.init()
        pg.mixer.init()
        pg.mixer.set_num_channels(100) # número de canais de som

        # Criando a Tela de Jogo
        self.display = pg.display.set_mode((cst.WIDTH, cst.HEIGHT))
        pg.display.set_caption(cst.TITLE)

        # Criando o Relógio de FPS
        self.clock = pg.time.Clock()

        self.beginning()

    def beginning(self):
        """
        Método que constrói a tela de início e encaminha para o início do jogo,
        criando os sprites, score e o gameloop.
        """
        # Criando uma pontuação para o Jogador
        self.score = 0

        # Criando o GameLoop para o Jogo
        self.gameloop = True

        # Iniciando a Tela de Início do Jogo
        title_screen = intf.Title(self.display)
        title_screen.run()

        settings = intf.Settings(self.display)

        if title_screen.active_settings:
            settings.run()
            if settings.active_reset:
                title_screen.waiting_player = True
                title_screen.run()

        # Delay para a Mudança: Tela de Início -> Jogo
        time.sleep(0.25)

        # Iniciando os Sprites (e os Grupos) e o Jogo
        self.start_sprites()
        self.playing()

    def start_sprites(self, difficulty="medium"):
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

        # Iniciar a musica do Jogo
        pg.mixer.music.load(cst.MUSIC_GAME)
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        is_boss = False
        life_boss = 10
        count_boss_died = 0

        while self.gameloop:
            self.clock.tick(cst.FPS)
            self.keys = pg.key.get_pressed()

            # evento: sair do jogo
            for event in pg.event.get():
                if event.type == QUIT:
                    self.gameloop = False

            # geração de obstáculos (caso não haja nenhum na tela e não haja boss)
            if len(self.obstacleGroup.sprites()) == 0 and not is_boss:
                sp.Obstacle(self.display, cst.SCALE_OBSTACLE, cst.OBSTACLE, self.score, (self.objectGroup, self.obstacleGroup), group_shoot=self.shootObstacleGroup)

            # colisão de (player com obstáculo) ou (player com tiro do obstáculo) ou (player com tiro do boss)
            if pg.sprite.groupcollide(self.playerGroup, self.obstacleGroup, False, True, pg.sprite.collide_mask) or pg.sprite.groupcollide(self.playerGroup, self.shootObstacleGroup, False, True, pg.sprite.collide_mask) or pg.sprite.groupcollide(self.playerGroup, self.bossGroup, False, False, pg.sprite.collide_mask) or pg.sprite.groupcollide(self.playerGroup, self.shootBossGroup, False, True, pg.sprite.collide_mask):
                self.player.lifes -= 1

            # colisão de tiro do player com obstáculo
            if pg.sprite.groupcollide(self.shootPlayerGroup, self.obstacleGroup, False, False, pg.sprite.collide_mask):
                collisions = pg.sprite.groupcollide(self.shootPlayerGroup, self.obstacleGroup, True, False, pg.sprite.collide_mask)
                for shoot in collisions:
                    obstacle_list = collisions[shoot]
                    for obstacle in obstacle_list:
                        obstacle.exploded = True
                self.score += 1
            
            # colisão de tiros
            pg.sprite.groupcollide(self.shootPlayerGroup, self.shootObstacleGroup, True, True, pg.sprite.collide_mask)
            pg.sprite.groupcollide(self.shootPlayerGroup, self.shootBossGroup, True, False, pg.sprite.collide_mask)

            if self.score != 0 and self.score % 15 == 0 and len(self.itemGroup) == 0 and not is_boss:
                item = random.choice(cst.ITEMS)
                self.item = sp.Items(self.display, item[0], item[1], item[2], (self.objectGroup, self.itemGroup), player=self.player)

            if pg.sprite.groupcollide(self.playerGroup, self.itemGroup, False, True, pg.sprite.collide_mask):
                self.item.apply_effect()

            # tela de pause
            if self.keys[K_p]:
                pause_screen = intf.Pause(self.display)
                pause_screen.run()
                if pause_screen.active_reset:
                    self.kill_all_sprites()
                    self.beginning()
                elif pause_screen.active_settings:
                    settings = intf.Settings(self.display)
                    settings.run()
                    if settings.active_reset:
                        self.kill_all_sprites()
                        self.beginning()

            # evento: o boss surge
            if self.score != 0 and self.score % 20 == 0 and len(self.bossGroup.sprites()) == 0:
                is_boss = True
                for _ in range(20):
                    for og in self.obstacleGroup.sprites():
                        og.exploded = True
                    self.kill_sprites(self.shootObstacleGroup)
                    self.kill_sprites(self.shootPlayerGroup)
                    self.objectGroup.draw(self.display)
                    self.objectGroup.update()
                    pg.display.update()
                
                boss = sp.Boss(self.display, cst.SCALE_BOSS, cst.BOSS, self.score, life_boss + count_boss_died * 5, (self.objectGroup, self.bossGroup), group_shoot=self.shootBossGroup)
                while boss.speedx > 0:
                    self.clock.tick(cst.FPS)
                    self.bossGroup.draw(self.display)
                    self.bossGroup.update()
                    pg.display.update()
                    continue

            # colisão de tiro do player com o boss
            if pg.sprite.groupcollide(self.shootPlayerGroup, self.bossGroup, True, False, pg.sprite.collide_mask):
                boss.lifes -= 1
                if boss.lifes == 0:
                    self.score += 1
                    is_boss = False
                    count_boss_died += 1

            sp.Obstacle.is_boss = is_boss

            # desenhar os objetos na tela
            self.objectGroup.draw(self.display)
            self.objectGroup.update()

            text_score = intf.Text(self.display, f"SCORE: {self.score}", cst.FONT, cst.GREEN, 30, [cst.WIDTH - 150, 50])
            text_score.draw()

            pg.display.update()

            # evento: você perdeu
            if self.player.lifes == 0:
                self.gameover()

            pg.display.update()

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

        # texto: gameover
        pg.mixer.music.stop()
        text_gameover = intf.Text(self.display, "GAME OVER", cst.FONT, cst.RED, 120, [cst.WIDTH // 2, cst.HEIGHT // 2])
        text_gameover.draw()
        pg.display.update()

        # efeitos sonoros para o gameover
        exterminate_sound = pg.mixer.Sound(cst.EXTERMINATE_SOUND)
        exterminate_sound.play()
        gameover_sound = pg.mixer.Sound(cst.GAMEOVER_SOUND)
        gameover_sound.play()

        time.sleep(3)
        self.gameloop = False

        # construindo a tela de reset
        reset_screen = intf.Reset(self.display)
        reset_screen.run()

        # encaminhando para o reinício do jogo
        self.kill_all_sprites()
        self.beginning()

