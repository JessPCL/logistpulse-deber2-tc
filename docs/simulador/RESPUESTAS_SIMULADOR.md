# Respuestas para pegar en el simulador

Se genera con `python scripts/armar_simulador.py`, que antes ejecuta los 10 programas y comprueba que pasan sus pruebas.

**Cómo llenarlo:** abre el .html **siempre en el mismo navegador**, sin modo incógnito (el avance se guarda en ese navegador). Escribe tu nombre y tu código y entra. Para cada correo: elige las 4 opciones, pega los dos textos y el código, y presiona **Enviar respuesta**. Al final usa **Descargar .txt**.

| Correo | Clasificación | Algoritmo | ¿Decidible? | Estado del caso |
|---|---|---|---|---|
| p1 | P | BFS | Decidible | Problema de decisión |
| p2 | P | Dijkstra | Decidible | Problema de optimización |
| p3 | P | Edmonds–Karp | Decidible | Problema de optimización |
| n1 | NP | Búsqueda exhaustiva de permutaciones | Decidible | Problema de decisión |
| n2 | NP | Prueba por división exhaustiva | Decidible | Problema de decisión |
| n3 | NP | Búsqueda exhaustiva con exponenciación modular | Decidible | Problema de decisión |
| n4 | NP | Permutaciones + verificación de adyacencia | Decidible | Problema de decisión |
| c1 | NP-completo | DPLL / retroceso con poda | Decidible | Problema de decisión |
| c2 | NP-completo | Backtracking / enumerar permutaciones | Decidible | Problema de decisión |
| c3 | NP-completo | Backtracking / ramificación | Decidible | Problema de decisión |

## p1 · P

**Clasificación:** P · **Algoritmo:** BFS · **¿Decidible?:** Decidible · **Estado:** Problema de decisión

**Computabilidad** (pegar en el primer recuadro):

```text
Sí existe un procedimiento efectivo: BFS desde Durán sobre los tramos habilitados. Termina porque cada zona entra a la cola a lo sumo una vez y cada tramo se revisa una vez; si la cola se vacía sin llegar a Norte, la respuesta es No. Es un problema de decisión (¿existe ruta?) y el camino encontrado sirve como evidencia.
```

**Complejidad** (pegar en el segundo recuadro):

```text
Entrada: grafo dirigido con V zonas y E tramos (lista de conexiones). Tiempo O(V + E): cada zona se encola una vez y cada tramo se examina una vez. Espacio O(V) para la cola y los padres, más O(V + E) para la lista de adyacencia. Es polinomial, por eso el problema está en P.
```

**Código** (pegar en el recuadro de código):

```python
from collections import deque


def hay_ruta(conexiones, origen, destino):
    """BFS sobre tramos con sentido. Devuelve el camino o None. Tiempo O(V + E), espacio O(V)."""
    ady = {}
    for u, v in conexiones:
        ady.setdefault(u, []).append(v)
        ady.setdefault(v, [])
    if origen not in ady or destino not in ady:
        return None
    padre = {origen: None}
    cola = deque([origen])
    while cola:
        u = cola.popleft()
        if u == destino:
            camino = []
            while u is not None:
                camino.append(u)
                u = padre[u]
            return camino[::-1]
        for v in ady[u]:
            if v not in padre:  # cada zona entra a la cola una sola vez
                padre[v] = u
                cola.append(v)
    return None


# Entrada: tramos habilitados del expediente (las flechas del mapa tienen sentido)
tramos = [("Durán", "Quito"), ("Durán", "Guayaquil"), ("Quito", "Norte"), ("Guayaquil", "Sur")]
print("¿Hay ruta Durán -> Norte?", hay_ruta(tramos, "Durán", "Norte"))

# Pruebas: con ruta, sin ruta (cierre de Quito -> Norte) y respeto del sentido
assert hay_ruta(tramos, "Durán", "Norte") == ["Durán", "Quito", "Norte"]
sin_quito_norte = [t for t in tramos if t != ("Quito", "Norte")]
assert hay_ruta(sin_quito_norte, "Durán", "Norte") is None
assert hay_ruta(tramos, "Norte", "Durán") is None
print("Pruebas OK")
```

