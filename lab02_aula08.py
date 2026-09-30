import os
import csv
import numpy as np
import matplotlib.pyplot as plt

SEED = 42
NUM_SERVICOS = 15
CAPACIDADE_RAM = 16.0
CAPACIDADE_CPU = 8.0
TAMANHO_POPULACAO = 60
NUM_GERACOES = 100
TAXA_CROSSOVER = 0.85
TAXA_MUTACAO = 0.05
TAMANHO_TORNEIO = 3
NUM_EXECUCOES = 10
DIRETORIO_RESULTADOS = "resultados"

NOMES = [
    "auth",
    "usuarios",
    "catalogo",
    "pagamentos",
    "pedidos",
    "estoque",
    "notificacoes",
    "analytics",
    "recomendacao",
    "busca",
    "chat",
    "logs",
    "monitoramento",
    "relatorios",
    "fraude"
]

VALOR = np.array([
    12, 15, 18, 30, 24,
    20, 14, 25, 28, 17,
    16, 10, 13, 22, 32
], dtype=float)

RAM = np.array([
    1.0, 1.2, 1.8, 2.5, 2.0,
    1.7, 1.1, 2.3, 2.8, 1.5,
    1.4, 0.8, 1.0, 2.1, 3.0
])

CPU = np.array([
    0.5, 0.7, 0.8, 1.4, 1.2,
    1.0, 0.6, 1.3, 1.6, 0.9,
    0.8, 0.4, 0.5, 1.1, 1.8
])

def calcular_recursos(individuo):

    ram_total = np.sum(individuo * RAM)
    cpu_total = np.sum(individuo * CPU)
    valor_total = np.sum(individuo * VALOR)

    return valor_total, ram_total, cpu_total


def fitness_rigido(individuo):

    valor, ram, cpu = calcular_recursos(individuo)

    if (
        ram > CAPACIDADE_RAM
        or cpu > CAPACIDADE_CPU
    ):
        return 0.0

    return valor


def fitness_proporcional(individuo):

    valor, ram, cpu = calcular_recursos(individuo)

    excesso_ram = max(
        0.0,
        ram - CAPACIDADE_RAM
    )

    excesso_cpu = max(
        0.0,
        cpu - CAPACIDADE_CPU
    )

    penalidade_ram = (
        excesso_ram / CAPACIDADE_RAM
    )

    penalidade_cpu = (
        excesso_cpu / CAPACIDADE_CPU
    )

    fator_ram = max(
        0.0,
        1.0 - penalidade_ram
    )

    fator_cpu = max(
        0.0,
        1.0 - penalidade_cpu
    )

    return valor * fator_ram * fator_cpu


def reparar_individuo(individuo, rng):

    individuo = individuo.copy()

    while True:

        _, ram, cpu = calcular_recursos(individuo)

        if (
            ram <= CAPACIDADE_RAM
            and cpu <= CAPACIDADE_CPU
        ):
            break

        selecionados = np.where(
            individuo == 1
        )[0]

        if len(selecionados) == 0:
            break

        razoes = []

        for indice in selecionados:

            consumo = RAM[indice] + CPU[indice]

            razao = (
                VALOR[indice]
                / max(consumo, 0.001)
            )

            razoes.append(
                (razao, indice)
            )

        _, indice_remover = min(
            razoes,
            key=lambda x: x[0]
        )

        individuo[indice_remover] = 0

    return individuo


def criar_individuo(rng):

    return rng.integers(
        0,
        2,
        size=NUM_SERVICOS
    ).astype(int)


def criar_populacao(rng):

    return np.array([
        criar_individuo(rng)
        for _ in range(TAMANHO_POPULACAO)
    ])


def selecao_torneio(
    populacao,
    fitness,
    rng
):

    indices = rng.choice(
        len(populacao),
        size=TAMANHO_TORNEIO,
        replace=False
    )

    melhor = indices[
        np.argmax(fitness[indices])
    ]

    return populacao[melhor].copy()


def crossover_ponto_unico(
    pai1,
    pai2,
    rng
):

    if rng.random() > TAXA_CROSSOVER:
        return pai1.copy(), pai2.copy()

    ponto = rng.integers(
        1,
        NUM_SERVICOS
    )

    filho1 = np.concatenate([
        pai1[:ponto],
        pai2[ponto:]
    ])

    filho2 = np.concatenate([
        pai2[:ponto],
        pai1[ponto:]
    ])

    return filho1, filho2


def mutacao(individuo, rng):

    individuo = individuo.copy()

    for i in range(NUM_SERVICOS):

        if rng.random() < TAXA_MUTACAO:
            individuo[i] = 1 - individuo[i]

    return individuo


def calcular_diversidade(populacao):

    if len(populacao) == 0:
        return 0.0

    individuos_unicos = set(
        tuple(individuo)
        for individuo in populacao
    )

    return (
        len(individuos_unicos)
        / len(populacao)
    )


