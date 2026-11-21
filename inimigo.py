
import time
import math
import random

import pygame
from PPlay.gameimage import GameImage


def verificar_colisao(jogador, inimigo):

    largura_jogador = jogador.parado_direita.width
    altura_jogador = jogador.parado_direita.height

    margem = inimigo.sprite.width * 0.20

    hitbox_x = inimigo.x + margem
    hitbox_largura = inimigo.sprite.width - (margem * 2)

    return (
        hitbox_x < jogador.x + largura_jogador
        and hitbox_x + hitbox_largura > jogador.x
        and inimigo.y < jogador.y + altura_jogador
        and inimigo.y + inimigo.sprite.height > jogador.y
    )


class Inimigo:

    def __init__(self, pasta_assets, x, altura_chao, velocidade=100):

        self.sprite_esquerda = GameImage(
            str(pasta_assets / "dinossauro_e.png")
        )

        self.sprite_direita = GameImage(
            str(pasta_assets / "dinossauro_d.png")
        )

        self.sprite = self.sprite_esquerda

        self.x = x
        self.y = altura_chao - self.sprite.height

        self.velocidade = velocidade
        self.morto = False

        self.comportamento = random.choice([
            "perseguidor",
            "estrategico",
            "flanqueador"
        ])

        self.distancia_alvo = random.randint(90, 180)
        self.alvo_x = self.x

        self.velocidade += random.randint(-15, 20)

        self.sprite.x = self.x
        self.sprite.y = self.y

    def atualizar(self, jogador, janela):

        if self.morto:
            return

        dt = janela.delta_time()

        centro_jogador = (
            jogador.x + jogador.parado_direita.width / 2
        )

        centro_inimigo = self.x + self.sprite.width / 2

        diferenca = centro_jogador - centro_inimigo

        if self.comportamento == "perseguidor":

            self.alvo_x = centro_jogador - self.sprite.width / 2

        elif self.comportamento == "estrategico":

            previsao = jogador.x + (
                jogador.velocidade * dt * 35
            )

            if diferenca > 0:
                self.alvo_x = previsao + self.distancia_alvo
            else:
                self.alvo_x = previsao - self.distancia_alvo

        elif self.comportamento == "flanqueador":

            if jogador.direcao == "direita":
                self.alvo_x = jogador.x - self.distancia_alvo
            else:
                self.alvo_x = jogador.x + self.distancia_alvo

        self.alvo_x = max(
            0,
            min(
                self.alvo_x,
                janela.width - self.sprite.width
            )
        )

        if self.x < self.alvo_x:

            self.x += self.velocidade * dt
            self.sprite = self.sprite_direita

        elif self.x > self.alvo_x:

            self.x -= self.velocidade * dt
            self.sprite = self.sprite_esquerda

        if abs(self.x - self.alvo_x) < 3:
            self.x = self.alvo_x

        self.sprite.x = self.x
        self.sprite.y = self.y

    def desenhar(self):

        if not self.morto:
            self.sprite.draw()

    def colidiu_com(self, jogador):

        return verificar_colisao(jogador, self)

    def morrer(self):

        self.morto = True


class Inseto:

    def __init__(self, pasta_assets, x, y, velocidade=130):

        self.sprite_esquerda = GameImage(
            str(pasta_assets / "inseto_e.png")
        )

        self.sprite_direita = GameImage(
            str(pasta_assets / "inseto_d.png")
        )

        self.sprite = self.sprite_esquerda

        self.x = x
        self.y = y + 40

        self.y_inicial = self.y

        self.velocidade = velocidade
        self.morto = False

        self.sprite.x = self.x
        self.sprite.y = self.y

    def atualizar(self, jogador, janela):

        if self.morto:
            return

        dt = janela.delta_time()

        if self.x < jogador.x:

            self.x += self.velocidade * dt
            self.sprite = self.sprite_direita

        elif self.x > jogador.x:

            self.x -= self.velocidade * dt
            self.sprite = self.sprite_esquerda

        self.y = (
            self.y_inicial
            + 20 * math.sin(time.time() * 4)
        )

        self.sprite.x = self.x
        self.sprite.y = self.y

    def desenhar(self):

        if not self.morto:
            self.sprite.draw()

    def colidiu_com(self, jogador):

        return verificar_colisao(jogador, self)

    def morrer(self):

        self.morto = True


