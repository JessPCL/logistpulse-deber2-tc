"""Arma docs/simulador/RESPUESTAS_SIMULADOR.md: lo que se pega en el simulador, caso por caso.

Para cada correo: las 4 selecciones (coinciden con la autocorrección del simulador), los textos de
computabilidad y complejidad, y un programa AUTOCONTENIDO (entrada + solución + pruebas), porque el
simulador pide "entrada, solución y al menos una prueba" en el campo de código.
Antes de escribir el documento, ejecuta los 10 programas: si alguno falla, no escribe nada.

Uso:  python scripts/armar_simulador.py
"""

import subprocess
import sys

import _bootstrap  # noqa: F401
from _bootstrap import RAIZ

CARPETA = RAIZ / "docs" / "simulador"

CASOS = [
    ("p1", "P", "BFS", "Problema de decisión",
     "Sí existe un procedimiento efectivo: BFS desde Durán sobre los tramos habilitados. Termina porque cada zona "
     "entra a la cola a lo sumo una vez y cada tramo se revisa una vez; si la cola se vacía sin llegar a Norte, la "
     "respuesta es No. Es un problema de decisión (¿existe ruta?) y el camino encontrado sirve como evidencia.",
     "Entrada: grafo dirigido con V zonas y E tramos (lista de conexiones). Tiempo O(V + E): cada zona se encola "
     "una vez y cada tramo se examina una vez. Espacio O(V) para la cola y los padres, más O(V + E) para la lista "
     "de adyacencia. Es polinomial, por eso el problema está en P."),
    ("p2", "P", "Dijkstra", "Problema de optimización",
     "Dijkstra es un procedimiento efectivo cuando los tiempos son no negativos, y aquí lo son. Termina porque cada "
     "nodo se cierra una sola vez y cada tramo se relaja un número finito de veces; las entradas viejas del heap se "
     "descartan. El sistema debe guardar pred[v] (predecesor de cada nodo) para reconstruir la ruta. Con tiempos "
     "negativos no sería correcto y habría que usar Bellman-Ford.",
     "Entrada: V centros y E tramos con tiempos >= 0. Con heap binario y listas de adyacencia hay a lo sumo E + 1 "
     "inserciones y extracciones de costo O(log V): tiempo O((V + E) log V) y espacio O(V + E). Es polinomial, en P. "
     "Resultado: Quito -> Latacunga -> Guayaquil = 8, que empata con Quito -> Ambato -> Guayaquil = 8."),
    ("p3", "P", "Edmonds–Karp", "Problema de optimización",
     "Edmonds-Karp es un procedimiento efectivo: busca con BFS un camino con capacidad residual y lo satura. "
     "Termina porque cada aumento suma al menos 1 camión (capacidades enteras) y además hace a lo sumo O(V·E) "
     "aumentos, sin depender del valor de las capacidades. El registro muestra cómo cambian los tramos usados y "
     "disponibles. Resultado: 10 camiones/día, aunque lo que sale de la Planta suma 12.",
     "Entrada: V nodos y E tramos con capacidades enteras. Hay a lo sumo O(V·E) aumentos y cada BFS cuesta O(E): "
     "tiempo O(V·E²) y espacio O(V + E) para la red residual. Es polinomial e independiente del tamaño de las "
     "capacidades, por eso está en P."),
    ("n1", "NP", "Búsqueda exhaustiva de permutaciones", "Problema de decisión",
     "Sí hay un procedimiento efectivo: probar las n! correspondencias y verificar cada una. Termina porque las "
     "permutaciones de n nodos son finitas. Si la respuesta es Sí, la correspondencia es un certificado que se "
     "revisa en tiempo polinomial; por eso el problema está en NP. No afirmamos que sea NP-completo ni que se "
     "conozca un algoritmo polinomial.",
     "Entrada: dos matrices de adyacencia n×n. Verificar un certificado: O(n²) comparaciones. Búsqueda "
     "exhaustiva: hasta n! permutaciones por O(n²) cada una, O(n!·n²) en tiempo y O(n) de espacio extra. Con 3 "
     "nodos son 6 candidatas; con 12 ya son unos 479 millones."),
    ("n2", "NP", "Prueba por división exhaustiva", "Problema de decisión",
     "Sí hay un procedimiento efectivo: probar d = 2, ..., B. Termina porque el rango es finito. El divisor d es un "
     "certificado y se verifica con una sola división (N mod d = 0 y 2 <= d <= B), en tiempo polinomial en los bits "
     "de N. Por eso el problema está en NP. La búsqueda y la validación son rutinas separadas.",
     "Entrada: N y B en binario, con log2 N y log2 B bits. Verificar: una división, polinomial en log N. Buscar: "
     "hasta B divisiones, O(B·M(log N)). Como B = 2^(log2 B), la búsqueda es exponencial en el tamaño de la entrada "
     "(pseudo-polinomial): cada bit extra de B duplica el trabajo. Resultado: N = 91 (7 bits), B = 10, d = 7."),
    ("n3", "NP", "Búsqueda exhaustiva con exponenciación modular", "Problema de decisión",
     "Sí hay un procedimiento efectivo: probar x = 0, ..., B. Termina porque hay B + 1 candidatos. El exponente x "
     "es un certificado y se verifica con exponenciación rápida en tiempo polinomial en log p + log B; por eso "
     "está en NP. La búsqueda y el verificador están separados y solo se usan los parámetros ficticios.",
     "Entrada: p, g, h y B en binario. Verificar: O(log x) multiplicaciones modulares. Búsqueda lineal: O(B) "
     "multiplicaciones, exponencial en los bits de B. Baby-step giant-step baja a O(raíz de B) en tiempo y "
     "espacio, pero sigue siendo exponencial en bits. Resultado: x = 6, porque 5^6 = 8 (mod 23)."),
    ("n4", "NP", "Permutaciones + verificación de adyacencia", "Problema de decisión",
     "Sí hay un procedimiento efectivo: probar las permutaciones distintas de la identidad y verificar cada una. "
     "Termina porque son finitas; si ninguna sirve, el programa responde No después de agotarlas todas (para el No "
     "no se conoce un certificado corto). Si la respuesta es Sí, la permutación es un certificado verificable en "
     "tiempo polinomial: el problema está en NP.",
     "Entrada: matriz de adyacencia n×n. Verificar una permutación: O(n²). Búsqueda: hasta n! permutaciones, "
     "O(n!·n²) en tiempo y O(n) de espacio extra. En el triángulo se encuentra (0, 2, 1); un grafo asimétrico de "
     "6 vértices obliga a revisar las 720 permutaciones."),
    ("c1", "NP-completo", "DPLL / retroceso con poda", "Problema de decisión",
     "Sí hay un procedimiento efectivo: hay 2^n asignaciones finitas. DPLL siempre termina porque cada llamada fija "
     "al menos una variable (profundidad <= n) y prueba los dos valores de la variable elegida. La asignación "
     "(horario candidato) es un certificado y la comprobación cláusula por cláusula es polinomial. Es NP-completo: "
     "está en NP y 3SAT se reduce a este problema con la identidad (Cook-Levin).",
     "Entrada: n variables y m cláusulas de hasta k literales. Verificar: O(m·k). Fuerza bruta: 2^n asignaciones, "
     "O(2^n·m·k). DPLL: árbol de <= 2^(n+1) nodos y O(n·m·k) por nodo, O(2^n·n·m·k) en el peor caso, con espacio "
     "O(n·m·k). Cada decisión extra duplica las posibilidades (3 -> 8; 60 -> unos 10^18). La instancia es 2-CNF, un "
     "caso que está en P, pero el problema general es NP-completo."),
    ("c2", "NP-completo", "Backtracking / enumerar permutaciones", "Problema de decisión",
     "Sí hay un procedimiento efectivo: revisar los (n-1)! recorridos que salen de la Planta y vuelven. Termina "
     "porque son finitos. Un recorrido es un certificado verificable en O(n). La pregunta es de decisión (¿existe un "
     "recorrido con costo <= L?), distinta de pedir el recorrido más corto. Es NP-completo: HAM-CYCLE se reduce a "
     "TSP-DEC con pesos 1 y 2 y L = n.",
     "Entrada: n centros y una matriz n×n de distancias. Verificar: O(n). Enumeración: (n-1)! recorridos por O(n), "
     "O(n!·n) en tiempo y O(n) en espacio. Held-Karp (optimización): O(n²·2^n) en tiempo y O(n·2^n) en espacio. "
     "Resultado: Planta -> Quito -> Guayaquil -> Planta = 15 km <= 20. Con 20 centros la enumeración tardaría miles "
     "de años."),
    ("c3", "NP-completo", "Backtracking / ramificación", "Problema de decisión",
     "Sí hay un procedimiento efectivo: ramificar sobre un corredor sin cubrir (u, v), porque toda selección válida "
     "contiene a u o a v. Termina porque cada rama usa un equipo y la profundidad es <= k. La selección es un "
     "certificado y el verificador separado es polinomial. Es NP-completo: INDEPENDENT-SET se reduce a VERTEX-COVER "
     "con k = |V| - j.",
     "Entrada: V zonas, E corredores y k en binario. Verificar: O(V + E). Ramificación: <= 2^(k+1) - 1 nodos y "
     "O(V + E) por nodo, O(2^k·(V + E)) en tiempo y O(k·(V + E)) en espacio. Por subconjuntos: O(2^V·(V + E)). "
     "La 2-aproximación es O(V + E) pero puede usar el doble de equipos. Resultado: {B} con k = 1."),
]