Salida al ejecutarlo:

```text
¿Hay ruta Durán -> Norte? ['Durán', 'Quito', 'Norte']
Pruebas OK
```

## p2 · P

**Clasificación:** P · **Algoritmo:** Dijkstra · **¿Decidible?:** Decidible · **Estado:** Problema de optimización

**Computabilidad** (pegar en el primer recuadro):

```text
Dijkstra es un procedimiento efectivo cuando los tiempos son no negativos, y aquí lo son. Termina porque cada nodo se cierra una sola vez y cada tramo se relaja un número finito de veces; las entradas viejas del heap se descartan. El sistema debe guardar pred[v] (predecesor de cada nodo) para reconstruir la ruta. Con tiempos negativos no sería correcto y habría que usar Bellman-Ford.
```

**Complejidad** (pegar en el segundo recuadro):

```text
Entrada: V centros y E tramos con tiempos >= 0. Con heap binario y listas de adyacencia hay a lo sumo E + 1 inserciones y extracciones de costo O(log V): tiempo O((V + E) log V) y espacio O(V + E). Es polinomial, en P. Resultado: Quito -> Latacunga -> Guayaquil = 8, que empata con Quito -> Ambato -> Guayaquil = 8.
```

**Código** (pegar en el recuadro de código):

```python
import heapq


def dijkstra(tramos, origen):
    """Tiempos mínimos desde origen con tiempos >= 0. Tiempo O((V + E) log V), espacio O(V + E)."""
    ady = {}
    for u, v, w in tramos:
        if w < 0:
            raise ValueError("Dijkstra exige tiempos no negativos")
        ady.setdefault(u, []).append((v, w))
        ady.setdefault(v, [])
    dist = {x: float("inf") for x in ady}
    pred = {x: None for x in ady}  # lo que el sistema debe conservar para reconstruir la ruta
    dist[origen] = 0
    heap = [(0, origen)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # entrada vieja del heap
        for v, w in ady[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                pred[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, pred


def ruta(pred, destino):
    camino = []
    while destino is not None:
        camino.append(destino)
        destino = pred[destino]
    return camino[::-1]


# Entrada: tiempos nuevos del expediente (tramos con sentido)
tramos = [("Quito", "Latacunga", 2), ("Quito", "Ambato", 5), ("Latacunga", "Guayaquil", 6), ("Ambato", "Guayaquil", 3)]
dist, pred = dijkstra(tramos, "Quito")
print("Tiempo mínimo Quito -> Guayaquil:", dist["Guayaquil"], "| ruta:", " -> ".join(ruta(pred, "Guayaquil")))

# Pruebas: tiempos a cada nodo, empate en 8 y rechazo de pesos negativos
assert dist == {"Quito": 0, "Latacunga": 2, "Ambato": 5, "Guayaquil": 8}
assert ruta(pred, "Guayaquil") == ["Quito", "Latacunga", "Guayaquil"]  # Quito -> Ambato -> Guayaquil también suma 8
try:
    dijkstra([("S", "A", 2), ("S", "B", 3), ("B", "A", -2)], "S")
    raise AssertionError("debía rechazar el peso negativo")
except ValueError:
    pass  # con pesos negativos Dijkstra no garantiza el mínimo (se usaría Bellman-Ford)
print("Pruebas OK")
```

Salida al ejecutarlo:

```text
Tiempo mínimo Quito -> Guayaquil: 8 | ruta: Quito -> Latacunga -> Guayaquil
Pruebas OK
```

## p3 · P

