from pathlib import Path
import pygame
import random

from PPlay.window import Window

from jogador import Jogador
from inimigo import (
    Inimigo, Inseto, Cavaleiro, Esqueleto,
    Robo, Homem
)
from sistema_vida import SistemaVida
from dificuldade import configurar_dificuldade
from menu import Menu
from sons import Sons


PASTA_PROJETO = Path(__file__).resolve().parent
PASTA_ASSETS = PASTA_PROJETO / "assets"

LARGURA = 960
ALTURA = 540
ALTURA_CHAO = 445

janela = Window(LARGURA, ALTURA, "Jornada Temporal")
teclado = janela.keyboard

sons = Sons(PASTA_ASSETS)

pygame.mouse.set_visible(True)

imagem_coracao_item = pygame.image.load(
    str(PASTA_ASSETS / "coração(cheio).png")
).convert_alpha()

imagem_coracao_item = pygame.transform.scale(
    imagem_coracao_item,
    (32, 32)
)


class ItemCoracao:

    def __init__(self, x, y):

        self.imagem = imagem_coracao_item

        self.retangulo = self.imagem.get_rect(
            topleft=(int(x), int(y))
        )

    def desenhar(self):

        janela.get_screen().blit(
            self.imagem,
            self.retangulo
        )


itens = []
item_drop_na_fase = False

CHANCES_DROP = {
    "facil": 0.15,
    "medio": 0.10,
    "dificil": 0.05
}


def obter_posicao_mouse():

    x, y = pygame.mouse.get_pos()

    largura_tela, altura_tela = pygame.display.get_window_size()

    if largura_tela > 0 and altura_tela > 0:

        x = int(x * LARGURA / largura_tela)
        y = int(y * ALTURA / altura_tela)

    return x, y


mouse_anterior = False

menu = Menu(PASTA_ASSETS, LARGURA, ALTURA)

botao_facil = pygame.image.load(
    str(PASTA_ASSETS / "facil.png")
).convert_alpha()

botao_medio = pygame.image.load(
    str(PASTA_ASSETS / "medio.png")
).convert_alpha()

botao_dificil = pygame.image.load(
    str(PASTA_ASSETS / "dificil.png")
).convert_alpha()

tamanho_botoes = (220, 65)

botao_facil = pygame.transform.scale(
    botao_facil, tamanho_botoes
)

botao_medio = pygame.transform.scale(
    botao_medio, tamanho_botoes
)

botao_dificil = pygame.transform.scale(
    botao_dificil, tamanho_botoes
)

x_botoes = (LARGURA - tamanho_botoes[0]) // 2

retangulo_facil = pygame.Rect(
    x_botoes, 180, tamanho_botoes[0], tamanho_botoes[1]
)

retangulo_medio = pygame.Rect(
    x_botoes, 260, tamanho_botoes[0], tamanho_botoes[1]
)

retangulo_dificil = pygame.Rect(
    x_botoes, 340, tamanho_botoes[0], tamanho_botoes[1]
)

vida = SistemaVida()

jogador = Jogador(str(PASTA_ASSETS), 0, 0)


def posicionar_jogador_centro():

    x = (LARGURA - jogador.parado_direita.width) // 2

    jogador.teleportar(x, ALTURA_CHAO)


posicionar_jogador_centro()

fase_atual = 1
rodada = 1

estado = "menu_principal"

dificuldade_atual = "facil"


def verificar_aumento_vida():

    if dificuldade_atual == "facil":

        vida.aumentar_vida_maxima()

    elif dificuldade_atual == "medio" and fase_atual == 2:

        vida.aumentar_vida_maxima()


FASES_BASE = {

    1: {
        "nome": "PRÉ-HISTÓRIA",
        "background": "floresta.png",
        "rodadas": {
            1: {"dinossauros": 2, "insetos": 1},
            2: {"dinossauros": 3, "insetos": 2},
            3: {"dinossauros": 5, "insetos": 3}
        }
    },

    2: {
        "nome": "ERA MEDIEVAL",
        "background": "medieval.jpg",
        "rodadas": {
            1: {"cavaleiros": 2, "esqueletos": 1},
            2: {"cavaleiros": 2, "esqueletos": 2},
            3: {"cavaleiros": 3, "esqueletos": 2},
            4: {"cavaleiros": 4, "esqueletos": 3}
        }
    },

    3: {
        "nome": "FUTURO",
        "background": "futuro.jpg",
        "rodadas": {
            1: {"robos": 2, "homens": 1},
            2: {"robos": 2, "homens": 2},
            3: {"robos": 3, "homens": 2},
            4: {"robos": 3, "homens": 3},
            5: {"robos": 4, "homens": 3}
        }
    }

}

