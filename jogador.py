from PPlay.sprite import Sprite


class Jogador:

    def __init__(self, pasta_assets, x, y):

        self.parado_direita = Sprite(f"{pasta_assets}/jogador_parado_direita.png")
        self.parado_esquerda = Sprite(f"{pasta_assets}/jogador_parado_esquerda.png")

        self.andando_direita = Sprite(f"{pasta_assets}/jogador_andando_direita.png", 8)
        self.andando_direita.set_sequence_time(0, 7, 650, True)

        self.andando_esquerda = Sprite(f"{pasta_assets}/jogador_andando_esquerda.png", 8)
        self.andando_esquerda.set_sequence_time(0, 7, 650, True)

        self.pulando = Sprite(f"{pasta_assets}/jogador_pulando.png")
        self.caindo = Sprite(f"{pasta_assets}/jogador_caindo.png")

        self.velocidade = 280
        self.forca_pulo = -650
        self.gravidade = 1500
        self.velocidade_y = 0
        self.no_chao = False
        self.direcao = "direita"
        self.estado = "parado"

        self.x = x
        self.y = y
        self.altura_chao = 0

        self._posicionar_sprites()

    def _sprite_atual(self):

        if not self.no_chao:

            if self.velocidade_y < 0:
                return self.pulando

            else:
                return self.caindo

        if self.estado == "andando":

            if self.direcao == "direita":
                return self.andando_direita

            return self.andando_esquerda

        if self.direcao == "direita":
            return self.parado_direita

        return self.parado_esquerda

    def _posicionar_sprites(self):

        for sprite in (
            self.parado_direita,
            self.parado_esquerda,
            self.andando_direita,
            self.andando_esquerda,
            self.pulando,
            self.caindo
        ):

            sprite.x = self.x
            sprite.y = self.y

    def atualizar(self, teclado, janela, altura_chao):

        dt = janela.delta_time()

        self.altura_chao = altura_chao
        movimento = False

        if teclado.key_pressed("A") or teclado.key_pressed("LEFT"):

            self.x -= self.velocidade * dt
            self.direcao = "esquerda"
            movimento = True

        elif teclado.key_pressed("D") or teclado.key_pressed("RIGHT"):

            self.x += self.velocidade * dt
            self.direcao = "direita"
            movimento = True

        largura = self.parado_direita.width

        self.x = max(
            0,
            min(self.x, janela.width - largura)
        )

        if (
            teclado.key_down("SPACE")
            or teclado.key_down("W")
            or teclado.key_down("UP")
        ) and self.no_chao:

            self.velocidade_y = self.forca_pulo
            self.no_chao = False

        self.velocidade_y += self.gravidade * dt
        self.y += self.velocidade_y * dt

        limite_y = altura_chao - self.parado_direita.height

        if self.y >= limite_y:

            self.y = limite_y
            self.velocidade_y = 0
            self.no_chao = True

        if self.no_chao and movimento:

            self.estado = "andando"

        else:

            self.estado = "parado"

        self._posicionar_sprites()

    def desenhar(self):

        sprite = self._sprite_atual()

        if self.estado == "andando" and self.no_chao:

            sprite.update()

        sprite.draw()

    def teleportar(self, x, altura_chao):

        self.x = x
        self.y = altura_chao - self.parado_direita.height

        self.velocidade_y = 0
        self.no_chao = True
        self.estado = "parado"

        self._posicionar_sprites()