def executar_ag(estrategia, seed):

    rng = np.random.default_rng(seed)

    populacao = criar_populacao(rng)

    historico_media = []
    historico_desvio = []
    historico_diversidade = []

    melhor_individuo = None
    melhor_fitness = -np.inf

    for _ in range(NUM_GERACOES):

        if estrategia == "A":

            fitness = np.array([
                fitness_rigido(ind)
                for ind in populacao
            ])

        else:

            fitness = np.array([
                fitness_proporcional(ind)
                for ind in populacao
            ])

        media = np.mean(fitness)
        desvio = np.std(fitness)

        diversidade = calcular_diversidade(
            populacao
        )

        historico_media.append(media)
        historico_desvio.append(desvio)
        historico_diversidade.append(diversidade)

        indice_melhor = np.argmax(fitness)

        if fitness[indice_melhor] > melhor_fitness:

            melhor_fitness = fitness[indice_melhor]

            melhor_individuo = (
                populacao[indice_melhor].copy()
            )

        nova_populacao = []

        while len(nova_populacao) < TAMANHO_POPULACAO:

            pai1 = selecao_torneio(
                populacao,
                fitness,
                rng
            )

            pai2 = selecao_torneio(
                populacao,
                fitness,
                rng
            )

            filho1, filho2 = crossover_ponto_unico(
                pai1,
                pai2,
                rng
            )

            filho1 = mutacao(
                filho1,
                rng
            )

            filho2 = mutacao(
                filho2,
                rng
            )

            filho1 = reparar_individuo(
                filho1,
                rng
            )

            filho2 = reparar_individuo(
                filho2,
                rng
            )

            nova_populacao.append(filho1)

            if len(nova_populacao) < TAMANHO_POPULACAO:
                nova_populacao.append(filho2)

        populacao = np.array(nova_populacao)

    return {
        "estrategia": estrategia,
        "melhor_individuo": melhor_individuo,
        "melhor_fitness": melhor_fitness,
        "media": historico_media,
        "desvio": historico_desvio,
        "diversidade": historico_diversidade
    }


def listar_servicos(individuo):

    selecionados = []

    for i, bit in enumerate(individuo):

        if bit == 1:

            selecionados.append({
                "indice": i + 1,
                "nome": NOMES[i],
                "valor": VALOR[i],
                "ram": RAM[i],
                "cpu": CPU[i]
            })

    return selecionados


def main():

    os.makedirs(
        DIRETORIO_RESULTADOS,
        exist_ok=True
    )

    resultados = {}

    for estrategia in ["A", "B"]:

        print("\n")
        print("=" * 70)
        print(f"ESTRATÉGIA {estrategia}")
        print("=" * 70)

        execucoes = []

        for execucao in range(NUM_EXECUCOES):

            resultado = executar_ag(
                estrategia,
                SEED + execucao
            )

            execucoes.append(resultado)

        media_geracoes = np.mean(
            [
                r["media"]
                for r in execucoes
            ],
            axis=0
        )

        desvio_geracoes = np.mean(
            [
                r["desvio"]
                for r in execucoes
            ],
            axis=0
        )

        diversidade_geracoes = np.mean(
            [
                r["diversidade"]
                for r in execucoes
            ],
            axis=0
        )

        melhor_execucao = max(
            execucoes,
            key=lambda r: r["melhor_fitness"]
        )

        resultados[estrategia] = {
            "media": media_geracoes,
            "desvio": desvio_geracoes,
            "diversidade": diversidade_geracoes,
            "melhor_individuo": (
                melhor_execucao["melhor_individuo"]
            ),
            "melhor_fitness": (
                melhor_execucao["melhor_fitness"]
            )
        }

        individuo = melhor_execucao[
            "melhor_individuo"
        ]

        valor, ram, cpu = calcular_recursos(
            individuo
        )

        print("Melhor indivíduo:")
        print(individuo)

        print(
            f"Fitness: "
            f"{melhor_execucao['melhor_fitness']:.4f}"
        )

        print(f"Valor total: {valor:.4f}")
        print(f"RAM: {ram:.4f} GB")
        print(f"CPU: {cpu:.4f} cores")

        print("\nMicrosserviços selecionados:")

        for servico in listar_servicos(individuo):

            print(
                f"{servico['indice']:2d} - "
                f"{servico['nome']:15s} | "
                f"Valor={servico['valor']:5.1f} | "
                f"RAM={servico['ram']:4.1f} | "
                f"CPU={servico['cpu']:4.1f}"
            )

    arquivo_csv = os.path.join(
        DIRETORIO_RESULTADOS,
        "lab02_resultados.csv"
    )

    with open(
        arquivo_csv,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        escritor = csv.writer(arquivo)

        escritor.writerow([
            "estrategia",
            "melhor_fitness",
            "valor_total",
            "ram",
            "cpu",
            "diversidade_media"
        ])

        for estrategia in ["A", "B"]:

            individuo = resultados[
                estrategia
            ]["melhor_individuo"]

            valor, ram, cpu = calcular_recursos(
                individuo
            )

            diversidade_media = np.mean(
                resultados[
                    estrategia
                ]["diversidade"]
            )

            escritor.writerow([
                estrategia,
                resultados[
                    estrategia
                ]["melhor_fitness"],
                valor,
                ram,
                cpu,
                diversidade_media
            ])

    plt.figure(figsize=(10, 6))

    for estrategia in ["A", "B"]:

        plt.plot(
            resultados[estrategia]["media"],
            label=f"Estratégia {estrategia}"
        )

    plt.xlabel("Geração")
    plt.ylabel("Fitness médio")
    plt.title(
        "LAB 02 - Fitness médio por geração"
    )

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            DIRETORIO_RESULTADOS,
            "lab02_fitness.png"
        ),
        dpi=150
    )

    plt.close()

    plt.figure(figsize=(10, 6))

    for estrategia in ["A", "B"]:

        plt.plot(
            resultados[estrategia]["diversidade"],
            label=f"Estratégia {estrategia}"
        )

    plt.xlabel("Geração")
    plt.ylabel("Diversidade genética")
    plt.title(
        "LAB 02 - Diversidade genética"
    )

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            DIRETORIO_RESULTADOS,
            "lab02_diversidade.png"
        ),
        dpi=150
    )

    plt.close()

    print("\n")
    print("=" * 70)
    print("LAB 02 FINALIZADO")
    print("=" * 70)


if __name__ == "__main__":
    main()