FASES = configurar_dificuldade(
    FASES_BASE,
    dificuldade_atual
)


def carregar_background():

    arquivo = FASES[fase_atual]["background"]

    imagem = pygame.image.load(
        str(PASTA_ASSETS / arquivo)
    ).convert()

    largura_original = imagem.get_width()
    altura_original = imagem.get_height()

    escala_x = LARGURA / largura_original
    escala_y = ALTURA / altura_original

    escala = min(escala_x, escala_y)

    nova_largura = int(largura_original * escala)
    nova_altura = int(altura_original * escala)

    imagem = pygame.transform.smoothscale(
        imagem,
        (nova_largura, nova_altura)
    )

    return imagem


def desenhar_background():

    tela = janela.get_screen()

    tela.fill((0, 0, 0))

    x = (LARGURA - fundo.get_width()) // 2
    y = (ALTURA - fundo.get_height()) // 2

    tela.blit(fundo, (x, y))


fundo = carregar_background()




def criar_inimigos(numero_fase, numero_rodada):

    inimigos = []

    configuracao = FASES[numero_fase]["rodadas"][numero_rodada]

    quantidade_esquerda = 0
    quantidade_direita = 0

    def adicionar_inimigo(inimigo):

        nonlocal quantidade_esquerda
        nonlocal quantidade_direita

        largura_inimigo = inimigo.sprite.width

        if quantidade_esquerda <= quantidade_direita:

            x = 20 + quantidade_esquerda * (largura_inimigo + 15)
            quantidade_esquerda += 1

        else:

            x = LARGURA - largura_inimigo - 20 - quantidade_direita * (largura_inimigo + 15)
            quantidade_direita += 1

        inimigo.x = x
        inimigo.sprite.x = x

        inimigos.append(inimigo)

    if numero_fase == 1:

        for i in range(configuracao["dinossauros"]):

            inimigo = Inimigo(
                PASTA_ASSETS,
                0,
                ALTURA_CHAO
            )

            adicionar_inimigo(inimigo)

        for i in range(configuracao["insetos"]):

            inimigo = Inseto(
                PASTA_ASSETS,
                0,
                300
            )

            adicionar_inimigo(inimigo)

    elif numero_fase == 2:

        for i in range(configuracao["cavaleiros"]):

            inimigo = Cavaleiro(
                PASTA_ASSETS,
                0,
                ALTURA_CHAO
            )

            adicionar_inimigo(inimigo)

        for i in range(configuracao["esqueletos"]):

            inimigo = Esqueleto(
                PASTA_ASSETS,
                0,
                ALTURA_CHAO
            )

            adicionar_inimigo(inimigo)

    elif numero_fase == 3:

        for i in range(configuracao["robos"]):

            inimigo = Robo(
                PASTA_ASSETS,
                0,
                ALTURA_CHAO
            )

            adicionar_inimigo(inimigo)

        for i in range(configuracao["homens"]):

            inimigo = Homem(
                PASTA_ASSETS,
                0,
                ALTURA_CHAO
            )

            adicionar_inimigo(inimigo)

    return inimigos


def tentar_dropar_coracao(inimigo, ultimo_inimigo_ultima_rodada=False):

    global item_drop_na_fase

    chance = CHANCES_DROP[dificuldade_atual]

    deve_dropar = random.random() < chance

    if (
        dificuldade_atual in ["facil", "medio"]
        and not item_drop_na_fase
        and ultimo_inimigo_ultima_rodada
    ):

        deve_dropar = True

    if deve_dropar:

        x = (
            inimigo.x
            + inimigo.sprite.width / 2
            - 16
        )

        y = ALTURA_CHAO - 32

        item = ItemCoracao(x, y)

        itens.append(item)

        item_drop_na_fase = True


def atualizar_itens():

    global itens

    largura_jogador = jogador.parado_direita.width
    altura_jogador = jogador.parado_direita.height

    hitbox_jogador = pygame.Rect(
        int(jogador.x),
        int(jogador.y),
        largura_jogador,
        altura_jogador
    )

    for item in itens[:]:

        item.desenhar()

        if hitbox_jogador.colliderect(item.retangulo):

            vida.recuperar_vida()

            itens.remove(item)


