AULA 08 — Resultados
Otimização de Sistemas Computacionais e Resiliência de Redes
LAB 01 — PSO para Balanceamento Dinâmico de Carga em Datacenters
1. Objetivo

Aplicar o algoritmo PSO para encontrar a melhor distribuição de tráfego entre 6 zonas de disponibilidade (AZs), minimizando a temperatura média ponderada dos racks.

Os coeficientes de aquecimento utilizados foram:

AZ	Coeficiente
AZ1	42,0 °C
AZ2	35,0 °C
AZ3	58,0 °C
AZ4	30,0 °C
AZ5	50,0 °C
AZ6	65,0 °C

A restrição principal é:

sum(W) = 1.0


O limite crítico de temperatura considerado foi de 75 °C.

2. Resultado — População de 10 partículas
Melhor distribuição
[0. 0. 0. 1. 0. 0.]

Métricas
Métrica	Resultado
População	10
W1	0,000000
W2	0,000000
W3	0,000000
W4	1,000000
W5	0,000000
W6	0,000000
Soma dos pesos	1,000000000000
Fitness	30,000000
Temperatura ponderada	30,000000 °C
3. Resultado — População de 30 partículas
Melhor distribuição
[0. 0. 0. 1. 0. 0.]

Métricas
Métrica	Resultado
População	30
W1	0,000000
W2	0,000000
W3	0,000000
W4	1,000000
W5	0,000000
W6	0,000000
Soma dos pesos	1,000000000000
Fitness	30,000000
Temperatura ponderada	30,000000 °C
4. Resultado — População de 50 partículas
Melhor distribuição
[0. 0. 0. 1. 0. 0.]

Métricas
Métrica	Resultado
População	50
W1	0,000000
W2	0,000000
W3	0,000000
W4	1,000000
W5	0,000000
W6	0,000000
Soma dos pesos	1,000000000000
Fitness	30,000000
Temperatura ponderada	30,000000 °C
5. Comparação dos experimentos
População	Melhor W	Soma W	Fitness	Temperatura
10	[0, 0, 0, 1, 0, 0]	1,000000	30,000000	30,000000 °C
30	[0, 0, 0, 1, 0, 0]	1,000000	30,000000	30,000000 °C
50	[0, 0, 0, 1, 0, 0]	1,000000	30,000000	30,000000 °C
6. Análise

Os três tamanhos de população encontraram a mesma distribuição final.

A solução encontrada foi:

W = [0, 0, 0, 1, 0, 0]


Isso significa que 100% do peso foi direcionado para a AZ4.

A AZ4 apresenta o menor coeficiente de aquecimento:

AZ4 = 30 °C


A soma dos pesos permaneceu igual a 1 em todos os experimentos, atendendo à restrição do problema.

7. Conclusão do LAB 01

O PSO encontrou uma distribuição válida para os três tamanhos de população avaliados.

O resultado final foi:

W = [0, 0, 0, 1, 0, 0]
Fitness = 30,000000
Temperatura = 30,000000 °C

LAB 02 — AG Binário para Seleção de Microsserviços em Edge
1. Objetivo

Aplicar um Algoritmo Genético Binário para selecionar um subconjunto de 15 microsserviços, maximizando o valor de negócio e respeitando as restrições de recursos.

Restrições
Recurso	Limite
RAM	16 GB
CPU	8 cores

Foram avaliadas duas estratégias:

Estratégia A — Penalidade Rígida

Estratégia B — Penalidade Proporcional

2. Estratégia A — Penalidade Rígida
2.1 Melhor indivíduo
[1 1 1 1 1 0 1 0 0 0 1 1 1 1 0]

2.2 Resultado
Métrica	Resultado
Fitness	174,0000
Valor total	174,0000
RAM utilizada	14,9000 GB
CPU utilizada	8,0000 cores
Limite de RAM	16 GB
Limite de CPU	8 cores
2.3 Microsserviços selecionados
Nº	Microsserviço	Valor	RAM (GB)	CPU
1	auth	12,0	1,0	0,5
2	usuarios	15,0	1,2	0,7
3	catalogo	18,0	1,8	0,8
4	pagamentos	30,0	2,5	1,4
5	pedidos	24,0	2,0	1,2
7	notificacoes	14,0	1,1	0,6
11	chat	16,0	1,4	0,8
12	logs	10,0	0,8	0,4
13	monitoramento	13,0	1,0	0,5
14	relatorios	22,0	2,1	1,1
Total		174,0	14,9	8,0
3. Estratégia B — Penalidade Proporcional
3.1 Melhor indivíduo
[1 1 1 1 1 0 1 0 0 0 1 1 1 1 0]

