# Qué pide cada correo y dónde lo respondemos

Léelo antes de redactar tu ficha. Cada correo del simulador pide varias cosas concretas, y la ficha tiene que cubrir **todas**.

## 1. El simulador tiene dos textos por caso
| Texto | Dónde se ve | Para qué sirve |
|---|---|---|
| **Tarjeta del caso** (asunto, resumen, algoritmo sugerido) | La lista de la bandeja y la cabecera del caso | Orientarse |
| **Cuerpo del correo** ("Buenos días, ...") | Al abrir el correo | **Es la solicitud real.** Si no coincide con la tarjeta, manda el cuerpo |

Hay dos casos donde no coinciden y ya están anotados:
- **c1 (H6):** la tarjeta dice "3-CNF", el correo habla de reglas en general y los datos son 2-CNF.
- **c3 (H7):** la tarjeta habla de "almacenes" y de "zona cubierta propia o vecina"; el correo pide **equipos de inspección** que cubran **corredores**.

## 2. De dónde salen los números (los datos son iguales para todos)
Los datos están **escritos dentro del archivo .html**. No hay nada aleatorio: el navegador solo guarda tu nombre y tus respuestas. Si a alguien le sale distinto, es porque tiene **otra versión del archivo**. El nuestro pesa 44 212 bytes.

En cada caso hay cuatro lugares donde mirar:
1. **"Abrir mapa"**, solo en p1, p2, p3 y c3. Es el dibujo del grafo: las flechas indican el sentido y los números sobre las flechas son los pesos (tiempos o capacidades).
2. **"Datos del caso"**: una tabla con columnas *Campo 1, Campo 2, Campo 3*. En p2 y p3 significan **origen, destino y peso**.
3. **"Ver tablas SQL"**: la misma tabla con columnas *dato, valor, descripción*. Los nombres de las columnas **no** corresponden a su contenido: en p2, `dato` = origen, `valor` = destino y `descripción` = tiempo.
4. **El código de ejemplo del caso.** En n1 y c2, la tabla no trae los valores concretos ("3 nodos, 2 enlaces", "matriz simétrica"); las matrices exactas están en ese código.

Todo eso ya está copiado en `data/casos_simulador.json`, que es lo que lee nuestro programa.

**p2 en concreto:** "el proveedor cambió los tiempos" es solo la historia del correo. Los tiempos de la tabla **ya son los nuevos**, y no hay una tabla anterior con la cual comparar. Son tramos con sentido: Quito→Latacunga 2, Quito→Ambato 5, Latacunga→Guayaquil 6 y Ambato→Guayaquil 3.

## 3. Lista por correo
"Salida" se refiere a `python -m logistpulse casos`. Marca cada punto en tu ficha.

### p1 · Daniela Paredes · ¿Puede llegar el envío a la zona Norte? · ficha: **terminada**
- [x] Responder Sí/No → **Sí**: Durán → Quito → Norte (salida, línea 1).
- [x] Procedimiento para comprobarlo en **toda** la red → BFS (ficha p1, §5).
- [x] Programa que se pueda ejecutar con **una lista de conexiones** → `python -m logistpulse p1 ARCHIVO ORIGEN DESTINO`.
- [x] Un ejemplo **con** ruta y otro **sin** ruta → `data/ejemplos/p1_con_ruta.txt` y `p1_sin_ruta.txt`, más sus pruebas.

### p2 · Marco Cedeño · Ruta mínima entre centros · ficha: **Luis**
- [x] Recorrido sugerido y su costo total en tiempo → Quito → Latacunga → Guayaquil = **8**. Hay **empate** con Quito → Ambato → Guayaquil = 8 (H3): la ficha debe decirlo.
- [x] Qué información conservar para reconstruir la ruta → el **predecesor** de cada nodo, `pred[v]` (salida, línea 1).
- [x] Código y una prueba pequeña → `casos/p2_ruta_minima.py`, `TestP2`.
- [ ] (Ficha) "Si consideras otra técnica, justifica sus supuestos" → Dijkstra exige pesos ≥ 0, y aquí se cumple. BFS no sirve porque minimiza tramos y no tiempo (H2). Bellman–Ford acepta pesos negativos pero cuesta O(V·E). Se incluye el contraejemplo con peso negativo que pide la tarea.