**Clasificación:** P · **Algoritmo:** Edmonds–Karp · **¿Decidible?:** Decidible · **Estado:** Problema de optimización

**Computabilidad** (pegar en el primer recuadro):

```text
Edmonds-Karp es un procedimiento efectivo: busca con BFS un camino con capacidad residual y lo satura. Termina porque cada aumento suma al menos 1 camión (capacidades enteras) y además hace a lo sumo O(V·E) aumentos, sin depender del valor de las capacidades. El registro muestra cómo cambian los tramos usados y disponibles. Resultado: 10 camiones/día, aunque lo que sale de la Planta suma 12.
```

**Complejidad** (pegar en el segundo recuadro):

```text
Entrada: V nodos y E tramos con capacidades enteras. Hay a lo sumo O(V·E) aumentos y cada BFS cuesta O(E): tiempo O(V·E²) y espacio O(V + E) para la red residual. Es polinomial e independiente del tamaño de las capacidades, por eso está en P.
```

**Código** (pegar en el recuadro de código):

```python
from collections import deque


def edmonds_karp(tramos, s, t, registro):
    """Flujo máximo con caminos aumentantes por BFS (Edmonds-Karp). Tiempo O(V·E²), espacio O(V + E)."""
    cap, ady = {}, {}
    for u, v, c in tramos:
        for a, b in ((u, v), (v, u)):
            if (a, b) not in cap:
                cap[(a, b)] = 0
                ady.setdefault(a, []).append(b)
        cap[(u, v)] += c
    original = dict(cap)
    flujo = 0
    while True:
        padre = {s: None}
        cola = deque([s])
        while cola and t not in padre:
            u = cola.popleft()
            for v in ady[u]:
                if v not in padre and cap[(u, v)] > 0:
                    padre[v] = u
                    cola.append(v)
        if t not in padre:
            return flujo
        camino, v = [], t
        while padre[v] is not None:
            camino.append((padre[v], v))
            v = padre[v]
        camino.reverse()
        cuello = min(cap[e] for e in camino)
        for u, v in camino:
            cap[(u, v)] -= cuello
            cap[(v, u)] += cuello
        flujo += cuello
        estado = [f"{u}->{v} usado {original[(u, v)] - cap[(u, v)]}/{original[(u, v)]}" for u, v in camino]
        registro.append(f"cuello {cuello}, total {flujo}: " + "; ".join(estado))


# Entrada: capacidades del expediente (camiones/día por tramo)
tramos = [("Planta", "Quito", 7), ("Planta", "Guayaquil", 5), ("Quito", "Clientes", 4),
          ("Guayaquil", "Clientes", 6), ("Quito", "Guayaquil", 2)]
registro = []
maximo = edmonds_karp(tramos, "Planta", "Clientes", registro)
print("Máximo de camiones/día:", maximo)
for i, linea in enumerate(registro, 1):
    print(f"  Aumento {i}: {linea}")

# Pruebas: máximo 10 (no 12 = 7 + 5) y un caso con cuello de botella simple
assert maximo == 10
assert sum(c for u, v, c in tramos if u == "Planta") == 12
assert edmonds_karp([("s", "a", 3), ("a", "t", 2)], "s", "t", []) == 2
print("Pruebas OK")
```

Salida al ejecutarlo:

```text
Máximo de camiones/día: 10
  Aumento 1: cuello 4, total 4: Planta->Quito usado 4/7; Quito->Clientes usado 4/4
  Aumento 2: cuello 5, total 9: Planta->Guayaquil usado 5/5; Guayaquil->Clientes usado 5/6
  Aumento 3: cuello 1, total 10: Planta->Quito usado 5/7; Quito->Guayaquil usado 1/2; Guayaquil->Clientes usado 6/6
Pruebas OK
```

## n1 · NP

**Clasificación:** NP · **Algoritmo:** Búsqueda exhaustiva de permutaciones · **¿Decidible?:** Decidible · **Estado:** Problema de decisión

