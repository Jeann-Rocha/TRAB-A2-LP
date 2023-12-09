"""
Módulo que contém as classes e métodos para a construção dos sprites do jogo.
"""

import constants as cst

import pygame as pg
from pygame.locals import *
import random
import threading
import time

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
    def __init__(self, display, scale, path_images, *groups) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)
        
        self.pos_width = self.display.get_width()
        self.speed = 1


    def update(self):
        """
        Método que atualiza o background para movimentar-se enquanto o jogador
        estiver jogando para dar um efeito de dinamicidade ao jogo.
        """

        self.display.blit(self.image, (0, 0))

        rel_x = self.pos_width % self.image.get_rect().width
        self.display.blit(self.image, (rel_x - self.image.get_rect().width, 0))
        if rel_x < 1200:
            self.display.blit(self.image, (rel_x, 0))
        self.pos_width -= self.speed


class Player(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para o player (jogador) do jogo.
    """

    def __init__(self, display: pg.Surface , scale: list, path_images: list, *groups, group_shoot: pg.sprite.Group) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        # posição inicial do player
        self.rect.x = 0
        self.rect.y = self.display.get_height() // 2

        self.timer_shoot = 0
        self.timer_shoot_max = 10
        self.group_shoot = group_shoot

        self.damaged = False # indicador de que o player levou dano
        self.lifes = 3
        self.speed = 30
        self.animation_speed = 10

        self.shooting_enabled = True
        self.reset_timer = None

        self.increase_speed_enabled = True
        self.reset_speed_timer = None

    def update(self):
        """
        Método que atualiza os movimentos e tiros do player.
        """

        if self.damaged:
            self.damaged = False
            # colocar som de dano no player...
        else:
            self.display.blit(self.image, (self.rect.x, self.rect.y))

        self.keys = pg.key.get_pressed()

        self.animate()
        if self.animation_speed >= 2:
            self.animation_speed -= 0.05 # efetio contínuo de aumento da velocidade
        self.movements()
        self.shoot_player()
        self.draw_lifes()

    def movements(self):
        """
        Método que atualiza os movimentos do player e limita os mesmos
        para as bordas da tela.
        """

        # diagonal superior esquerda
        if self.keys[K_w] and self.keys[K_a]:
            self.rect.x -= self.speed
            self.rect.y -= self.speed
        # diagonal superior direita
        elif self.keys[K_w] and self.keys[K_d]:
            self.rect.x += self.speed
            self.rect.y -= self.speed
        # diagonal inferior esquerda
        elif self.keys[K_s] and self.keys[K_a]:
            self.rect.x -= self.speed
            self.rect.y += self.speed
        # diagonal inferior direita
        elif self.keys[K_s] and self.keys[K_d]:
            self.rect.x += self.speed
            self.rect.y += self.speed
        # cima
        elif self.keys[K_w]:
            self.rect.y -= self.speed
        # baixo
        elif self.keys[K_s]:
            self.rect.y += self.speed
        # esquerda
        elif self.keys[K_a]:
            self.rect.x -= self.speed
        # direita
        elif self.keys[K_d]:
            self.rect.x += self.speed

        # borda superior
        if self.rect.top < 0:
            self.rect.top = 0
        # borda inferior
        if self.rect.bottom > self.display.get_height():
            self.rect.bottom = self.display.get_height()
        # borda lateral esquerda
        if self.rect.left < 0:
            self.rect.left = 0
        # borda lateral direita
        if self.rect.right > self.display.get_width():
            self.rect.right = self.display.get_width()

    def shoot_player(self):
        """
        Método que atualiza os tiros do player.
        """

        self.timer_shoot += 1
        if self.timer_shoot > self.timer_shoot_max:
            if self.keys[K_SPACE]:
                self.timer_shoot = 0
                Shoot(self.display, cst.SCALE_SHOOT, cst.SHOOT_PLAYER, self.rect.topright, False, 0, (self.groups[0], self.group_shoot))
                shoot_sound = pg.mixer.Sound(cst.SHOOT_SOUND)
                shoot_sound.play()


    def increase_fire_rate(self):
        """
        Método para aumentar temporariamente a taxa de tiro.
        """
        self.shooting_enabled = False
        self.timer_shoot_max = 2

        # Inicia um temporizador para voltar ao timer_shoot_max após 10 segundos
        self.reset_timer = threading.Timer(10, self._reset_fire_rate)
        self.reset_timer.start()

    def _reset_fire_rate(self):
        """
        Método chamado pelo temporizador para reverter as alterações após a duração.
        """
        self.timer_shoot_max = 10
        self.shooting_enabled = True

    def increase_speed(self):
        """
        Método para aumentar temporariamente a velocidade do player.
        """
        self.increase_speed_enabled = False
        self.speed = 50

        # Inicia um temporizador para voltar ao speed após 10 segundos
        self.reset_speed_timer = threading.Timer(10, self._reset_speed)
        self.reset_speed_timer.start()

    def _reset_speed(self):
        """
        Método chamado pelo temporizador para reverter as alterações após a duração.
        """
        self.speed = 30
        self.increase_speed_enabled = True


class Obstacle(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para os obstáculos do jogo.
    """
    
    is_boss = False
    timer_shoot = 0

    def __init__(self, display, scale, path_images, speed_increment, *groups, group_shoot) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        self.group_shoot = group_shoot
        self.rect.x = self.display.get_width()
        self.rect.y = random.randint(0, display.get_height() - scale[1])
        self.speed_increment = speed_increment
        self.speed = speed_increment / 5 + random.randint(10, 30)


    def update(self):
        """
        Método que atualiza os movimentos dos obstáculos, que estão
        pré-definidos pelo jogo.
        """

        if not self.rect.right < 0 and not self.exploded:
            self.display.blit(self.image, (self.rect.x, self.rect.y))

            self.rect.x -= self.speed

            if not self.is_boss:
                self.new_obstacles()
            self.shoot_obstacles()
            self.animate()
        else:
            self.display.blit(self.image, (self.rect.x, self.rect.y))
            self.animate_explosion()

        if self.rect.right < 0 or self.exploded:
            self.groups[1].remove(self)

    def new_obstacles(self):
        """
        Método que gera (aleatoriamente) novos obstáculos.
        """

        new_obstacles = random.randint(1, 4)
        if len(self.groups[1].sprites()) <= 2:
            if random.random() < 0.03:
                for _ in range(new_obstacles):
                    Obstacle(self.display, cst.SCALE_OBSTACLE, cst.OBSTACLE, self.speed_increment, (self.groups[0], self.groups[1]), group_shoot=self.group_shoot)


    def shoot_obstacles(self):
        """
        Método que atualiza os tiros do obstáculo.
        """

        self.timer_shoot += 1
        if self.timer_shoot > 70:
            self.timer_shoot = 0
            obstacles_choice = random.sample(self.groups[1].sprites(), random.randint(0, len(self.groups[1].sprites())))
            for oc in obstacles_choice:
                Shoot(self.display, cst.SCALE_SHOOT, cst.SHOOT_OBSTACLE, (oc.rect.left, oc.rect.centery), True, oc.speed, (self.groups[0], self.group_shoot))
            for ob in self.groups[1].sprites():
                ob.timer_shoot = 0
            shoot_sound = pg.mixer.Sound(cst.SHOOT_SOUND)
            shoot_sound.play()


class Shoot(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para os disparos (tiros) do jogo.
    """

    def __init__(self, display, scale, path_images, pos, speed_sprite, is_obstacle=False, *groups) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        self.is_obstacle = is_obstacle
        self.obstacle = None
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        shoot_sound = pg.mixer.Sound(cst.SHOOT_SOUND)
        shoot_sound.play()

        self.speed = speed_sprite + 5
    

    def update(self):
        """
        Método que atualiza os movimentos do tiro, que estão
        pré-definidos pelo jogo.
        """

        self.display.blit(self.image, (self.rect.x, self.rect.y))

        self.animate()

        if self.is_obstacle:
            self.rect.x -= self.speed

            if self.rect.right < 0:
                self.kill()
        else:
            self.rect.x += self.speed

            if self.rect.left > self.display.get_width():
                self.kill()


class Boss(pg.sprite.Sprite, Render):
    """
    Classe de Sprite(s) para o boss do jogo.
    """

    speedx = 5

    def __init__(self, display, scale, path_images, speed_increment, *groups, group_shoot) -> None:
        pg.sprite.Sprite.__init__(self, *groups)
        Render.__init__(self, display, scale, path_images, *groups)

        self.animation_speed = 10
        self.lifes = 10
        self.rect.x = self.display.get_width()
        self.rect.y = 0
        self.speedy = speed_increment / 5 + 20
        self.verificate_speedy = "DOWN"
        self.speed = speed_increment / 5

        self.group_shoot = group_shoot
        self.last_shoot_time = 0
        self.start_time = time.time()
        boss_sound = pg.mixer.Sound(cst.BOSS_SOUND_1)
        boss_sound.play()


    def shoot_boss(self):
        current_time = time.time() + 2
        time_on_screen = current_time - self.start_time

        if time_on_screen >= 5 and current_time - self.last_shoot_time >= 2:
                self.last_shoot_time = current_time
                Shoot(self.display, cst.SCALE_SHOOT_BOSS, cst.SHOOT_BOSS, (self.rect.left, random.uniform(self.rect.top, self.rect.bottom)), self.speed, True, (self.groups[0], self.group_shoot))


    def update(self):
        """
        Método que atualiza os movimentos do boss, que estão
        pré-definidos pelo jogo.
        """

        if self.rect.right < 0 or self.exploded:
            self.groups[1].remove(self)

        self.display.blit(self.image, (self.rect.x, self.rect.y))

        self.rect.x -= self.speedx

        if self.rect.right <= self.display.get_width():
            self.speedx = 0

        if self.speedx == 0:
            if not self.exploded:
                if self.rect.top < 0:
                    self.verificate_speedy = "DOWN"
                if self.rect.bottom > self.display.get_height():
                    self.verificate_speedy = "UP"
                if self.verificate_speedy == "DOWN":
                    self.rect.y += self.speedy
                elif self.verificate_speedy == "UP":
                    self.rect.y -= self.speedy
                self.animate()
            else:
                self.display.blit(self.image, (self.rect.x, self.rect.y))
                self.animate_explosion()

        if self.lifes <= 0:
            self.exploded = True
            self.groups[1].empty()
        self.shoot_boss()

