import os
import numpy as np
import matplotlib.pyplot as plt

SEED = 42
NUM_SWITCHES = 10
NUM_FORMIGAS = 30
NUM_ITERACOES = 100
ALPHA = 1.0
BETA = 3.0
RHO = 0.2
Q = 100.0
DIRETORIO_RESULTADOS = "resultados"

D = np.array([
    [0, 10, 18, 22, 30, 28, 35, 40, 45, 50],
    [10, 0, 12, 20, 25, 30, 32, 38, 42, 48],
    [18, 12, 0, 14, 22, 24, 28, 35, 40, 45],
    [22, 20, 14, 0, 16, 20, 25, 30, 36, 42],
    [30, 25, 22, 16, 0, 12, 18, 25, 30, 38],
    [28, 30, 24, 20, 12, 0, 15, 22, 28, 35],
    [35, 32, 28, 25, 18, 15, 0, 14, 20, 28],
    [40, 38, 35, 30, 25, 22, 14, 0, 16, 24],
    [45, 42, 40, 36, 30, 28, 20, 16, 0, 18],
    [50, 48, 45, 42, 38, 35, 28, 24, 18, 0]
], dtype=float)

PARES_CRITICOS = [
    (0, 9),
    (1, 8),
    (2, 7),
    (3, 6),
    (0, 5)
]

class UnionFind:

    def __init__(self, tamanho):

        self.parent = list(
            range(tamanho)
        )

        self.rank = [
            0
            for _ in range(tamanho)
        ]

    def find(self, x):

        if self.parent[x] != x:

            self.parent[x] = self.find(
                self.parent[x]
            )

        return self.parent[x]

    def union(self, a, b):

        raiz_a = self.find(a)
        raiz_b = self.find(b)

        if raiz_a == raiz_b:
            return False

        if self.rank[raiz_a] < self.rank[raiz_b]:

            self.parent[raiz_a] = raiz_b

        elif self.rank[raiz_a] > self.rank[raiz_b]:

            self.parent[raiz_b] = raiz_a

        else:

            self.parent[raiz_b] = raiz_a
            self.rank[raiz_a] += 1

        return True


def criar_lista_arestas():

    arestas = []

    for i in range(NUM_SWITCHES):

        for j in range(i + 1, NUM_SWITCHES):

            arestas.append((i, j))

    return arestas


ARESTAS = criar_lista_arestas()

def eh_arvore(arestas):

    if len(arestas) != NUM_SWITCHES - 1:
        return False

    uf = UnionFind(NUM_SWITCHES)

    for a, b in arestas:

        if not uf.union(a, b):
            return False

    raizes = set(
        uf.find(i)
        for i in range(NUM_SWITCHES)
    )

    return len(raizes) == 1


def dijkstra(origem, adjacencia):

    infinito = float("inf")

    distancias = [
        infinito
        for _ in range(NUM_SWITCHES)
    ]

    visitado = [
        False
        for _ in range(NUM_SWITCHES)
    ]

    distancias[origem] = 0.0

    for _ in range(NUM_SWITCHES):

        melhor = None
        melhor_distancia = infinito

        for i in range(NUM_SWITCHES):

            if (
                not visitado[i]
                and distancias[i] < melhor_distancia
            ):

                melhor = i
                melhor_distancia = distancias[i]

        if melhor is None:
            break

        visitado[melhor] = True

        for vizinho, peso in adjacencia[melhor]:

            nova_distancia = (
                distancias[melhor] + peso
            )

            if nova_distancia < distancias[vizinho]:

                distancias[vizinho] = nova_distancia

    return distancias


def criar_adjacencia(arestas):

    adj = [
        []
        for _ in range(NUM_SWITCHES)
    ]

    for a, b in arestas:

        adj[a].append(
            (b, D[a][b])
        )

        adj[b].append(
            (a, D[a][b])
        )

    return adj


def calcular_latencia(arestas):

    if not eh_arvore(arestas):
        return float("inf")

    adj = criar_adjacencia(arestas)

    total = 0.0

    for origem, destino in PARES_CRITICOS:

        distancias = dijkstra(
            origem,
            adj
        )

        total += distancias[destino]

    return total


def construir_solucao(
    feromonio,
    rng
):

    uf = UnionFind(NUM_SWITCHES)
    selecionadas = []
    arestas_disponiveis = ARESTAS.copy()

    while len(selecionadas) < NUM_SWITCHES - 1:

        candidatos = []
        pesos = []

        for indice, (a, b) in enumerate(
            arestas_disponiveis
        ):

            if uf.find(a) == uf.find(b):
                continue

            tau = feromonio[a][b]

            eta = 1.0 / max(
                D[a][b],
                1e-9
            )

            peso = (
                (tau ** ALPHA)
                *
                (eta ** BETA)
            )

            candidatos.append(
                (indice, a, b)
            )

            pesos.append(peso)

        if not candidatos:
            break

        pesos = np.array(
            pesos,
            dtype=float
        )

        soma = np.sum(pesos)

        if soma <= 0:

            probabilidades = (
                np.ones(len(pesos))
                / len(pesos)
            )

        else:

            probabilidades = (
                pesos / soma
            )

        escolhido = rng.choice(
            len(candidatos),
            p=probabilidades
        )

        indice, a, b = (
            candidatos[escolhido]
        )

        if uf.union(a, b):

            selecionadas.append(
                (a, b)
            )

        arestas_disponiveis.pop(indice)

    return selecionadas


def criar_matriz_adjacencia(arestas):

    matriz = np.zeros(
        (
            NUM_SWITCHES,
            NUM_SWITCHES
        ),
        dtype=int
    )

    for a, b in arestas:

        matriz[a][b] = 1
        matriz[b][a] = 1

    return matriz