**Computabilidad** (pegar en el primer recuadro):

```text
Sí hay un procedimiento efectivo: probar las n! correspondencias y verificar cada una. Termina porque las permutaciones de n nodos son finitas. Si la respuesta es Sí, la correspondencia es un certificado que se revisa en tiempo polinomial; por eso el problema está en NP. No afirmamos que sea NP-completo ni que se conozca un algoritmo polinomial.
```

**Complejidad** (pegar en el segundo recuadro):

```text
Entrada: dos matrices de adyacencia n×n. Verificar un certificado: O(n²) comparaciones. Búsqueda exhaustiva: hasta n! permutaciones por O(n²) cada una, O(n!·n²) en tiempo y O(n) de espacio extra. Con 3 nodos son 6 candidatas; con 12 ya son unos 479 millones.
```

**Código** (pegar en el recuadro de código):

```python
from itertools import permutations


def verificar(A, B, p):
    """¿La correspondencia p conserva todas las conexiones? O(n²)."""
    n = len(A)
    return sorted(p) == list(range(n)) and all(A[i][j] == B[p[i]][p[j]] for i in range(n) for j in range(n))


def buscar(A, B):
    """Prueba las n! correspondencias. Tiempo O(n!·n²), espacio O(n)."""
    if len(A) != len(B):
        return None
    for p in permutations(range(len(A))):
        if verificar(A, B, p):
            return p
    return None


# Entrada: matrices de adyacencia de las dos redes (código del expediente)
A = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
B = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
p = buscar(A, B)
print("¿Misma estructura?", p is not None, "| correspondencia nodo i de A -> nodo p[i] de B:", p)

# Pruebas: certificado válido, identidad inválida y un par no isomorfo con los mismos grados
assert p == (1, 0, 2) and verificar(A, B, p)
assert not verificar(A, B, (0, 1, 2))
C6 = [[1 if abs(i - j) in (1, 5) else 0 for j in range(6)] for i in range(6)]
dos_triangulos = [[1 if i != j and i // 3 == j // 3 else 0 for j in range(6)] for i in range(6)]
assert buscar(C6, dos_triangulos) is None
print("Pruebas OK")
```

Salida al ejecutarlo:

```text
¿Misma estructura? True | correspondencia nodo i de A -> nodo p[i] de B: (1, 0, 2)
Pruebas OK
```

## n2 · NP

**Clasificación:** NP · **Algoritmo:** Prueba por división exhaustiva · **¿Decidible?:** Decidible · **Estado:** Problema de decisión

**Computabilidad** (pegar en el primer recuadro):

```text
Sí hay un procedimiento efectivo: probar d = 2, ..., B. Termina porque el rango es finito. El divisor d es un certificado y se verifica con una sola división (N mod d = 0 y 2 <= d <= B), en tiempo polinomial en los bits de N. Por eso el problema está en NP. La búsqueda y la validación son rutinas separadas.
```

**Complejidad** (pegar en el segundo recuadro):

```text
Entrada: N y B en binario, con log2 N y log2 B bits. Verificar: una división, polinomial en log N. Buscar: hasta B divisiones, O(B·M(log N)). Como B = 2^(log2 B), la búsqueda es exponencial en el tamaño de la entrada (pseudo-polinomial): cada bit extra de B duplica el trabajo. Resultado: N = 91 (7 bits), B = 10, d = 7.
```

**Código** (pegar en el recuadro de código):