class InimigoMedieval:

    def __init__(
        self,
        pasta_assets,
        x,
        altura_chao,
        arquivo_esquerda,
        arquivo_direita,
        velocidade
    ):

        self.sprite_esquerda = GameImage(
            str(pasta_assets / arquivo_esquerda)
        )

        self.sprite_direita = GameImage(
            str(pasta_assets / arquivo_direita)
        )

        self.sprite = self.sprite_esquerda

        self.x = x
        self.y = altura_chao - self.sprite.height

        self.velocidade = velocidade
        self.morto = False

        self.sprite.x = self.x
        self.sprite.y = self.y

    def atualizar(self, jogador, janela):

        if self.morto:
            return

        dt = janela.delta_time()

        centro_jogador = (
            jogador.x + jogador.parado_direita.width / 2
        )

        centro_inimigo = (
            self.x + self.sprite.width / 2
        )

        if centro_inimigo < centro_jogador:

            self.x += self.velocidade * dt
            self.sprite = self.sprite_direita

        elif centro_inimigo > centro_jogador:

            self.x -= self.velocidade * dt
            self.sprite = self.sprite_esquerda

        self.x = max(
            0,
            min(
                self.x,
                janela.width - self.sprite.width
            )
        )

        self.sprite.x = self.x
        self.sprite.y = self.y

    def desenhar(self):

        if not self.morto:
            self.sprite.draw()

    def colidiu_com(self, jogador):

        return verificar_colisao(jogador, self)

    def morrer(self):

        self.morto = True


class Cavaleiro(InimigoMedieval):

    def __init__(self, pasta_assets, x, altura_chao):

        super().__init__(
            pasta_assets,
            x,
            altura_chao,
            "cavaleiro_e.png",
            "cavaleiro_d.png",
            velocidade=115
        )


class Esqueleto(InimigoMedieval):

    esqueletos_ativos = []
    esqueleto_atirador = None

    def __init__(self, pasta_assets, x, altura_chao):

        super().__init__(
            pasta_assets,
            x,
            altura_chao,
            "esqueleto_e.png",
            "esqueleto_d.png",
            velocidade=95
        )

        self.projeteis = []
        self.intervalo_disparo = 2
        self.ultimo_disparo = time.time()
        self.pasta_assets = pasta_assets
        self.disparou_turno = False

        Esqueleto.esqueletos_ativos.append(self)

    @classmethod
    def escolher_atirador(cls):

        cls.esqueletos_ativos = [
            esqueleto
            for esqueleto in cls.esqueletos_ativos
            if not esqueleto.morto
        ]

        if cls.esqueleto_atirador is not None:
            if cls.esqueleto_atirador.morto:
                cls.esqueleto_atirador = None

        if cls.esqueleto_atirador is None and cls.esqueletos_ativos:
            cls.esqueleto_atirador = random.choice(
                cls.esqueletos_ativos
            )

    def disparar(self, jogador):

        agora = time.time()

        if agora - self.ultimo_disparo < self.intervalo_disparo:
            return

        centro_jogador = (
            jogador.x + jogador.parado_direita.width / 2
        )

        centro_esqueleto = (
            self.x + self.sprite.width / 2
        )

        if centro_jogador >= centro_esqueleto:

            direcao = 1
            arquivo_flecha = "fecha_d.png"
            x = self.x + self.sprite.width

        else:

            direcao = -1
            arquivo_flecha = "fecha_e.png"

            flecha_temporaria = GameImage(
                str(self.pasta_assets / arquivo_flecha)
            )

            x = self.x - flecha_temporaria.width

        projetil = Projetil(
            self.pasta_assets,
            x,
            0,
            direcao,
            arquivo=arquivo_flecha
        )

        projetil.y = (
            self.y
            + (self.sprite.height / 2)
            - (projetil.sprite.height / 2)
        )

        projetil.sprite.x = projetil.x
        projetil.sprite.y = projetil.y

        self.projeteis.append(projetil)

        self.ultimo_disparo = agora
        self.disparou_turno = True

    def atualizar(self, jogador, janela):

        super().atualizar(jogador, janela)

        if self.morto:

            if Esqueleto.esqueleto_atirador is self:
                Esqueleto.esqueleto_atirador = None

            return

        for projetil in self.projeteis:
            projetil.atualizar(janela)

        self.projeteis = [
            projetil
            for projetil in self.projeteis
            if projetil.ativo
        ]

        Esqueleto.escolher_atirador()

        if Esqueleto.esqueleto_atirador is self:

            if self.disparou_turno and not self.projeteis:

                self.disparou_turno = False
                Esqueleto.esqueleto_atirador = None

            elif not self.disparou_turno:

                self.disparar(jogador)

    def desenhar(self):

        super().desenhar()

        for projetil in self.projeteis:
            projetil.desenhar()


class InimigoFuturo:

    def __init__(
        self,
        pasta_assets,
        x,
        altura_chao,
        arquivo_esquerda,
        arquivo_direita,
        velocidade
    ):

        self.sprite_esquerda = GameImage(
            str(pasta_assets / arquivo_esquerda)
        )

        self.sprite_direita = GameImage(
            str(pasta_assets / arquivo_direita)
        )

        self.sprite = self.sprite_esquerda

        self.x = x
        self.y = altura_chao - self.sprite.height

        self.velocidade = velocidade
        self.morto = False

        self.sprite.x = self.x
        self.sprite.y = self.y

    def atualizar(self, jogador, janela):

        if self.morto:
            return

        dt = janela.delta_time()

        centro_jogador = (
            jogador.x + jogador.parado_direita.width / 2
        )

        centro_inimigo = (
            self.x + self.sprite.width / 2
        )

        if centro_inimigo < centro_jogador:

            self.x += self.velocidade * dt
            self.sprite = self.sprite_direita

        elif centro_inimigo > centro_jogador:

            self.x -= self.velocidade * dt
            self.sprite = self.sprite_esquerda

        self.x = max(
            0,
            min(
                self.x,
                janela.width - self.sprite.width
            )
        )

        self.sprite.x = self.x
        self.sprite.y = self.y

    def desenhar(self):

        if not self.morto:
            self.sprite.draw()

    def colidiu_com(self, jogador):

        return verificar_colisao(jogador, self)

    def morrer(self):

        self.morto = True


