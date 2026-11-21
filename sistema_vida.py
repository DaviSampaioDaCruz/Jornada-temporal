import time
import pygame
from pathlib import Path


class SistemaVida:

    def __init__(self):

        self.vida_maxima = 3
        self.vida = 3

        self.tempo_invulneravel = 2
        self.ultimo_dano = 0

        pasta_projeto = Path(__file__).resolve().parent
        pasta_assets = pasta_projeto / "assets"

        caminho_cheio = pasta_assets / "coração(cheio).png"
        caminho_vazio = pasta_assets / "coração(vazio).png"

        self.coracao_cheio = pygame.image.load(
            str(caminho_cheio)
        ).convert_alpha()

        self.coracao_vazio = pygame.image.load(
            str(caminho_vazio)
        ).convert_alpha()

        tamanho = (36, 36)

        self.coracao_cheio = pygame.transform.scale(
            self.coracao_cheio, tamanho
        )

        self.coracao_vazio = pygame.transform.scale(
            self.coracao_vazio, tamanho
        )

    def receber_dano(self):

        agora = time.time()

        if self.vida > 0 and self.esta_vulneravel():

            self.vida -= 1
            self.ultimo_dano = agora

            return True

        return False

    def recuperar_vida(self):

        if self.vida < self.vida_maxima:

            self.vida += 1

            return True

        return False

    def aumentar_vida_maxima(self):

        self.vida_maxima += 1

        self.vida += 1

        self.vida = min(self.vida, self.vida_maxima)

    def esta_vulneravel(self):

        agora = time.time()

        return agora - self.ultimo_dano >= self.tempo_invulneravel

    def desenhar(self, superficie):

        for i in range(self.vida_maxima):

            x = 20 + i * 45
            y = 20

            if i < self.vida:
                imagem = self.coracao_cheio
            else:
                imagem = self.coracao_vazio

            superficie.blit(imagem, (x, y))

    def morreu(self):

        return self.vida <= 0