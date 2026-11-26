import copy


def configurar_dificuldade(fases, dificuldade):

    rodadas_extras = {
        "facil": 0,
        "medio": 1,
        "dificil": 2
    }

    quantidade_extra = rodadas_extras[dificuldade]

    fases_configuradas = copy.deepcopy(fases)

    for fase in fases_configuradas.values():

        rodadas = fase["rodadas"]

        ultima_rodada = max(rodadas)
        configuracao_extra = rodadas[ultima_rodada]

        for i in range(quantidade_extra):

            nova_rodada = max(rodadas) + 1

            rodadas[nova_rodada] = copy.deepcopy(
                configuracao_extra
            )

    return fases_configuradas