class Projetil:

    def __init__(
        self,
        pasta_assets,
        x,
        y,
        direcao,
        velocidade=350,
        arquivo="tiro.png"
    ):

        self.sprite = GameImage(
            str(pasta_assets / arquivo)
        )

        self.x = x
        self.y = y

        self.velocidade = velocidade
        self.ativo = True
        self.direcao_x = direcao

        self.sprite.x = self.x
        self.sprite.y = self.y

    def atualizar(self, janela):

        if not self.ativo:
            return

        dt = janela.delta_time()

        self.x += self.direcao_x * self.velocidade * dt

        self.sprite.x = self.x
        self.sprite.y = self.y

        if (
            self.x + self.sprite.width <= 0
            or self.x >= janela.width
            or self.y + self.sprite.height <= 0
            or self.y >= janela.height
        ):

            self.ativo = False

    def colidiu_com(self, jogador):

        if not self.ativo:
            return False

        sprite_jogador = jogador._sprite_atual()

        hitbox_jogador = pygame.Rect(
            int(jogador.x),
            int(jogador.y),
            sprite_jogador.width,
            sprite_jogador.height
        )

        hitbox_projetil = pygame.Rect(
            int(self.x),
            int(self.y),
            self.sprite.width,
            self.sprite.height
        )

        if hitbox_jogador.colliderect(hitbox_projetil):

            self.ativo = False
            return True

        return False

    def desenhar(self):

        if self.ativo:
            self.sprite.draw()


class Robo(InimigoFuturo):

    robos_ativos = []
    robo_atirador = None

    def __init__(self, pasta_assets, x, altura_chao):

        super().__init__(
            pasta_assets,
            x,
            altura_chao,
            "robo_e.png",
            "robo_d.png",
            velocidade=120
        )

        self.projeteis = []
        self.intervalo_disparo = 2
        self.ultimo_disparo = time.time()
        self.pasta_assets = pasta_assets
        self.disparou_turno = False

        Robo.robos_ativos.append(self)

    @classmethod
    def escolher_atirador(cls):

        cls.robos_ativos = [
            robo for robo in cls.robos_ativos
            if not robo.morto
        ]

        if cls.robo_atirador is not None:
            if cls.robo_atirador.morto:
                cls.robo_atirador = None

        if cls.robo_atirador is None and cls.robos_ativos:
            cls.robo_atirador = random.choice(cls.robos_ativos)

    def disparar(self, jogador):

        agora = time.time()

        if agora - self.ultimo_disparo < self.intervalo_disparo:
            return

        centro_jogador = (
            jogador.x + jogador.parado_direita.width / 2
        )

        centro_robo = (
            self.x + self.sprite.width / 2
        )

        if centro_jogador >= centro_robo:

            direcao = 1
            x = self.x + self.sprite.width

        else:

            direcao = -1

            tiro_temporario = GameImage(
                str(self.pasta_assets / "tiro.png")
            )

            x = self.x - tiro_temporario.width

        projetil = Projetil(
            self.pasta_assets,
            x,
            0,
            direcao
        )

        projetil.y = (
            self.y
            + (self.sprite.height / 2)
            - (projetil.sprite.height / 2)
        )

        projetil.sprite.x = projetil.x
        projetil.sprite.y = projetil.y

        self.projeteis.append(projetil)

        self.ultimo_disparo = agora
        self.disparou_turno = True

    def atualizar(self, jogador, janela):

        super().atualizar(jogador, janela)

        if self.morto:

            if Robo.robo_atirador is self:
                Robo.robo_atirador = None

            return

        for projetil in self.projeteis:
            projetil.atualizar(janela)

        self.projeteis = [
            projetil
            for projetil in self.projeteis
            if projetil.ativo
        ]

        Robo.escolher_atirador()

        if Robo.robo_atirador is self:

            if self.disparou_turno and not self.projeteis:

                self.disparou_turno = False
                Robo.robo_atirador = None

            elif not self.disparou_turno:

                self.disparar(jogador)

    def desenhar(self):

        super().desenhar()

        for projetil in self.projeteis:
            projetil.desenhar()


class Homem(InimigoFuturo):

    def __init__(self, pasta_assets, x, altura_chao):

        super().__init__(
            pasta_assets,
            x,
            altura_chao,
            "homem_e.png",
            "homem_d.png",
            velocidade=100
        )
