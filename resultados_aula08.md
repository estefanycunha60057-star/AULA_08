Resultado LAB 01: 

======================================================================
PSO - POPULAÇÃO: 10
======================================================================
Melhor distribuição W:
[0. 0. 0. 1. 0. 0.]
Soma dos pesos: 1.000000000000
Fitness final: 30.000000
Temperatura ponderada: 30.000000 °C

======================================================================
PSO - POPULAÇÃO: 30
======================================================================
Melhor distribuição W:
[0. 0. 0. 1. 0. 0.]
Soma dos pesos: 1.000000000000
Fitness final: 30.000000
Temperatura ponderada: 30.000000 °C

======================================================================
PSO - POPULAÇÃO: 50
======================================================================
Melhor distribuição W:
[0. 0. 0. 1. 0. 0.]
Soma dos pesos: 1.000000000000
Fitness final: 30.000000
Temperatura ponderada: 30.000000 °C


Resultado Lab 02:

======================================================================
ESTRATÉGIA A
======================================================================
Melhor indivíduo:
[1 1 1 1 1 0 1 0 0 0 1 1 1 1 0]
Fitness: 174.0000
Valor total: 174.0000
RAM: 14.9000 GB
CPU: 8.0000 cores

Microsserviços selecionados:
 1 - auth            | Valor= 12.0 | RAM= 1.0 | CPU= 0.5
 2 - usuarios        | Valor= 15.0 | RAM= 1.2 | CPU= 0.7
 3 - catalogo        | Valor= 18.0 | RAM= 1.8 | CPU= 0.8
 4 - pagamentos      | Valor= 30.0 | RAM= 2.5 | CPU= 1.4
 5 - pedidos         | Valor= 24.0 | RAM= 2.0 | CPU= 1.2
 7 - notificacoes    | Valor= 14.0 | RAM= 1.1 | CPU= 0.6
11 - chat            | Valor= 16.0 | RAM= 1.4 | CPU= 0.8
12 - logs            | Valor= 10.0 | RAM= 0.8 | CPU= 0.4
13 - monitoramento   | Valor= 13.0 | RAM= 1.0 | CPU= 0.5
14 - relatorios      | Valor= 22.0 | RAM= 2.1 | CPU= 1.1


======================================================================
ESTRATÉGIA B
======================================================================
Melhor indivíduo:
[1 1 1 1 1 0 1 0 0 0 1 1 1 1 0]
Fitness: 174.0000
Valor total: 174.0000
RAM: 14.9000 GB
CPU: 8.0000 cores

Microsserviços selecionados:
 1 - auth            | Valor= 12.0 | RAM= 1.0 | CPU= 0.5
 2 - usuarios        | Valor= 15.0 | RAM= 1.2 | CPU= 0.7
 3 - catalogo        | Valor= 18.0 | RAM= 1.8 | CPU= 0.8
 4 - pagamentos      | Valor= 30.0 | RAM= 2.5 | CPU= 1.4
 5 - pedidos         | Valor= 24.0 | RAM= 2.0 | CPU= 1.2
 7 - notificacoes    | Valor= 14.0 | RAM= 1.1 | CPU= 0.6
11 - chat            | Valor= 16.0 | RAM= 1.4 | CPU= 0.8
12 - logs            | Valor= 10.0 | RAM= 0.8 | CPU= 0.4
13 - monitoramento   | Valor= 13.0 | RAM= 1.0 | CPU= 0.5
14 - relatorios      | Valor= 22.0 | RAM= 2.1 | CPU= 1.1


======================================================================
LAB 02 FINALIZADO
======================================================================

Resultados Lab 03:

======================================================================
LAB 03 - ACO
======================================================================

Melhor topologia encontrada pelo ACO:
Switch 1 <-> Switch 2
Switch 1 <-> Switch 6
Switch 2 <-> Switch 3
Switch 2 <-> Switch 9
Switch 4 <-> Switch 5
Switch 6 <-> Switch 7
Switch 9 <-> Switch 10
Switch 5 <-> Switch 6
Switch 8 <-> Switch 9

Latência da topologia ACO: 253.0000

Matriz de Adjacência Final:
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

Latência média das árvores aleatórias: 403.7200
Melhor latência aleatória: 235.0000
Ganho percentual do ACO em relação à média aleatória: 37.33%


======================================================================
LAB 03 FINALIZADO
======================================================================
