
import pygame
from pathlib import Path


class Sons:

    def __init__(self, pasta_assets):

        pasta_sons = Path(pasta_assets) / "sons"

        pygame.mixer.init()

        self.dano = pygame.mixer.Sound(
            str(pasta_sons / "dano.wav")
        )

        self.impacto = pygame.mixer.Sound(
            str(pasta_sons / "impacto.wav")
        )

        self.volume_efeitos = 0.7
        self.volume_musica = 0.3

        self.volume_musica_anterior = self.volume_musica
        self.volume_efeitos_anterior = self.volume_efeitos

        self.dano.set_volume(self.volume_efeitos)
        self.impacto.set_volume(self.volume_efeitos)

        pygame.mixer.music.load(
            str(pasta_sons / "musica_fundo.mp3")
        )

        pygame.mixer.music.set_volume(self.volume_musica)
        pygame.mixer.music.play(-1)

        self.volume_img = pygame.image.load(
            str(pasta_sons / "volume.png")
        ).convert_alpha()

        self.volume_img = pygame.transform.scale(
            self.volume_img,
            (45, 45)
        )

        self.x_barra = 660
        self.largura_barra = 250

        self.y_musica = 285
        self.y_efeitos = 365

        self.arrastando = None

        self.mouse_anterior = False

        self.fonte = pygame.font.SysFont("Arial", 20)

    def tocar_dano(self):

        self.dano.play()

    def tocar_impacto(self):

        self.impacto.play()

    def definir_volume_musica(self, volume):

        self.volume_musica = max(0, min(1, volume))

        if self.volume_musica > 0:

            self.volume_musica_anterior = self.volume_musica

        pygame.mixer.music.set_volume(
            self.volume_musica
        )

    def definir_volume_efeitos(self, volume):

        self.volume_efeitos = max(0, min(1, volume))

        if self.volume_efeitos > 0:

            self.volume_efeitos_anterior = self.volume_efeitos

        self.dano.set_volume(self.volume_efeitos)
        self.impacto.set_volume(self.volume_efeitos)

    def alternar_mudo_musica(self):

        if self.volume_musica > 0:

            self.volume_musica_anterior = self.volume_musica
            self.definir_volume_musica(0)

        else:

            self.definir_volume_musica(
                self.volume_musica_anterior
            )

    def alternar_mudo_efeitos(self):

        if self.volume_efeitos > 0:

            self.volume_efeitos_anterior = self.volume_efeitos
            self.definir_volume_efeitos(0)

        else:

            self.definir_volume_efeitos(
                self.volume_efeitos_anterior
            )

    def obter_posicao_mouse(self):

        x, y = pygame.mouse.get_pos()

        largura_tela, altura_tela = pygame.display.get_window_size()

        if largura_tela > 0 and altura_tela > 0:

            x = int(x * 960 / largura_tela)
            y = int(y * 540 / altura_tela)

        return x, y

    def atualizar_controles(self):

        mouse_x, mouse_y = self.obter_posicao_mouse()

        mouse_pressionado = pygame.mouse.get_pressed()[0]

        clicou_mouse = (
            mouse_pressionado
            and not self.mouse_anterior
        )

        if clicou_mouse:

            botao_musica = pygame.Rect(
                self.x_barra - 65,
                self.y_musica - 22,
                45,
                45
            )

            botao_efeitos = pygame.Rect(
                self.x_barra - 65,
                self.y_efeitos - 22,
                45,
                45
            )

            if botao_musica.collidepoint(mouse_x, mouse_y):

                self.alternar_mudo_musica()

                self.arrastando = None

            elif botao_efeitos.collidepoint(mouse_x, mouse_y):

                self.alternar_mudo_efeitos()

                self.arrastando = None

        if mouse_pressionado:

            if self.arrastando is None:

                if (
                    abs(mouse_y - self.y_musica) <= 20
                    and self.x_barra - 10 <= mouse_x <= self.x_barra + self.largura_barra + 10
                ):

                    self.arrastando = "musica"

                elif (
                    abs(mouse_y - self.y_efeitos) <= 20
                    and self.x_barra - 10 <= mouse_x <= self.x_barra + self.largura_barra + 10
                ):

                    self.arrastando = "efeitos"

            if self.arrastando == "musica":

                volume = (mouse_x - self.x_barra) / self.largura_barra

                self.definir_volume_musica(volume)

            elif self.arrastando == "efeitos":

                volume = (mouse_x - self.x_barra) / self.largura_barra

                self.definir_volume_efeitos(volume)

        else:

            self.arrastando = None

        self.mouse_anterior = mouse_pressionado

    def desenhar_barra(self, tela, y, volume):

        posicao = self.x_barra + int(
            volume * self.largura_barra
        )

        pygame.draw.line(
            tela,
            (100, 100, 100),
            (self.x_barra, y),
            (self.x_barra + self.largura_barra, y),
            8
        )

        pygame.draw.line(
            tela,
            (230, 185, 60),
            (self.x_barra, y),
            (posicao, y),
            8
        )

        pygame.draw.circle(
            tela,
            (255, 255, 255),
            (posicao, y),
            11
        )

        pygame.draw.circle(
            tela,
            (30, 30, 30),
            (posicao, y),
            11,
            2
        )

    def desenhar_controles(self, tela):

        texto_musica = self.fonte.render(
            "Musica de fundo",
            True,
            (255, 255, 255)
        )

        texto_efeitos = self.fonte.render(
            "Sons de efeito",
            True,
            (255, 255, 255)
        )

        tela.blit(
            texto_musica,
            (self.x_barra, self.y_musica - 35)
        )

        tela.blit(
            texto_efeitos,
            (self.x_barra, self.y_efeitos - 35)
        )

        tela.blit(
            self.volume_img,
            (self.x_barra - 65, self.y_musica - 22)
        )

        tela.blit(
            self.volume_img,
            (self.x_barra - 65, self.y_efeitos - 22)
        )

        self.desenhar_barra(
            tela,
            self.y_musica,
            self.volume_musica
        )

        self.desenhar_barra(
            tela,
            self.y_efeitos,
            self.volume_efeitos
        )

        porcentagem_musica = self.fonte.render(
            f"{int(self.volume_musica * 100)}%",
            True,
            (255, 255, 255)
        )

        porcentagem_efeitos = self.fonte.render(
            f"{int(self.volume_efeitos * 100)}%",
            True,
            (255, 255, 255)
        )

        tela.blit(
            porcentagem_musica,
            (self.x_barra + self.largura_barra + 15, self.y_musica - 12)
        )

        tela.blit(
            porcentagem_efeitos,
            (self.x_barra + self.largura_barra + 15, self.y_efeitos - 12)
        )
