# Presentación final (8–10 min) · Integra: Jessica

| Min | Quién | Contenido |
|---|---|---|
| 0:00–1:00 | Jessica | Contexto LOGISTPULSE y regla P ⊆ NP, NPC ⊆ NP |
| 1:00–4:00 | Camila | Autómatas: estados, transiciones, demo de Multiple Run en JFLAP (1 válida, 1 inválida) |
| 4:00–7:00 | Luis | Ruta de la planta (Dijkstra, 11 m, empate con la Figura 5) + FEFO / reposición |
| 7:00–9:30 | Jessica | Un caso de complejidad (c2 TSP: reducción HAM→TSP, n! vs Held–Karp vs heurística) + parada |
| 9:30–10:00 | Todos | Conclusiones y límites |

> Cada integrante pega aquí su guion de 3 minutos (lo genera su prompt).

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