```python
def verificar(N, B, d):
    """Verifica un divisor propuesto con una sola división: polinomial en log N."""
    return 2 <= d <= B and N % d == 0


def buscar(N, B):
    """Prueba d = 2, 3, ..., min(B, N): O(B) divisiones, exponencial en los bits de B."""
    for d in range(2, min(B, N) + 1):
        if N % d == 0:
            return d
    return None


# Entrada: datos de la consola (los números se reciben en binario)
N, B = 91, 10
d = buscar(N, B)
print(f"N = {N} ({bin(N)[2:]}, {N.bit_length()} bits), B = {B} ({bin(B)[2:]}) -> divisor:", d)

# Pruebas: divisor en el rango, rango sin divisor, certificado fuera de rango y un primo
assert d == 7 and verificar(N, B, d)
assert buscar(91, 6) is None
assert not verificar(91, 10, 13)
assert buscar(97, 96) is None
print("Pruebas OK")
```

Salida al ejecutarlo:

```text
N = 91 (1011011, 7 bits), B = 10 (1010) -> divisor: 7
Pruebas OK
```

## n3 · NP

**Clasificación:** NP · **Algoritmo:** Búsqueda exhaustiva con exponenciación modular · **¿Decidible?:** Decidible · **Estado:** Problema de decisión

**Computabilidad** (pegar en el primer recuadro):

```text
Sí hay un procedimiento efectivo: probar x = 0, ..., B. Termina porque hay B + 1 candidatos. El exponente x es un certificado y se verifica con exponenciación rápida en tiempo polinomial en log p + log B; por eso está en NP. La búsqueda y el verificador están separados y solo se usan los parámetros ficticios.
```

**Complejidad** (pegar en el segundo recuadro):

```text
Entrada: p, g, h y B en binario. Verificar: O(log x) multiplicaciones modulares. Búsqueda lineal: O(B) multiplicaciones, exponencial en los bits de B. Baby-step giant-step baja a O(raíz de B) en tiempo y espacio, pero sigue siendo exponencial en bits. Resultado: x = 6, porque 5^6 = 8 (mod 23).
```

**Código** (pegar en el recuadro de código):

```python
def verificar(p, g, h, B, x):
    """Verifica un exponente propuesto con exponenciación rápida: O(log x) multiplicaciones modulares."""
    return 0 <= x <= B and pow(g, x, p) == h % p


def buscar(p, g, h, B):
    """Prueba x = 0, 1, ..., B con una multiplicación por paso: O(B), exponencial en los bits de B."""
    valor = 1
    for x in range(B + 1):
        if valor == h % p:
            return x
        valor = valor * g % p
    return None


# Entrada: parámetros ficticios de la estación
p, g, h, B = 23, 5, 8, 10
x = buscar(p, g, h, B)
print(f"¿Existe x <= {B} con {g}^x = {h} (mod {p})?", x)

# Pruebas: exponente válido, exponente incorrecto y límite B demasiado bajo
assert x == 6 and verificar(p, g, h, B, x)
assert not verificar(p, g, h, B, 5)
assert buscar(p, g, h, 5) is None
print("Pruebas OK")
```

Salida al ejecutarlo:

```text
¿Existe x <= 10 con 5^x = 8 (mod 23)? 6
Pruebas OK
```

## n4 · NP

**Clasificación:** NP · **Algoritmo:** Permutaciones + verificación de adyacencia · **¿Decidible?:** Decidible · **Estado:** Problema de decisión

**Computabilidad** (pegar en el primer recuadro):

```text
Sí hay un procedimiento efectivo: probar las permutaciones distintas de la identidad y verificar cada una. Termina porque son finitas; si ninguna sirve, el programa responde No después de agotarlas todas (para el No no se conoce un certificado corto). Si la respuesta es Sí, la permutación es un certificado verificable en tiempo polinomial: el problema está en NP.
```

**Complejidad** (pegar en el segundo recuadro):

```text
Entrada: matriz de adyacencia n×n. Verificar una permutación: O(n²). Búsqueda: hasta n! permutaciones, O(n!·n²) en tiempo y O(n) de espacio extra. En el triángulo se encuentra (0, 2, 1); un grafo asimétrico de 6 vértices obliga a revisar las 720 permutaciones.
```

**Código** (pegar en el recuadro de código):

