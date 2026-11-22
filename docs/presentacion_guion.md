# Presentación final (8–10 min) · Integra: Jessica

| Min | Quién | Contenido |
|---|---|---|
| 0:00–1:00 | Jessica | Contexto LOGISTPULSE y regla P ⊆ NP, NPC ⊆ NP |
| 1:00–4:00 | Camila | Autómatas: estados, transiciones, demo de Multiple Run en JFLAP (1 válida, 1 inválida) |
| 4:00–7:00 | Luis | Ruta de la planta (Dijkstra, 11 m, empate con la Figura 5) + FEFO / reposición |
| 7:00–9:30 | Jessica | Un caso de complejidad (c2 TSP: reducción HAM→TSP, n! vs Held–Karp vs heurística) + parada |
| 9:30–10:00 | Todos | Conclusiones y límites |

## Camila · 1:00–4:00

### Diapositiva 1 · Estados y transiciones en LOGISTPULSE (1:00–1:45)

**En pantalla**

- Tres Autómatas Finitos Deterministas (AFD): **pedido**, **reserva** y **orden de compra**
- Desde cada estado y ante cada evento existe **una única transición**
- Cadena vacía rechazada ($q_0 \notin F$)

**Qué decir**

En la Fase A modelamos el ciclo de vida operativo de LOGISTPULSE —pedido, reserva y orden de compra— utilizando Autómatas Finitos Deterministas. Elegimos un AFD porque las reglas de negocio en logística no admiten ambigüedad: desde cada estado y ante cada evento del alfabeto existe una única transición posible. Si una secuencia cumple las reglas y termina en un estado de aceptación, el autómata la acepta; si no, la rechaza. Por ejemplo, la cadena vacía siempre se rechaza porque el estado inicial no es final.

### Diapositiva 2 · Demo de Multiple Run en JFLAP (1:45–2:45)

**En pantalla**

- [Captura de Multiple Run del pedido](../jflap/capturas/pedido_multiple_run.png)
- Cadena válida: **`criedn`** → **Accept**
- Validación 100 % coherente entre JFLAP y las pruebas en Python

**Qué decir**

Para comprobar que el modelo teórico coincide exactamente con el código, probamos los tres autómatas en JFLAP usando Multiple Run. En esta captura del autómata de pedido cargamos todo el conjunto de cadenas de prueba, válidas e inválidas, y verificamos que cada resultado coincidiera con lo esperado. Por ejemplo, la secuencia válida `criedn` recorre el flujo completo hasta un estado de aceptación, mientras que las secuencias incompletas o fuera de orden se rechazan automáticamente.

### Diapositiva 3 · Caso clave `crix` (decisión A6) y complejidad (2:45–4:00)

**En pantalla**

- Cadena inválida: **`crix`** → **Reject**
- **Decisión A6:** un pedido **no se puede cancelar** después de iniciar el *picking*
- Complejidad de evaluación: tiempo **$O(n)$** · espacio auxiliar **$O(1)$**

**Qué decir**

El caso más claro de cómo el autómata protege las reglas del negocio es la cadena inválida `crix`. Los primeros eventos avanzan el pedido con normalidad hasta que inicia el proceso de picking; justo ahí llega el evento `x`, que representa un intento de cancelación. Según nuestra decisión A6, un pedido no se puede cancelar después de haber iniciado el picking. Al ser un AFD, no existe transición válida con `x` hacia un estado de aceptación, por lo que JFLAP marca `crix` como Reject. Finalmente, evaluar cualquier cadena de longitud $n$ toma tiempo lineal $O(n)$ y espacio auxiliar constante $O(1)$. Ahora Luis continúa con la ruta de la planta y el inventario.

## Luis · 4:00–7:00

### Diapositiva 1 · Ruta del robot en la planta (4:00–5:05)

**En pantalla**

- [Diagrama de la planta y rutas óptimas](diagramas/planta_ruta.png)
- Dijkstra · R → B → A → E → D · **11 m**
- BFS · R → A → E → D · **3 tramos y 12 m**

**Qué decir**

Para calcular el recorrido del robot, representamos la planta como un grafo con siete zonas y once pasillos bidireccionales. Cada pasillo tiene un peso que indica su longitud en metros. El robot parte de Recepción y debe llegar a Despacho.

Usamos Dijkstra porque queremos recorrer la menor distancia total y todos los pesos son no negativos. El programa devuelve la ruta por B, A y Empaque, con un costo de 11 metros. La ruta de la Figura 5 también pasa por Picking y cuesta los mismos 11 metros. Las dos son óptimas.

BFS encuentra un recorrido de tres tramos que suma 12 metros. Su objetivo es minimizar los tramos. Para el robot, nos interesa minimizar los metros. Si bloqueamos Empaque, Despacho queda aislado porque su único acceso pasa por esa zona.

### Diapositiva 2 · FEFO y selección de lotes (5:05–6:05)

**En pantalla**

Pedido de **80 unidades de leche**.