inimigos = criar_inimigos(fase_atual, rodada)


def iniciar_jogo(dificuldade):

    global FASES, fase_atual, rodada
    global vida, fundo, inimigos, jogador
    global estado, dificuldade_atual
    global itens, item_drop_na_fase

    dificuldade_atual = dificuldade

    FASES = configurar_dificuldade(
        FASES_BASE,
        dificuldade_atual
    )

    vida = SistemaVida()

    jogador = Jogador(str(PASTA_ASSETS), 0, 0)

    posicionar_jogador_centro()

    fase_atual = 1
    rodada = 1

    itens = []
    item_drop_na_fase = False

    fundo = carregar_background()

    inimigos = criar_inimigos(fase_atual, rodada)

    estado = "inicio_fase"


def reiniciar_jogo():

    global estado

    estado = "menu_principal"


def desenhar_texto(texto, tamanho, cor, y):

    fonte = pygame.font.SysFont("Arial", tamanho, bold=True)

    imagem_texto = fonte.render(texto, True, cor)

    x = (janela.width - imagem_texto.get_width()) // 2

    janela.get_screen().blit(imagem_texto, (x, y))


def desenhar_menu_dificuldade():

    tela = janela.get_screen()

    escurecimento = pygame.Surface((LARGURA, ALTURA))
    escurecimento.set_alpha(180)
    escurecimento.fill((0, 0, 0))

    tela.blit(escurecimento, (0, 0))

    desenhar_texto(
        "ESCOLHA A DIFICULDADE",
        42,
        (255, 255, 255),
        100
    )

    tela.blit(botao_facil, retangulo_facil.topleft)
    tela.blit(botao_medio, retangulo_medio.topleft)
    tela.blit(botao_dificil, retangulo_dificil.topleft)

    desenhar_texto(
        "CLIQUE EM UMA DAS OPCOES",
        20,
        (255, 255, 255),
        440
    )


def desenhar_inicio_fase():

    quantidade_rodadas = len(
        FASES[fase_atual]["rodadas"]
    )

    tela = janela.get_screen()

    escurecimento = pygame.Surface((LARGURA, ALTURA))
    escurecimento.set_alpha(150)
    escurecimento.fill((0, 0, 0))

    tela.blit(escurecimento, (0, 0))

    desenhar_texto(
        FASES[fase_atual]["nome"],
        48,
        (255, 255, 255),
        175
    )

    desenhar_texto(
        f"{quantidade_rodadas} RODADAS",
        30,
        (255, 255, 255),
        245
    )

    desenhar_texto(
        "APERTE ESPACO PARA COMEÇAR",
        25,
        (255, 220, 80),
        330
    )



def desenhar_menu_pausa():

    tela = janela.get_screen()

    for inimigo in inimigos:
        inimigo.desenhar()

    for item in itens:
        item.desenhar()

    jogador.desenhar()

    vida.desenhar(tela)

    desenhar_texto(
        FASES[fase_atual]["nome"],
        25,
        (255, 255, 255),
        10
    )

    desenhar_texto(
        f"RODADA {rodada}/{len(FASES[fase_atual]['rodadas'])}",
        22,
        (255, 255, 255),
        42
    )

    escurecimento = pygame.Surface((LARGURA, ALTURA))
    escurecimento.set_alpha(180)
    escurecimento.fill((0, 0, 0))

    tela.blit(escurecimento, (0, 0))

    desenhar_texto(
        "JOGO PAUSADO",
        45,
        (255, 255, 255),
        150
    )

    menu.desenhar_pausa(tela)

    sons.atualizar_controles()
    sons.desenhar_controles(tela)