def executar_aco(seed):

    rng = np.random.default_rng(seed)

    feromonio = np.ones(
        (
            NUM_SWITCHES,
            NUM_SWITCHES
        ),
        dtype=float
    )

    melhor_global = None
    melhor_global_latencia = float("inf")
    historico = []

    for _ in range(NUM_ITERACOES):

        solucoes = []

        for _ in range(NUM_FORMIGAS):

            solucao = construir_solucao(
                feromonio,
                rng
            )

            if eh_arvore(solucao):

                latencia = calcular_latencia(
                    solucao
                )

                solucoes.append(
                    (
                        solucao,
                        latencia
                    )
                )

        if not solucoes:
            continue

        melhor_iteracao = min(
            solucoes,
            key=lambda x: x[1]
        )

        solucao_iteracao = (
            melhor_iteracao[0]
        )

        latencia_iteracao = (
            melhor_iteracao[1]
        )

        if latencia_iteracao < melhor_global_latencia:

            melhor_global_latencia = (
                latencia_iteracao
            )

            melhor_global = (
                solucao_iteracao.copy()
            )

        feromonio *= (
            1.0 - RHO
        )

        deposito = (
            Q
            / max(latencia_iteracao, 1e-9)
        )

        for a, b in solucao_iteracao:

            feromonio[a][b] += deposito
            feromonio[b][a] += deposito

        historico.append(
            melhor_global_latencia
        )

    return (
        melhor_global,
        melhor_global_latencia,
        historico
    )


def gerar_arvore_aleatoria(rng):

    while True:

        arestas = ARESTAS.copy()

        rng.shuffle(arestas)

        uf = UnionFind(NUM_SWITCHES)
        arvore = []

        for a, b in arestas:

            if uf.union(a, b):

                arvore.append(
                    (a, b)
                )

                if len(arvore) == NUM_SWITCHES - 1:
                    break

        if eh_arvore(arvore):
            return arvore


def main():

    os.makedirs(
        DIRETORIO_RESULTADOS,
        exist_ok=True
    )

    print("\n")
    print("=" * 70)
    print("LAB 03 - ACO")
    print("=" * 70)

    melhor_aco, latencia_aco, historico = (
        executar_aco(SEED)
    )

    print("\nMelhor topologia encontrada pelo ACO:")

    for a, b in melhor_aco:

        print(
            f"Switch {a + 1} <-> Switch {b + 1}"
        )

    print(
        f"\nLatência da topologia ACO: "
        f"{latencia_aco:.4f}"
    )

    matriz = criar_matriz_adjacencia(
        melhor_aco
    )

    print("\nMatriz de Adjacência Final:")
    print(matriz)

    arquivo_adjacencia = os.path.join(
        DIRETORIO_RESULTADOS,
        "lab03_adjacencia.txt"
    )

    with open(
        arquivo_adjacencia,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            "Matriz de Adjacência Final\n\n"
        )

        arquivo.write(
            str(matriz)
        )

        arquivo.write(
            "\n\nArestas:\n"
        )

        for a, b in melhor_aco:

            arquivo.write(
                f"Switch {a + 1} <-> "
                f"Switch {b + 1}\n"
            )

    rng = np.random.default_rng(
        SEED + 100
    )

    NUM_BASELINES = 100

    latencias_aleatorias = []

    for _ in range(NUM_BASELINES):

        arvore = gerar_arvore_aleatoria(rng)

        latencia = calcular_latencia(
            arvore
        )

        latencias_aleatorias.append(
            latencia
        )

    media_aleatoria = np.mean(
        latencias_aleatorias
    )

    melhor_aleatoria = np.min(
        latencias_aleatorias
    )

    ganho_percentual = (
        (
            media_aleatoria
            - latencia_aco
        )
        / media_aleatoria
        * 100.0
    )

    print(
        "\nLatência média das árvores aleatórias: "
        f"{media_aleatoria:.4f}"
    )

    print(
        "Melhor latência aleatória: "
        f"{melhor_aleatoria:.4f}"
    )

    print(
        "Ganho percentual do ACO em relação "
        "à média aleatória: "
        f"{ganho_percentual:.2f}%"
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        historico,
        label="Melhor ACO"
    )

    plt.axhline(
        media_aleatoria,
        linestyle="--",
        label="Média das topologias aleatórias"
    )

    plt.xlabel("Iteração")
    plt.ylabel("Latência")
    plt.title(
        "LAB 03 - Convergência do ACO"
    )

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            DIRETORIO_RESULTADOS,
            "lab03_convergencia.png"
        ),
        dpi=150
    )

    plt.close()

    arquivo_resultados = os.path.join(
        DIRETORIO_RESULTADOS,
        "lab03_resultados.txt"
    )

    with open(
        arquivo_resultados,
        "w",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(
            "LAB 03 - RESULTADOS\n"
        )

        arquivo.write(
            "=" * 60 + "\n\n"
        )

        arquivo.write(
            f"Latência ACO: "
            f"{latencia_aco:.6f}\n"
        )

        arquivo.write(
            f"Latência média aleatória: "
            f"{media_aleatoria:.6f}\n"
        )

        arquivo.write(
            f"Melhor latência aleatória: "
            f"{melhor_aleatoria:.6f}\n"
        )

        arquivo.write(
            f"Ganho percentual contra média aleatória: "
            f"{ganho_percentual:.6f}%\n"
        )

        arquivo.write(
            "\nArestas ACO:\n"
        )

        for a, b in melhor_aco:

            arquivo.write(
                f"{a + 1} - {b + 1}\n"
            )

    print("\n")
    print("=" * 70)
    print("LAB 03 FINALIZADO")
    print("=" * 70)


if __name__ == "__main__":
    main()