def comprobar(caso: str) -> str:
    r = subprocess.run([sys.executable, "-I", str(CARPETA / f"{caso}.py")], capture_output=True, text=True,
                       encoding="utf-8")
    if r.returncode != 0 or "Pruebas OK" not in r.stdout:
        raise SystemExit(f"ERROR: docs/simulador/{caso}.py no pasa sus pruebas:\n{r.stdout}{r.stderr}")
    return r.stdout.strip()


def main() -> None:
    salidas = {c[0]: comprobar(c[0]) for c in CASOS}  # primero se ejecutan los 10 programas
    L = ["# Respuestas para pegar en el simulador", "",
         "Se genera con `python scripts/armar_simulador.py`, que antes ejecuta los 10 programas y comprueba que "
         "pasan sus pruebas.", "",
         "**Cómo llenarlo:** abre el .html **siempre en el mismo navegador**, sin modo incógnito (el avance se "
         "guarda en ese navegador). Escribe tu nombre y tu código y entra. Para cada correo: elige las 4 opciones, "
         "pega los dos textos y el código, y presiona **Enviar respuesta**. Al final usa **Descargar .txt**.", "",
         "| Correo | Clasificación | Algoritmo | ¿Decidible? | Estado del caso |", "|---|---|---|---|---|"]
    L += [f"| {c[0]} | {c[1]} | {c[2]} | Decidible | {c[3]} |" for c in CASOS]
    for caso, cls, algo, estado, comp, compl in CASOS:
        codigo = (CARPETA / f"{caso}.py").read_text(encoding="utf-8").rstrip()
        L += ["", f"## {caso} · {cls}", "",
              f"**Clasificación:** {cls} · **Algoritmo:** {algo} · **¿Decidible?:** Decidible · **Estado:** {estado}", "",
              "**Computabilidad** (pegar en el primer recuadro):", "", "```text", comp, "```", "",
              "**Complejidad** (pegar en el segundo recuadro):", "", "```text", compl, "```", "",
              "**Código** (pegar en el recuadro de código):", "", "```python", codigo, "```", "",
              "Salida al ejecutarlo:", "", "```text", salidas[caso], "```"]
    (CARPETA / "RESPUESTAS_SIMULADOR.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"OK docs/simulador/RESPUESTAS_SIMULADOR.md (10 programas ejecutados, todos con 'Pruebas OK')")


if __name__ == "__main__":
    main()
