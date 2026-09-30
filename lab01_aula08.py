"""
LAB 01 - PSO para Balanceamento Dinâmico de Carga em Datacenters

Otimização:
    Minimizar a temperatura média ponderada dos racks.

Variáveis:
    W = [w1, w2, w3, w4, w5, w6]

Restrição:
    sum(W) = 1.0

Coeficientes de aquecimento:
    C = [42, 35, 58, 30, 50, 65]

Populações testadas:
    10, 30 e 50 partículas.

Implementação do PSO feita do zero.
"""

import os
import csv
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURAÇÕES
# ============================================================

SEED = 42

NUM_DIMENSOES = 6

COEF_AQUECIMENTO = np.array(
    [42.0, 35.0, 58.0, 30.0, 50.0, 65.0]
)

LIMITE_CRITICO = 75.0

POPULACOES = [10, 30, 50]

NUM_ITERACOES = 100

W_INERCIA = 0.7
C1 = 1.5
C2 = 1.5

VELOCIDADE_MAX = 0.20

DIRETORIO_RESULTADOS = "resultados"


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def normalizar_posicao(posicao):
    """
    Garante que todas as posições sejam >= 0
    e que a soma seja exatamente 1.0.
    """

    posicao = np.maximum(posicao, 0.0)

    soma = np.sum(posicao)

    if soma <= 1e-12:
        return np.ones(NUM_DIMENSOES) / NUM_DIMENSOES

    posicao = posicao / soma

    # Correção numérica para garantir soma exatamente 1
    posicao[-1] += 1.0 - np.sum(posicao)

    return posicao


def calcular_fitness(peso):
    """
    Função objetivo.

    Temperatura ponderada:
        T = sum(w_i * C_i)

    Penalidade externa:
        Caso alguma temperatura individual ultrapasse
        o limite crítico de 75 graus.

    Como os dados fornecidos possuem máximo 65 graus,
    a penalidade não será ativada neste cenário específico.
    """

    peso = normalizar_posicao(peso)

    temperatura_ponderada = np.sum(
        peso * COEF_AQUECIMENTO
    )

    # Penalidade externa
    excesso = np.maximum(
        COEF_AQUECIMENTO - LIMITE_CRITICO,
        0.0
    )

    penalidade = np.sum(excesso) * 1000.0

    fitness = temperatura_ponderada + penalidade

    return fitness


# ============================================================
# CLASSE PSO
# ============================================================

class PSOContinuo:

    def __init__(
        self,
        tamanho_populacao,
        dimensoes,
        iteracoes,
        seed
    ):

        self.tamanho_populacao = tamanho_populacao
        self.dimensoes = dimensoes
        self.iteracoes = iteracoes

        self.rng = np.random.default_rng(seed)

        # Posições iniciais
        self.posicoes = self.rng.random(
            (tamanho_populacao, dimensoes)
        )

        # Normalização obrigatória
        for i in range(tamanho_populacao):
            self.posicoes[i] = normalizar_posicao(
                self.posicoes[i]
            )

        # Velocidades
        self.velocidades = self.rng.uniform(
            -0.05,
            0.05,
            (tamanho_populacao, dimensoes)
        )

        # Pbest
        self.pbest_posicoes = self.posicoes.copy()

        self.pbest_fitness = np.array([
            calcular_fitness(posicao)
            for posicao in self.posicoes
        ])

        # Gbest
        indice_melhor = np.argmin(
            self.pbest_fitness
        )

        self.gbest_posicao = (
            self.pbest_posicoes[indice_melhor].copy()
        )

        self.gbest_fitness = (
            self.pbest_fitness[indice_melhor]
        )

        # Histórico
        self.historico_gbest = []
        self.historico_pbest = []

    def executar(self):

        for iteracao in range(self.iteracoes):

            for i in range(self.tamanho_populacao):

                r1 = self.rng.random(self.dimensoes)
                r2 = self.rng.random(self.dimensoes)

                # Atualização da velocidade
                self.velocidades[i] = (
                    W_INERCIA * self.velocidades[i]
                    +
                    C1 * r1 *
                    (
                        self.pbest_posicoes[i]
                        - self.posicoes[i]
                    )
                    +
                    C2 * r2 *
                    (
                        self.gbest_posicao
                        - self.posicoes[i]
                    )
                )

                # Limitação da velocidade
                self.velocidades[i] = np.clip(
                    self.velocidades[i],
                    -VELOCIDADE_MAX,
                    VELOCIDADE_MAX
                )

                # Atualização da posição
                self.posicoes[i] += self.velocidades[i]

                # Normalização obrigatória
                self.posicoes[i] = normalizar_posicao(
                    self.posicoes[i]
                )

                # Avaliação
                fitness_atual = calcular_fitness(
                    self.posicoes[i]
                )

                # Atualização do Pbest
                if fitness_atual < self.pbest_fitness[i]:

                    self.pbest_fitness[i] = fitness_atual

                    self.pbest_posicoes[i] = (
                        self.posicoes[i].copy()
                    )

            # Atualização do Gbest
            indice_melhor = np.argmin(
                self.pbest_fitness
            )

            if (
                self.pbest_fitness[indice_melhor]
                < self.gbest_fitness
            ):

                self.gbest_fitness = (
                    self.pbest_fitness[indice_melhor]
                )

                self.gbest_posicao = (
                    self.pbest_posicoes[indice_melhor].copy()
                )

            self.historico_gbest.append(
                self.gbest_fitness
            )

            self.historico_pbest.append(
                np.mean(self.pbest_fitness)
            )

        return (
            self.gbest_posicao,
            self.gbest_fitness,
            self.historico_gbest
        )