```python
from itertools import permutations


def verificar(G, p):
    """¿p es una simetría real (no la identidad) que conserva todas las adyacencias? O(n²)."""
    n = len(G)
    return (sorted(p) == list(range(n)) and list(p) != list(range(n))
            and all(G[i][j] == G[p[i]][p[j]] for i in range(n) for j in range(n)))


def buscar(G):
    """Prueba las n! permutaciones; si ninguna sirve, responde No tras agotarlas. O(n!·n²)."""
    for p in permutations(range(len(G))):
        if verificar(G, p):
            return p
    return None


def matriz(n, aristas):
    G = [[0] * n for _ in range(n)]
    for u, v in aristas:
        G[u][v] = G[v][u] = 1
    return G


# Entrada: el plano del portal (triángulo de 3 zonas)
triangulo = matriz(3, [(0, 1), (1, 2), (0, 2)])
p = buscar(triangulo)
print("Simetría del plano (zona i -> zona p[i]):", p)

# Pruebas: certificado válido, la identidad no cuenta y un grafo asimétrico agota las 6! = 720 opciones
assert p == (0, 2, 1) and verificar(triangulo, p)
assert not verificar(triangulo, (0, 1, 2))
asimetrico = matriz(6, [(0, 1), (1, 2), (2, 3), (3, 4), (5, 1), (5, 2)])
assert buscar(asimetrico) is None
print("Pruebas OK")
```

Salida al ejecutarlo:

```text
Simetría del plano (zona i -> zona p[i]): (0, 2, 1)
Pruebas OK
```

## c1 · NP-completo

**Clasificación:** NP-completo · **Algoritmo:** DPLL / retroceso con poda · **¿Decidible?:** Decidible · **Estado:** Problema de decisión

**Computabilidad** (pegar en el primer recuadro):

```text
Sí hay un procedimiento efectivo: hay 2^n asignaciones finitas. DPLL siempre termina porque cada llamada fija al menos una variable (profundidad <= n) y prueba los dos valores de la variable elegida. La asignación (horario candidato) es un certificado y la comprobación cláusula por cláusula es polinomial. Es NP-completo: está en NP y 3SAT se reduce a este problema con la identidad (Cook-Levin).
```

**Complejidad** (pegar en el segundo recuadro):

```text
Entrada: n variables y m cláusulas de hasta k literales. Verificar: O(m·k). Fuerza bruta: 2^n asignaciones, O(2^n·m·k). DPLL: árbol de <= 2^(n+1) nodos y O(n·m·k) por nodo, O(2^n·n·m·k) en el peor caso, con espacio O(n·m·k). Cada decisión extra duplica las posibilidades (3 -> 8; 60 -> unos 10^18). La instancia es 2-CNF, un caso que está en P, pero el problema general es NP-completo.
```

**Código** (pegar en el recuadro de código):

