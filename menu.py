import pygame
from pathlib import Path


class Menu:

    def __init__(self, pasta_assets, largura, altura):

        self.largura = largura
        self.altura = altura
        self.pasta_assets = Path(pasta_assets)

        self.background = pygame.image.load(
            str(self.pasta_assets / "tela_inicial.png")
        ).convert()

        self.background = pygame.transform.scale(
            self.background,
            (self.largura, self.altura)
        )

        self.botao_play = pygame.image.load(
            str(self.pasta_assets / "play.jpg")
        ).convert()

        self.botao_exit = pygame.image.load(
            str(self.pasta_assets / "exit.jpg")
        ).convert()

        self.botao_start = pygame.image.load(
            str(self.pasta_assets / "start.jpg")
        ).convert()

        self.botao_exit_pausa = pygame.image.load(
            str(self.pasta_assets / "exit.jpg")
        ).convert()

        self.tamanho_botoes = (220, 65)

        self.botao_play = pygame.transform.scale(
            self.botao_play, self.tamanho_botoes
        )

        self.botao_exit = pygame.transform.scale(
            self.botao_exit, self.tamanho_botoes
        )

        self.botao_start = pygame.transform.scale(
            self.botao_start, self.tamanho_botoes
        )

        self.botao_exit_pausa = pygame.transform.scale(
            self.botao_exit_pausa, self.tamanho_botoes
        )

        x = (self.largura - self.tamanho_botoes[0]) // 2

        self.retangulo_play = pygame.Rect(
            x, 220,
            self.tamanho_botoes[0],
            self.tamanho_botoes[1]
        )

        self.retangulo_exit = pygame.Rect(
            x, 310,
            self.tamanho_botoes[0],
            self.tamanho_botoes[1]
        )

        self.retangulo_start = pygame.Rect(
            x, 250,
            self.tamanho_botoes[0],
            self.tamanho_botoes[1]
        )

        self.retangulo_exit_pausa = pygame.Rect(
            x, 340,
            self.tamanho_botoes[0],
            self.tamanho_botoes[1]
        )

        self.mouse_menu_anterior = False
        self.mouse_pausa_anterior = False

    def obter_posicao_mouse(self):

        mouse_x, mouse_y = pygame.mouse.get_pos()

        largura_tela, altura_tela = pygame.display.get_window_size()

        if largura_tela > 0 and altura_tela > 0:
            mouse_x = int(mouse_x * self.largura / largura_tela)
            mouse_y = int(mouse_y * self.altura / altura_tela)

        return mouse_x, mouse_y

    def desenhar(self, superficie):

        superficie.blit(
            self.background,
            (0, 0)
        )

        superficie.blit(
            self.botao_play,
            self.retangulo_play.topleft
        )

        superficie.blit(
            self.botao_exit,
            self.retangulo_exit.topleft
        )

    def atualizar(self):

        mouse_pressionado = pygame.mouse.get_pressed()[0]

        clicou = (
            mouse_pressionado
            and not self.mouse_menu_anterior
        )

        self.mouse_menu_anterior = mouse_pressionado

        if clicou:

            posicao_mouse = self.obter_posicao_mouse()

            if self.retangulo_play.collidepoint(posicao_mouse):
                return "play"

            elif self.retangulo_exit.collidepoint(posicao_mouse):
                return "exit"

        return None

    def desenhar_pausa(self, superficie):

        superficie.blit(
            self.botao_start,
            self.retangulo_start.topleft
        )

        superficie.blit(
            self.botao_exit_pausa,
            self.retangulo_exit_pausa.topleft
        )

    def atualizar_pausa(self):

        mouse_pressionado = pygame.mouse.get_pressed()[0]

        clicou = (
            mouse_pressionado
            and not self.mouse_pausa_anterior
        )

        self.mouse_pausa_anterior = mouse_pressionado

        if clicou:

            posicao_mouse = self.obter_posicao_mouse()

            if self.retangulo_start.collidepoint(posicao_mouse):
                return "start"

            elif self.retangulo_exit_pausa.collidepoint(posicao_mouse):
                return "exit"

        return None