### p3 · Luis Vaca · Máximo de camiones hacia clientes · ficha: **Luis**
- [x] Máximo que puede despacharse → **10 camiones/día**.
- [x] Registro reproducible de cómo se actualizan los tramos usados y disponibles → "Registro de actualización de tramos" en la salida.
- [x] Algoritmo en código → Edmonds–Karp, `casos/p3_flujo_maximo.py`.
- [ ] (Ficha) Cuánto crece el trabajo con más nodos y conexiones → O(V·E²), con los conteos de la salida y H13.
- [x] No asumir que la suma de lo que sale de Planta es el flujo → sale 12, pero llegan 10 (corte mínimo, H4).

### n1 · Elena Ruiz · Comparar topologías equivalentes · ficha: **Camila**
- [x] ¿Existe una correspondencia uno a uno que preserve todas las conexiones? → **Sí**.
- [x] La correspondencia como evidencia revisable → π = (1, 0, 2) más el verificador.
- [x] Programa que pruebe el caso del expediente → `casos/n1_isomorfismo.py`, pruebas.
- [ ] (Ficha) Cómo escala al crecer el número de nodos → hasta n! permutaciones; el verificador es O(n²).

### n2 · Andrés Molina · ¿Tiene N un factor en este intervalo? · ficha: **Camila**
- [x] Rutina que encuentre un divisor y otra **separada** que valide uno propuesto → `buscar` y `verificar`.
- [x] Resultado para el N y el B de la consola → N = 91, B = 10: **d = 7**.
- [ ] (Ficha) Comparar el costo de buscar con el de verificar, con los números **en binario** → buscar es O(B), exponencial en bits (H9, H14); verificar es una división.
- [x] No modificar ni publicar el identificador → solo se usan los datos de prueba.

### n3 · Paola León · ¿Existe exponente x que produzca h? · ficha: **Camila**
- [x] Separar la búsqueda del verificador → búsqueda lineal y BSGS frente a `verificar` (exponenciación rápida).
- [x] Código y prueba reproducible → **x = 6** (5⁶ ≡ 8 mod 23).
- [ ] (Ficha) Costo de cada etapa → buscar es O(B), exponencial en bits; BSGS es O(√B); verificar es O(log x) multiplicaciones.
- [x] Usar solo los parámetros ficticios de la estación.

### n4 · Santiago Jaramillo · ¿La topología tiene una simetría? · ficha: **Camila**
- [x] Una simetría que **no** sea la identidad y conserve las adyacencias → π = (0, 2, 1) en el triángulo.
- [x] La permutación como certificado y un verificador independiente → sí; además, el verificador rechaza la identidad.
- [ ] (Ficha) Si no hay simetría, cómo concluye el programa que agotó las opciones → recorre las n! permutaciones (720 con 6 vértices, H11).

### c1 · Mónica Ruiz · ¿Hay una asignación que cumpla todas las reglas? · ficha: **terminada**
- [x] Horario candidato → x1 = verdadero, x2 = falso, x3 = verdadero.
- [x] Comprobación independiente cláusula por cláusula → "Regla 1 ... se cumple porque x1 es verdadero" (salida).
- [x] Implementación de búsqueda → DPLL, con fuerza bruta como referencia.
- [x] Cómo cambia el número de posibilidades con la cantidad de decisiones → 2ⁿ (ficha c1, §0 y §3).
- [x] Si no existe → el programa dice que hay que renegociar la ventana de despacho.

### c2 · Jorge Tapia · Recorrido dentro del presupuesto · ficha: **terminada**
- [x] Un recorrido válido, su costo y una verificación ejecutable → Planta → Quito → Guayaquil → Planta = **15 km ≤ 20**.
- [x] Distinguir la pregunta de decisión de pedir el recorrido más barato → ficha c2, §2 y §5.
- [x] Crecimiento al incorporar más centros → (n−1)! y Held–Karp, con tiempos medidos.

### c3 · Carla Núñez · ¿Bastan k equipos para cubrir los corredores? · ficha: **terminada**
- [x] Selección de no más de k zonas que cubra todos los corredores → **{B}** con k = 1.
- [x] La selección como certificado y un verificador **separado** → `verificar`.
- [x] Búsqueda que resuelva el expediente → ramificación.
- [x] Cómo varía el esfuerzo cuando crece el mapa → O(2ᵏ·(V + E)), con tiempos medidos.

Los puntos marcados con **(Ficha)** ya tienen su cálculo en el código. Solo falta **explicarlos por escrito** en la ficha de su responsable.