```python
from itertools import product


def verificar(clausulas, asig):
    """Comprobación independiente: cada cláusula necesita un literal verdadero. O(m·k)."""
    return all(any(asig[abs(l)] == (l > 0) for l in c) for c in clausulas)


def simplificar(clausulas, lit):
    """Fija lit = verdadero: quita las cláusulas que ya se cumplen y borra el literal opuesto."""
    return [[l for l in c if l != -lit] for c in clausulas if lit not in c]


def dpll(clausulas, asig=None):
    """DPLL: propagación unitaria + literal puro + ramificación. Peor caso O(2ⁿ·n·m·k)."""
    asig = dict(asig or {})
    unit = next((c[0] for c in clausulas if len(c) == 1), None)
    while unit is not None:
        asig[abs(unit)] = unit > 0
        clausulas = simplificar(clausulas, unit)
        unit = next((c[0] for c in clausulas if len(c) == 1), None)
    if any(len(c) == 0 for c in clausulas):
        return None
    literales = {l for c in clausulas for l in c}
    for l in literales:
        if -l not in literales:
            asig[abs(l)] = l > 0
            clausulas = simplificar(clausulas, l)
    if not clausulas:
        return asig
    x = abs(clausulas[0][0])
    for lit in (x, -x):
        r = dpll(simplificar(clausulas, lit), {**asig, x: lit > 0})
        if r is not None:
            return r
    return None


def resolver(clausulas, n):
    r = dpll(clausulas)
    return None if r is None else {i: r.get(i, False) for i in range(1, n + 1)}


# Entrada: x1, x2, x3 (decisiones vehículo-franja) y las reglas (x1 o no x2) y (x2 o x3)
n, reglas = 3, [[1, -2], [2, 3]]
horario = resolver(reglas, n)
print("Horario candidato:", horario, "| posibilidades con", n, "decisiones:", 2 ** n)

# Pruebas: el verificador acepta el horario, DPLL coincide con fuerza bruta y detecta una fórmula sin solución
assert horario == {1: True, 2: False, 3: True} and verificar(reglas, horario)
assert not verificar(reglas, {1: False, 2: True, 3: False})
insatisfacible = [[a * 1, b * 2, c * 3] for a in (1, -1) for b in (1, -1) for c in (1, -1)]
assert resolver(insatisfacible, 3) is None
assert not any(verificar(insatisfacible, dict(zip((1, 2, 3), v))) for v in product((True, False), repeat=3))
tres_cnf = [[1, 2, 3], [-1, -2, 4], [-3, -4, 5], [2, 4, -5], [-1, 3, 5]]
assert verificar(tres_cnf, resolver(tres_cnf, 5))
print("Pruebas OK")
```

Salida al ejecutarlo:

```text
Horario candidato: {1: True, 2: False, 3: True} | posibilidades con 3 decisiones: 8
Pruebas OK
```

## c2 · NP-completo

**Clasificación:** NP-completo · **Algoritmo:** Backtracking / enumerar permutaciones · **¿Decidible?:** Decidible · **Estado:** Problema de decisión

**Computabilidad** (pegar en el primer recuadro):

```text
Sí hay un procedimiento efectivo: revisar los (n-1)! recorridos que salen de la Planta y vuelven. Termina porque son finitos. Un recorrido es un certificado verificable en O(n). La pregunta es de decisión (¿existe un recorrido con costo <= L?), distinta de pedir el recorrido más corto. Es NP-completo: HAM-CYCLE se reduce a TSP-DEC con pesos 1 y 2 y L = n.
```

**Complejidad** (pegar en el segundo recuadro):

```text
Entrada: n centros y una matriz n×n de distancias. Verificar: O(n). Enumeración: (n-1)! recorridos por O(n), O(n!·n) en tiempo y O(n) en espacio. Held-Karp (optimización): O(n²·2^n) en tiempo y O(n·2^n) en espacio. Resultado: Planta -> Quito -> Guayaquil -> Planta = 15 km <= 20. Con 20 centros la enumeración tardaría miles de años.
```

**Código** (pegar en el recuadro de código):