# ============================================================
# EXECUÇÃO DOS TESTES
# ============================================================

def executar_experimentos():

    os.makedirs(
        DIRETORIO_RESULTADOS,
        exist_ok=True
    )

    resultados = []

    historicos = {}

    for populacao in POPULACOES:

        print("\n" + "=" * 70)
        print(f"PSO - POPULAÇÃO: {populacao}")
        print("=" * 70)

        pso = PSOContinuo(
            tamanho_populacao=populacao,
            dimensoes=NUM_DIMENSOES,
            iteracoes=NUM_ITERACOES,
            seed=SEED + populacao
        )

        melhor_w, melhor_fitness, historico = (
            pso.executar()
        )

        soma = np.sum(melhor_w)

        temperatura = calcular_fitness(
            melhor_w
        )

        print(
            "Melhor distribuição W:"
        )

        print(
            np.round(melhor_w, 6)
        )

        print(
            f"Soma dos pesos: {soma:.12f}"
        )

        print(
            f"Fitness final: {melhor_fitness:.6f}"
        )

        print(
            f"Temperatura ponderada: {temperatura:.6f} °C"
        )

        historicos[populacao] = historico

        resultados.append({
            "populacao": populacao,
            "w1": melhor_w[0],
            "w2": melhor_w[1],
            "w3": melhor_w[2],
            "w4": melhor_w[3],
            "w5": melhor_w[4],
            "w6": melhor_w[5],
            "soma": soma,
            "fitness": melhor_fitness
        })

    # ========================================================
    # CSV
    # ========================================================

    arquivo_csv = os.path.join(
        DIRETORIO_RESULTADOS,
        "lab01_resultados.csv"
    )

    with open(
        arquivo_csv,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        campos = list(resultados[0].keys())

        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos
        )

        escritor.writeheader()

        escritor.writerows(resultados)

    # ========================================================
    # GRÁFICO
    # ========================================================

    plt.figure(figsize=(10, 6))

    for populacao, historico in historicos.items():

        plt.plot(
            historico,
            label=f"{populacao} partículas"
        )

    plt.xlabel("Iteração")
    plt.ylabel("Melhor fitness")
    plt.title(
        "LAB 01 - Evolução do fitness do PSO"
    )

    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            DIRETORIO_RESULTADOS,
            "lab01_fitness.png"
        ),
        dpi=150
    )

    plt.close()

    return resultados


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    resultados = executar_experimentos()

    print("\n")
    print("=" * 70)
    print("LAB 01 FINALIZADO")
    print("=" * 70)