| Lote | Unidades tomadas | Unidades pendientes |
|---|---:|---:|
| L-001 | 30 | 50 |
| L-002 | 25 | 25 |
| L-003 | 25 | 0 |

**Qué decir**

FEFO decide de qué lotes sacar las unidades del pedido. Primero revisamos que cada lote corresponda al producto solicitado, tenga stock y venza después del día de la reserva. Después ordenamos los lotes por vencimiento. Si dos vencen el mismo día, usamos primero el de menor código.

Para el pedido de 80 unidades, tomamos 30 del primer lote, 25 del segundo y las últimas 25 del tercero. Si pedimos 200 y solo hay 155 elegibles, la política configurada determina cómo seguir. Podemos reservar 155 y dejar 45 pendientes, rechazar el pedido o dejarlo en espera de reposición.

### Diapositiva 3 · Cuándo y cuánto reponer (6:05–7:00)

**En pantalla**

- Posición de inventario · **18 + 10 − 5 = 23**
- Mínimo de **30** y objetivo de **50** unidades
- Sugerencia · **50 − 23 = 27 unidades**
- Después de registrar la orden · **0 unidades adicionales sugeridas**

**Qué decir**

Para decidir cuánto reponer, sumamos lo que hay en bodega y lo que ya está pedido al proveedor, y restamos lo reservado. En este ejemplo, la posición es 18 más 10 menos 5, es decir, 23. El mínimo es 30. Como estamos por debajo, se activa la reposición.

El objetivo es 50, así que se sugieren 27 unidades. Cuando se registra la orden, esas unidades pasan a contar como pendientes de recibir. Si los demás datos siguen iguales, la posición sube a 50 y el siguiente cálculo devuelve cero. Así evitamos duplicar la orden.

## Jessica · 0:00–1:00 y 7:00–10:00

### Diapositiva 1 · LOGISTPULSE y la regla de las clases (0:00–1:00)

**En pantalla**

- LOGISTPULSE: pedidos, bodega, planta y **10 correos** de empleados
- P ⊆ NP · NP-completo ⊆ NP · ¿P = NP? **abierto**

**Qué decir**

LOGISTPULSE es una empresa de logística. Modelamos sus procesos con autómatas, sus rutas con grafos y su inventario con FEFO, y clasificamos diez problemas que nos llegaron por correo. Una regla antes de empezar: P está dentro de NP, y los NP-completos también están dentro de NP. "NP" no significa "no polinomial", y nadie ha demostrado que P sea distinto de NP. Ahora Camila presenta los autómatas.

### Diapositiva 2 · c2: ¿hay un recorrido dentro del presupuesto? (7:00–8:15)

**En pantalla**

- Planta → Quito → Guayaquil → Planta = **15 km ≤ 20** (verificar: O(n))
- Decisión ("¿existe uno ≤ L?") ≠ optimización ("¿cuál es el más corto?")
- HAM-CYCLE ≤p TSP-DEC: arista → 1, no arista → 2, L = n

**Qué decir**

Jorge pregunta si existe al menos un recorrido que visite todos los centros, vuelva a la Planta y no pase de 20 kilómetros. Es una pregunta de decisión: la respuesta es sí, con un recorrido de 15 kilómetros. Comprobar un recorrido propuesto es rápido: se suman n distancias. Encontrarlo es lo difícil. Para mostrar que es NP-completo, transformamos el problema del ciclo hamiltoniano: cada arista del grafo vale 1, cada par sin arista vale 2, y el presupuesto es n. Hay un recorrido de costo n si y solo si el grafo tiene un ciclo hamiltoniano.

### Diapositiva 3 · Decidible no es lo mismo que rápido (8:15–9:30)

**En pantalla**

| Centros | Revisar todos los recorridos |
|---:|---|
| 10 | 0,46 s |
| 20 | unos 4 800 años |

- Held–Karp: 14 centros en 0,13 s, pero sigue siendo exponencial
- Vecino más cercano: 13 frente al óptimo 6 (rápido, sin garantía)
- "¿Este programa terminará?": **indecidible** (problema de la parada)

**Qué decir**

Con pocos centros, revisar todos los recorridos es instantáneo. Pero con 20 centros tardaría unos 4 800 años. El problema sigue siendo decidible: la respuesta llegaría, solo que demasiado tarde. Held–Karp mejora mucho, pero sigue siendo exponencial, y una heurística como el vecino más cercano es rápida pero puede dar 13 cuando el óptimo es 6. Distinto es preguntar si un programa cualquiera terminará: ahí no existe ningún algoritmo, por mucho tiempo que le demos. Eso es el problema de la parada.

### Cierre · Conclusiones y límites (9:30–10:00)

**Qué decir**

Tres ideas para cerrar. Primero, cada respuesta está respaldada por código y 146 pruebas, pero vale para los datos del expediente. Segundo, que una instancia sea fácil no cambia la clase del problema. Tercero, decidible no significa rápido. Gracias.