```python
from itertools import permutations


def costo(dist, ruta):
    return sum(dist[ruta[i]][ruta[i + 1]] for i in range(len(ruta) - 1))


def verificar(dist, L, ruta):
    """Visita cada centro una vez, vuelve a la salida y cuesta <= L. O(n)."""
    n = len(dist)
    return (len(ruta) == n + 1 and ruta[0] == ruta[-1] == 0
            and sorted(ruta[:-1]) == list(range(n)) and costo(dist, ruta) <= L)


def buscar(dist, L):
    """Pregunta de DECISIÓN: ¿existe un recorrido con costo <= L? Prueba los (n-1)! órdenes: O(n!·n)."""
    n = len(dist)
    for orden in permutations(range(1, n)):
        ruta = (0,) + orden + (0,)
        if costo(dist, ruta) <= L:
            return ruta
    return None


# Entrada: matriz de distancias (km) y presupuesto L del expediente
centros = ["Planta", "Quito", "Guayaquil"]
dist = [[0, 4, 8], [4, 0, 3], [8, 3, 0]]
L = 20
ruta = buscar(dist, L)
print("Recorrido:", " -> ".join(centros[i] for i in ruta), "| costo:", costo(dist, ruta), "km <=", L)

# Pruebas: recorrido verificado, presupuesto insuficiente y diferencia con la pregunta de optimización
assert ruta == (0, 1, 2, 0) and costo(dist, ruta) == 15 and verificar(dist, L, ruta)
assert buscar(dist, 14) is None
assert not verificar(dist, L, (0, 1, 0))  # no visita Guayaquil
mas_barato = min(costo(dist, (0,) + o + (0,)) for o in permutations(range(1, 3)))
assert mas_barato == 15  # el óptimo responde otra pregunta: ¿cuál es el recorrido más corto?
print("Pruebas OK")
```

Salida al ejecutarlo:

```text
Recorrido: Planta -> Quito -> Guayaquil -> Planta | costo: 15 km <= 20
Pruebas OK
```

## c3 · NP-completo

**Clasificación:** NP-completo · **Algoritmo:** Backtracking / ramificación · **¿Decidible?:** Decidible · **Estado:** Problema de decisión

**Computabilidad** (pegar en el primer recuadro):

```text
Sí hay un procedimiento efectivo: ramificar sobre un corredor sin cubrir (u, v), porque toda selección válida contiene a u o a v. Termina porque cada rama usa un equipo y la profundidad es <= k. La selección es un certificado y el verificador separado es polinomial. Es NP-completo: INDEPENDENT-SET se reduce a VERTEX-COVER con k = |V| - j.
```

**Complejidad** (pegar en el segundo recuadro):

```text
Entrada: V zonas, E corredores y k en binario. Verificar: O(V + E). Ramificación: <= 2^(k+1) - 1 nodos y O(V + E) por nodo, O(2^k·(V + E)) en tiempo y O(k·(V + E)) en espacio. Por subconjuntos: O(2^V·(V + E)). La 2-aproximación es O(V + E) pero puede usar el doble de equipos. Resultado: {B} con k = 1.
```

**Código** (pegar en el recuadro de código):

```python
def verificar(corredores, k, S):
    """Verificador separado: |S| <= k y cada corredor tiene un equipo en un extremo. O(V + E)."""
    zonas = {z for c in corredores for z in c}
    return len(S) <= k and set(S) <= zonas and all(u in S or v in S for u, v in corredores)


def ramificar(corredores, k):
    """Toma un corredor sin cubrir (u, v): toda solución contiene a u o a v. Tiempo O(2^k·(V + E))."""
    if not corredores:
        return set()
    if k == 0:
        return None
    u, v = corredores[0]
    for z in (u, v):
        resto = [c for c in corredores if z not in c]
        r = ramificar(resto, k - 1)
        if r is not None:
            return r | {z}
    return None


# Entrada: corredores entre zonas y k equipos de inspección
corredores = [("A", "B"), ("B", "C")]
k = 1
S = ramificar(corredores, k)
print(f"¿Bastan {k} equipo(s)?", S is not None, "| selección:", S)

# Pruebas: certificado {B}, k = 0 sin solución, selección que no cubre y un caso que exige k + 1
assert S == {"B"} and verificar(corredores, k, S)
assert ramificar(corredores, 0) is None
assert not verificar(corredores, 1, {"A"})
pares = [(f"a{i}", f"b{i}") for i in range(5)]
assert ramificar(pares, 4) is None and verificar(pares, 5, ramificar(pares, 5))
print("Pruebas OK")
```

Salida al ejecutarlo:

```text
¿Bastan 1 equipo(s)? True | selección: {'B'}
Pruebas OK
```
