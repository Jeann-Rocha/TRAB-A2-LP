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

        # Criando uma pontuação para o jogador
        self.score = 0

        # Criando variável que indicará se um item temporário ainda está ativo
        self.item_effect_active = None 

        # Criando o GameLoop para o jogo
        self.gameloop = True

        # Iniciando a Tela de Início do jogo
        title_screen = intf.Title(self.display)
        title_screen.run()

        # Colocando a interface de Créditos caso esta seja chamada
        if title_screen.active_credit:
            credits = intf.Credits(self.display)
            credits.run()
            if credits.active_reset:
                self.beginning()

        # Delay para a mudança: Tela de Início -> Jogo
        time.sleep(0.25)

        # Iniciando os sprites (e os grupos) e o jogo
        self.start_sprites()
        self.playing()

    def start_sprites(self):
        """
        Método onde se definem os objetos (sprites) do jogo.
        """

        # Criando os grupos para os sprites
        self.objectGroup = pg.sprite.Group() # contém todos os sprites
        self.playerGroup = pg.sprite.GroupSingle()
        self.obstacleGroup = pg.sprite.Group()
        self.shootPlayerGroup = pg.sprite.Group()
        self.shootObstacleGroup = pg.sprite.Group()
        self.bossGroup = pg.sprite.Group()
        self.shootBossGroup = pg.sprite.Group()
        self.itemGroup = pg.sprite.Group()

        # Criando o Background e o Player do jogo.
        sp.Background(self.display, cst.SCALE_BACKGROUND, cst.BACKGROUND_GAME, self.objectGroup)
        self.player = sp.Player(self.display, cst.SCALE_PLAYER, cst.PLAYER, (self.objectGroup, self.playerGroup), group_shoot=self.shootPlayerGroup)

    def playing(self):
        """
        Método onde se constrói a jogabilidade do jogo.
        """

        # Iniciar a musica do jogo
        pg.mixer.music.load(cst.MUSIC_GAME)
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)

        # Variáveis úteis para a criação e definição dos parâmetros do boss
        is_boss = False
        life_boss = 5
        count_boss_died = 0 # quanto mais boss mortos, maior a vida e velocidade do próximo boss

        while self.gameloop:
            self.clock.tick(cst.FPS)
            self.keys = pg.key.get_pressed()

            # Evento: sair do jogo
            for event in pg.event.get():
                if event.type == QUIT:
                    self.gameloop = False

            # Geração de obstáculos (caso não haja nenhum na tela e não haja boss)
            if len(self.obstacleGroup.sprites()) == 0 and not is_boss:
                sp.Obstacle(self.display, cst.SCALE_OBSTACLE, cst.OBSTACLE, self.score, (self.objectGroup, self.obstacleGroup), group_shoot=self.shootObstacleGroup)

            # Colisão de (player com obstáculo) ou (player com tiro do obstáculo) ou (player com tiro do boss)
            if pg.sprite.groupcollide(self.playerGroup, self.obstacleGroup, False, True, pg.sprite.collide_mask) or pg.sprite.groupcollide(self.playerGroup, self.shootObstacleGroup, False, True, pg.sprite.collide_mask) or pg.sprite.groupcollide(self.playerGroup, self.bossGroup, False, False, pg.sprite.collide_mask) or pg.sprite.groupcollide(self.playerGroup, self.shootBossGroup, False, True, pg.sprite.collide_mask):
                self.player.lifes -= 1
                self.player.damaged = True

            # Colisão de tiro do player com obstáculo
            if pg.sprite.groupcollide(self.shootPlayerGroup, self.obstacleGroup, False, False, pg.sprite.collide_mask):
                collisions = pg.sprite.groupcollide(self.shootPlayerGroup, self.obstacleGroup, True, False, pg.sprite.collide_mask)
                for shoot in collisions:
                    obstacle_list = collisions[shoot]
                    for obstacle in obstacle_list:
                        obstacle.exploded = True
                self.score += 1
            
            # Colisão de tiros
            pg.sprite.groupcollide(self.shootPlayerGroup, self.shootObstacleGroup, True, True, pg.sprite.collide_mask) # player e obstáculo
            pg.sprite.groupcollide(self.shootPlayerGroup, self.shootBossGroup, True, False, pg.sprite.collide_mask) # player e boss

            # Condição para o surgimento de itens (de 15 em 15 pontos)
            if self.score != 0 and self.score % 15 == 0 and len(self.itemGroup) == 0 and not is_boss:
                item = random.choice(cst.ITEMS)
                sp.Items(self.display, item[0], item[1], item[2], (self.objectGroup, self.itemGroup), player=self.player)

            # Colisão de player com item: o player adquire as propriedades do item
            if pg.sprite.groupcollide(self.playerGroup, self.itemGroup, False, False, pg.sprite.collide_mask):
                collisions = pg.sprite.groupcollide(self.playerGroup, self.itemGroup, False, True, pg.sprite.collide_mask)
                take_item_sound = pg.mixer.Sound(cst.ITEM_SOUND)
                take_item_sound.play()
                item = list(collisions.values())[0][0]
                self.item_effect_active = item
                item.apply_effect()

            # Tela de pause
            if self.keys[K_p]:
                pause_screen = intf.Pause(self.display)
                pause_screen.run()
                if pause_screen.active_reset:
                    self.reset()

            # Condição para o surgimento do boss (de 20 em 20 pontos)
            if self.score != 0 and self.score % 20 == 0 and len(self.bossGroup.sprites()) == 0:
                is_boss = True
                for _ in range(15):
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

            # Colisão de tiro do player com o boss
            if pg.sprite.groupcollide(self.shootPlayerGroup, self.bossGroup, True, False, pg.sprite.collide_mask):
                boss.lifes -= 1
                boss.damaged = True
                if boss.lifes == 0:
                    self.score += 1
                    is_boss = False
                    count_boss_died += 1

            # Atualizando a verificação de existência de boss para a criação de novos obstáculos
            sp.Obstacle.is_boss = is_boss

            # Desenhar os objetos na tela
            self.objectGroup.draw(self.display)
            self.objectGroup.update()
            if self.item_effect_active and (not self.player.shooting_enabled or not self.player.increase_speed_enabled):
                # Exibir a imagem do item no topo da tela
                self.display.blit(self.item_effect_active.image, (cst.WIDTH // 2 - self.item_effect_active.rect.width // 2, 10))
            text_score = intf.Text(self.display, f"SCORE: {self.score}", cst.FONT, cst.GREEN, 30, [cst.WIDTH - 150, 50])
            text_score.draw()
            pg.display.update()

            # Evento: você perdeu
            if self.player.lifes == 0:
                self.gameover()
            pg.display.update()
    

    def kill_sprites(self, group):
        """
        Método onde se destroem todos os objetos (sprites) de um grupo e da tela.
        """

        for sprite in group.sprites():
            sprite.kill()

    def reset(self):
        """
        Método onde se destroem todos os objetos (sprites) do jogo e, logo em
        seguida, efetua o reinício do mesmo.
        """

        # Removendo todos os sprites
        self.kill_sprites(self.objectGroup)

        # Redefinir o estado do efeito dos itens
        self.item_effect_active = None

        # Reiniciando o jogo (retornando ao beginning())
        self.beginning()

    def gameover(self) -> None:
        """
        Método que atualiza um texto de gameover na tela e encaminha
        para a interface de reset.
        """

        # Texto: gameover
        pg.mixer.music.stop()
        text_gameover = intf.Text(self.display, "GAME OVER", cst.FONT, cst.RED, 120, [cst.WIDTH // 2, cst.HEIGHT // 2])
        text_gameover.draw()
        pg.display.update()

        # Efeitos sonoros para o gameover
        exterminate_sound = pg.mixer.Sound(cst.EXTERMINATE_SOUND)
        exterminate_sound.play()
        gameover_sound = pg.mixer.Sound(cst.GAMEOVER_SOUND)
        gameover_sound.play()

        time.sleep(3)
        self.gameloop = False

        # Construindo a tela de reset
        reset_screen = intf.Reset(self.display)
        reset_screen.run()

        # Encaminhando para o reinício do jogo
        self.reset()