while True:

    estado_anterior = estado

    mouse_pressionado = pygame.mouse.get_pressed()[0]

    clicou_mouse = (
        mouse_pressionado
        and not mouse_anterior
    )

    mouse_anterior = mouse_pressionado

    desenhar_background()

    if teclado.key_down("ESC"):

        if estado == "jogando":

            estado = "pausado"

        elif estado != "pausado":

            break

    if estado == "menu_principal":

        menu.desenhar(janela.get_screen())

        opcao = menu.atualizar()

        if opcao == "play":

            estado = "menu_dificuldade"

        elif opcao == "exit":

            break

    elif estado == "menu_dificuldade":

        desenhar_menu_dificuldade()

        if estado_anterior == "menu_dificuldade" and clicou_mouse:

            posicao_mouse = obter_posicao_mouse()

            if retangulo_facil.collidepoint(posicao_mouse):

                iniciar_jogo("facil")

            elif retangulo_medio.collidepoint(posicao_mouse):

                iniciar_jogo("medio")

            elif retangulo_dificil.collidepoint(posicao_mouse):

                iniciar_jogo("dificil")

    elif estado == "pausado":

        desenhar_menu_pausa()

        opcao = menu.atualizar_pausa()

        if opcao == "start":

            estado = "jogando"

        elif opcao == "exit":

            estado = "menu_principal"

    elif estado == "inicio_fase":

        desenhar_inicio_fase()

        vida.desenhar(janela.get_screen())

        if teclado.key_down("SPACE"):

            estado = "jogando"

    elif estado == "jogando":

        altura_jogador = jogador.parado_direita.height
        pe_anterior = jogador.y + altura_jogador

        jogador.atualizar(teclado, janela, ALTURA_CHAO)

        pe_atual = jogador.y + altura_jogador

        for inimigo in inimigos:

            inimigo.atualizar(jogador, janela)

            if isinstance(inimigo, (Robo, Esqueleto)):

                for projetil in inimigo.projeteis:

                    if projetil.colidiu_com(jogador):

                        if vida.receber_dano():

                            sons.tocar_dano()

            if inimigo.colidiu_com(jogador):

                acertou_cabeca = (
                    jogador.velocidade_y > 0
                    and pe_anterior <= inimigo.y + 12
                    and pe_atual >= inimigo.y
                )

                if acertou_cabeca:

                    ultimo_inimigo_ultima_rodada = (
                        rodada == len(FASES[fase_atual]["rodadas"])
                        and sum(
                            1 for outro in inimigos
                            if not outro.morto
                        ) == 1
                    )

                    inimigo.morrer()

                    sons.tocar_impacto()

                    tentar_dropar_coracao(
                        inimigo,
                        ultimo_inimigo_ultima_rodada
                    )

                    jogador.velocidade_y = -400
                    jogador.no_chao = False

                    break

                else:

                    if vida.receber_dano():

                        sons.tocar_dano()

        inimigos = [
            inimigo for inimigo in inimigos
            if not inimigo.morto
        ]

        atualizar_itens()

        if len(inimigos) == 0 and len(itens) == 0:

            quantidade_rodadas = len(
                FASES[fase_atual]["rodadas"]
            )

            if rodada < quantidade_rodadas:

                rodada += 1

                inimigos = criar_inimigos(
                    fase_atual,
                    rodada
                )

                posicionar_jogador_centro()

            else:

                if fase_atual < len(FASES):

                    fase_atual += 1
                    rodada = 1

                    verificar_aumento_vida()

                    while vida.vida < vida.vida_maxima:
                        vida.recuperar_vida()

                    item_drop_na_fase = False

                    fundo = carregar_background()

                    inimigos = criar_inimigos(
                        fase_atual,
                        rodada
                    )

                    posicionar_jogador_centro()

                    estado = "inicio_fase"

                else:

                    estado = "vitoria"

        if vida.morreu():

            estado = "derrota"

        for inimigo in inimigos:
            inimigo.desenhar()

        for item in itens:
            item.desenhar()

        jogador.desenhar()

        vida.desenhar(janela.get_screen())

        desenhar_texto(
            FASES[fase_atual]["nome"],
            25,
            (255, 255, 255),
            10
        )

        desenhar_texto(
            f"RODADA {rodada}/{len(FASES[fase_atual]['rodadas'])}",
            22,
            (255, 255, 255),
            42
        )

    elif estado == "derrota" or estado == "vitoria":

        tela = janela.get_screen()

        escurecimento = pygame.Surface((LARGURA, ALTURA))
        escurecimento.set_alpha(180)
        escurecimento.fill((0, 0, 0))

        tela.blit(escurecimento, (0, 0))

        if estado == "derrota":

            desenhar_texto(
                "FIM DE JOGO",
                55,
                (255, 50, 50),
                200
            )

        elif estado == "vitoria":

            desenhar_texto(
                "JOGO CONCLUIDO!",
                50,
                (50, 255, 100),
                200
            )

        desenhar_texto(
            "Pressione ESPACO para continuar",
            25,
            (255, 255, 255),
            290
        )

        if teclado.key_down("SPACE"):

            reiniciar_jogo()

    janela.update()