3.2 Resultado
Métrica	Resultado
Fitness	174,0000
Valor total	174,0000
RAM utilizada	14,9000 GB
CPU utilizada	8,0000 cores
Limite de RAM	16 GB
Limite de CPU	8 cores
3.3 Microsserviços selecionados
Nº	Microsserviço	Valor	RAM (GB)	CPU
1	auth	12,0	1,0	0,5
2	usuarios	15,0	1,2	0,7
3	catalogo	18,0	1,8	0,8
4	pagamentos	30,0	2,5	1,4
5	pedidos	24,0	2,0	1,2
7	notificacoes	14,0	1,1	0,6
11	chat	16,0	1,4	0,8
12	logs	10,0	0,8	0,4
13	monitoramento	13,0	1,0	0,5
14	relatorios	22,0	2,1	1,1
Total		174,0	14,9	8,0
4. Comparação das estratégias
Métrica	Estratégia A	Estratégia B
Fitness	174,0000	174,0000
Valor total	174,0000	174,0000
RAM	14,9000 GB	14,9000 GB
CPU	8,0000 cores	8,0000 cores
Indivíduo final	Igual	Igual
5. Análise

As duas estratégias encontraram o mesmo indivíduo final:

[1 1 1 1 1 0 1 0 0 0 1 1 1 1 0]


A solução utiliza:

RAM = 14,9 GB
CPU = 8,0 cores


A utilização de RAM permanece 1,1 GB abaixo do limite máximo.

A utilização de CPU corresponde exatamente ao limite permitido de 8 cores.

O valor de negócio acumulado foi de 174,0.

6. Conclusão do LAB 02

As duas estratégias produziram a mesma solução final nos resultados apresentados.

A configuração selecionada possui:

Valor = 174,0
RAM = 14,9 GB
CPU = 8,0 cores


A solução respeita as duas restrições de capacidade.

LAB 03 — ACO para Projeto de Topologia de Rede de Baixa Latência
1. Objetivo

Aplicar o algoritmo de Colônia de Formigas (ACO) para construir uma topologia de rede em árvore conectando 10 switches.

A solução deve evitar ciclos e conectar todos os switches utilizando uma árvore geradora.

2. Topologia encontrada

A melhor topologia encontrada pelo ACO foi:

Nº	Conexão
1	Switch 1 ↔ Switch 2
2	Switch 1 ↔ Switch 6
3	Switch 2 ↔ Switch 3
4	Switch 2 ↔ Switch 9
5	Switch 4 ↔ Switch 5
6	Switch 6 ↔ Switch 7
7	Switch 9 ↔ Switch 10
8	Switch 5 ↔ Switch 6
9	Switch 8 ↔ Switch 9

A topologia possui:

10 switches
9 arestas

3. Latência da topologia ACO

A latência acumulada encontrada foi:

253,0000

4. Matriz de Adjacência Final
[[0 1 0 0 0 1 0 0 0 0]
 [1 0 1 0 0 0 0 0 1 0]
 [0 1 0 0 0 0 0 0 0 0]
 [0 0 0 0 1 0 0 0 0 0]
 [0 0 0 1 0 1 0 0 0 0]
 [1 0 0 0 1 0 1 0 0 0]
 [0 0 0 0 0 1 0 0 0 0]
 [0 0 0 0 0 0 0 0 1 0]
 [0 1 0 0 0 0 0 1 0 1]
 [0 0 0 0 0 0 0 0 1 0]]

5. Comparação com topologias aleatórias

Foram avaliadas 100 topologias aleatórias válidas.

Métrica	Resultado
Latência ACO	253,0000
Latência média aleatória	403,7200
Melhor latência aleatória	235,0000
Ganho contra média aleatória	37,33%
6. Cálculo do ganho percentual

O ganho percentual foi calculado utilizando a média das topologias aleatórias:

((403,72 - 253,00) / 403,72) × 100


Resultado:

37,33%


A solução ACO apresentou uma redução de 37,33% em relação à latência média das topologias aleatórias avaliadas.

7. Observação sobre a melhor solução aleatória

Entre as 100 topologias aleatórias, a melhor apresentou latência de:

235,0000


Esse valor é inferior à latência de 253,0000 encontrada pelo ACO nessa execução.

Portanto, o valor de 37,33% apresentado anteriormente representa especificamente a redução em relação à latência média das topologias aleatórias, e não em relação à melhor solução aleatória.

8. Conclusão do LAB 03

O ACO encontrou uma topologia válida formada por 10 switches e 9 conexões.

A latência acumulada da solução encontrada foi:

253,0000


A média das 100 topologias aleatórias foi:

403,7200


A redução em relação à média foi:

37,33%


A matriz de adjacência apresentada representa a topologia final encontrada pelo algoritmo.

RESULTADOS FINAIS DA AULA 08
LAB 01
Algoritmo: PSO
Melhor distribuição: [0, 0, 0, 1, 0, 0]
Fitness: 30,000000
Temperatura: 30,000000 °C
Soma dos pesos: 1,000000

LAB 02
Algoritmo: AG Binário
Melhor indivíduo: [1 1 1 1 1 0 1 0 0 0 1 1 1 1 0]
Fitness: 174,0000
Valor: 174,0000
RAM: 14,9000 GB
CPU: 8,0000 cores

LAB 03
Algoritmo: ACO
Latência ACO: 253,0000
Latência média aleatória: 403,7200
Ganho contra média aleatória: 37,33%
