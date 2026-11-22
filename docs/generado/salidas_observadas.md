# Salidas observadas

_Generado el 2026-11-22 ejecutando `python -m logistpulse`. Reproducible: mismos datos, mismo orden de desempate._

## automatas

```text

==============================================================================
FASE A · Autómata Pedido
==============================================================================
M_Pedido = (Q, Σ, δ, q0, F)
Q  = {Borrador, Confirmado, Reservado, Preparacion, Empacado, Despachado, Entregado, Cancelado} ∪ {ERROR}
Σ  = {c=confirmar, r=reservar, i=iniciar_picking, e=empacar, d=despachar, n=entregar, x=cancelar}
q0 = Borrador
F  = {Entregado, Cancelado}
|δ declarada| = 9 transiciones (el resto va a ERROR)

[OK] 'criedn' [confirmar → reservar → iniciar_picking → empacar → despachar → entregar] -> ACEPTA · Entregado ∈ F.
     [ENUNCIADO] Borrador→Confirmado→Reservado→Preparacion→Empacado→Despachado→Entregado
[OK] 'x' [cancelar] -> ACEPTA · Cancelado ∈ F.
     Cancelación desde Borrador: cierre legítimo
[OK] 'crx' [confirmar → reservar → cancelar] -> ACEPTA · Cancelado ∈ F.
     Se cancela un pedido reservado: libera la reserva y cierra en Cancelado
[OK] 'd' [despachar] -> RECHAZA · Paso 1: δ(Borrador, d='despachar') no está definida -> sumidero ERROR.
     [ENUNCIADO] Borrador→Despachado: δ(Borrador,d) no existe; no se despacha sin confirmar, reservar, preparar y empacar
[OK] 'crid' [confirmar → reservar → iniciar_picking → despachar] -> RECHAZA · Paso 4: δ(Preparacion, d='despachar') no está definida -> sumidero ERROR.
     Despachar desde Preparacion sin empacar: δ(Preparacion,d) no existe
[OK] 'crix' [confirmar → reservar → iniciar_picking → cancelar] -> RECHAZA · Paso 4: δ(Preparacion, x='cancelar') no está definida -> sumidero ERROR.
     Cancelar durante el picking no está permitido en el modelo: δ(Preparacion,x) no existe
[OK] 'cried' [confirmar → reservar → iniciar_picking → empacar → despachar] -> RECHAZA · Despachado ∉ F: la secuencia termina en un estado no final (proceso incompleto).
     Termina en Despachado ∉ F: falta la entrega
[OK] 'criednd' [confirmar → reservar → iniciar_picking → empacar → despachar → entregar → despachar] -> RECHAZA · Paso 7: δ(Entregado, d='despachar') no está definida -> sumidero ERROR.
     Evento después del estado final Entregado
[OK] 'ε' [ε] -> RECHAZA · Borrador ∉ F: la secuencia termina en un estado no final (proceso incompleto).
     Cadena vacía ε: Borrador ∉ F

==============================================================================
FASE A · Autómata Reserva
==============================================================================
M_Reserva = (Q, Σ, δ, q0, F)
Q  = {Solicitada, Validada, Reservada, Consumida, Liberada, Expirada, Rechazada} ∪ {ERROR}
Σ  = {v=validar, s=sin_stock, c=confirmar, p=picking, x=cancelar, t=vence_plazo}
q0 = Solicitada
F  = {Consumida, Liberada, Expirada, Rechazada}
|δ declarada| = 6 transiciones (el resto va a ERROR)

[OK] 'vcp' [validar → confirmar → picking] -> ACEPTA · Consumida ∈ F.
     [ENUNCIADO] Solicitada→Validada→Reservada→Consumida
[OK] 's' [sin_stock] -> ACEPTA · Rechazada ∈ F.
     Sin stock: Solicitada→Rechazada
[OK] 'vcx' [validar → confirmar → cancelar] -> ACEPTA · Liberada ∈ F.
     Reserva cancelada: Reservada→Liberada
[OK] 'vct' [validar → confirmar → vence_plazo] -> ACEPTA · Expirada ∈ F.
     Vence el plazo: Reservada→Expirada
[OK] 'vp' [validar → picking] -> RECHAZA · Paso 2: δ(Validada, p='picking') no está definida -> sumidero ERROR.
     Consumir una reserva que nunca fue confirmada: δ(Validada,p) no existe
[OK] 'p' [picking] -> RECHAZA · Paso 1: δ(Solicitada, p='picking') no está definida -> sumidero ERROR.
     Picking directo desde Solicitada
[OK] 'vcpx' [validar → confirmar → picking → cancelar] -> RECHAZA · Paso 4: δ(Consumida, x='cancelar') no está definida -> sumidero ERROR.
     Cancelar una reserva ya consumida
[OK] 'vc' [validar → confirmar] -> RECHAZA · Reservada ∉ F: la secuencia termina en un estado no final (proceso incompleto).
     Termina en Reservada ∉ F: la reserva sigue abierta
[OK] 'sv' [sin_stock → validar] -> RECHAZA · Paso 2: δ(Rechazada, v='validar') no está definida -> sumidero ERROR.
     Validar una solicitud ya rechazada

==============================================================================
FASE A · Autómata OrdenCompra
==============================================================================
M_OrdenCompra = (Q, Σ, δ, q0, F)
Q  = {Borrador, En aprobacion, Aprobada, Rechazada, Enviada, Recepcion parcial, Recibida} ∪ {ERROR}
Σ  = {s=solicitar_aprobacion, a=aprobar, r=rechazar, e=emitir_orden, p=recibir_parte, c=recibir_completa, f=completar_recepcion}
q0 = Borrador
F  = {Rechazada, Recibida}
|δ declarada| = 8 transiciones (el resto va a ERROR)

[OK] 'saec' [solicitar_aprobacion → aprobar → emitir_orden → recibir_completa] -> ACEPTA · Recibida ∈ F.
     Borrador→En aprobacion→Aprobada→Enviada→Recibida (recepción completa)
[OK] 'saepf' [solicitar_aprobacion → aprobar → emitir_orden → recibir_parte → completar_recepcion] -> ACEPTA · Recibida ∈ F.
     Una recepción parcial y luego se completa
[OK] 'saeppf' [solicitar_aprobacion → aprobar → emitir_orden → recibir_parte → recibir_parte → completar_recepcion] -> ACEPTA · Recibida ∈ F.
     Dos recepciones parciales (bucle) y luego se completa
[OK] 'sr' [solicitar_aprobacion → rechazar] -> ACEPTA · Rechazada ∈ F.
     Orden rechazada: cierre legítimo
[OK] 'sre' [solicitar_aprobacion → rechazar → emitir_orden] -> RECHAZA · Paso 3: δ(Rechazada, e='emitir_orden') no está definida -> sumidero ERROR.
     [ENUNCIADO] Rechazada→Enviada: un estado final rechazado no habilita emisión
[OK] 'e' [emitir_orden] -> RECHAZA · Paso 1: δ(Borrador, e='emitir_orden') no está definida -> sumidero ERROR.
     Emitir sin solicitar ni aprobar
[OK] 'sac' [solicitar_aprobacion → aprobar → recibir_completa] -> RECHAZA · Paso 3: δ(Aprobada, c='recibir_completa') no está definida -> sumidero ERROR.
     Recibir mercadería de una orden aprobada pero nunca emitida
[OK] 'saep' [solicitar_aprobacion → aprobar → emitir_orden → recibir_parte] -> RECHAZA · Recepcion parcial ∉ F: la secuencia termina en un estado no final (proceso incompleto).
     Termina en Recepcion parcial ∉ F: falta completar la recepción
[OK] 'saecp' [solicitar_aprobacion → aprobar → emitir_orden → recibir_completa → recibir_parte] -> RECHAZA · Paso 5: δ(Recibida, p='recibir_parte') no está definida -> sumidero ERROR.
     Recibir después de Recibida
```

## rutas

```text

==============================================================================
FASE B · Planta como grafo ponderado (Dijkstra)
==============================================================================
V = 7, E = 11, dirigido = False, origen = R, destino = D
Traza de Dijkstra (escenario base):
   Extraer R (dist=0)
      relajar R->A: ∞ → 4 (pred[A]=R)
      relajar R->B: ∞ → 2 (pred[B]=R)
   Extraer B (dist=2)
      relajar B->A: 4 → 3 (pred[A]=B)
      relajar B->C: ∞ → 5 (pred[C]=B)
      relajar B->P: ∞ → 9 (pred[P]=B)
   Extraer A (dist=3)
      relajar A->E: ∞ → 8 (pred[E]=A)
      relajar A->P: 9 → 6 (pred[P]=A)
   Extraer C (dist=5)
   Extraer P (dist=6)
   Extraer E (dist=8)
      relajar E->D: ∞ → 11 (pred[D]=E)
   Extraer D (dist=11)
[Base (sin bloqueos)] bloqueados: ninguno -> R → B → A → E → D = 11 m
     Empate: 2 rutas de costo 11: R → B → A → E → D | R → B → A → P → E → D
[Pasillo A bloqueado] bloqueados: A -> R → B → C → E → D = 12 m
     Empate: 2 rutas de costo 12: R → B → C → E → D | R → B → C → P → E → D
[Picking bloqueado] bloqueados: P -> R → B → A → E → D = 11 m
[Empaque bloqueado (D queda aislado)] bloqueados: E -> NO existe ruta (dist = ∞)
BFS (ignora pesos): R → A → E → D = 3 tramos, pero cuesta 12 m > 11 ⇒ con pesos hay que usar Dijkstra
```

## inventario

```text

==============================================================================
FASE C · FEFO (fecha de referencia 2026-11-20)
==============================================================================
LECHE-1L x80 -> COMPLETO · plan [L-001:30, L-002:25, L-003:25] · reservado 80 · pendiente 0
     orden FEFO: ['L-001', 'L-002', 'L-003', 'L-006'] · descartados: L-004 (vencido o vence hoy (2026-11-18)); L-005 (sin cantidad disponible); L-007 (vencido o vence hoy (2026-11-20))
LECHE-1L x200 -> PARCIAL · plan [L-001:30, L-002:25, L-003:40, L-006:60] · reservado 155 · pendiente 45
     orden FEFO: ['L-001', 'L-002', 'L-003', 'L-006'] · descartados: L-004 (vencido o vence hoy (2026-11-18)); L-005 (sin cantidad disponible); L-007 (vencido o vence hoy (2026-11-20))
LECHE-1L x200 -> RECHAZADO · plan [—] · reservado 0 · pendiente 200
     orden FEFO: ['L-001', 'L-002', 'L-003', 'L-006'] · descartados: L-004 (vencido o vence hoy (2026-11-18)); L-005 (sin cantidad disponible); L-007 (vencido o vence hoy (2026-11-20))
LECHE-1L x200 -> EN_ESPERA · plan [—] · reservado 0 · pendiente 200
     orden FEFO: ['L-001', 'L-002', 'L-003', 'L-006'] · descartados: L-004 (vencido o vence hoy (2026-11-18)); L-005 (sin cantidad disponible); L-007 (vencido o vence hoy (2026-11-20))
YOGUR-200G x12 -> COMPLETO · plan [Y-100:12] · reservado 12 · pendiente 0
     orden FEFO: ['Y-100'] · descartados: —

==============================================================================
FASE C · Reposición por punto de pedido
==============================================================================
| SKU | posición | mínimo | objetivo | ¿posición ≤ mínimo? | sugerencia |
|---|---|---|---|---|---|
| SKU-EJ | 23 | 30 | 50 | Sí | 27 |
| LECHE-1L | 75 | 100 | 250 | Sí | 175 |
| YOGUR-200G | 40 | 30 | 60 | No | 0 |
| AGUA-500ML | 280 | 100 | 400 | No | 0 |
| QUESO-500G | -5 | 20 | 40 | Sí | 45 |
| PAN-MOLDE | 30 | 30 | 45 | Sí | 15 |

Anti-duplicado: SKU-EJ sugiere 27; tras emitir esa orden (en_orden += 27) la posición pasa a 50 > mínimo ⇒ nueva sugerencia = 0
```

## casos

```text

==============================================================================
FASE D · P1 · P · ¿Puede llegar el envío a la zona Norte?
==============================================================================
RESPUESTA AL CORREO: Sí, hoy existe ruta Durán → Norte: Durán → Quito → Norte (2 tramos).
Si se cierra Quito→Norte: No existe ruta (BFS agotó la cola).
Verificar camino: True
BFS por niveles:
| Paso | Sale de la cola | Entran (se registra padre) | Cola después |
|---|---|---|---|
| INICIO | — | Durán | Durán |
| 1 | Durán | Quito, Guayaquil | Quito, Guayaquil |
| 2 | Quito | Norte | Guayaquil, Norte |
| 3 | Guayaquil | Sur | Norte, Sur |
| 4 | Norte | **¡destino!** | Sur |

==============================================================================
FASE D · P2 · P · Ruta mínima entre centros de distribución
==============================================================================
RESPUESTA AL CORREO: recorrido sugerido Quito → Latacunga → Guayaquil, tiempo total 8. El sistema debe conservar pred[v] (predecesor) de cada nodo para reconstruir la ruta.
dist desde Quito: {'Ambato': 5, 'Guayaquil': 8, 'Latacunga': 2, 'Quito': 0}
Rutas de costo mínimo (empate): ['Quito → Ambato → Guayaquil', 'Quito → Latacunga → Guayaquil']
Versión de decisión: ¿ruta con costo ≤ 8? True · ≤ 7? False
Peso negativo (S→A 2, S→B 3, B→A −2, A→C 1): Dijkstra da C=3, Bellman–Ford da C=2  ⇒ Dijkstra falla

==============================================================================
FASE D · P3 · P · Máximo de camiones hacia clientes
==============================================================================
RESPUESTA AL CORREO: pueden llegar como máximo 10 camiones/día de Planta a Clientes (la salida de Planta suma 12, pero el cuello de botella deja pasar 10).
Registro de actualización de tramos (usado / disponible):
  Aumento 1: Planta → Quito → Clientes · cuello 4 · total 4
      usar     Planta→Quito           usado 4/7 · disponible 3
      usar     Quito→Clientes         usado 4/4 · disponible 0
  Aumento 2: Planta → Guayaquil → Clientes · cuello 5 · total 9
      usar     Planta→Guayaquil       usado 5/5 · disponible 0
      usar     Guayaquil→Clientes     usado 5/6 · disponible 1
  Aumento 3: Planta → Quito → Guayaquil → Clientes · cuello 1 · total 10
      usar     Planta→Quito           usado 5/7 · disponible 2
      usar     Quito→Guayaquil        usado 1/2 · disponible 1
      usar     Guayaquil→Clientes     usado 6/6 · disponible 0
Flujo final por tramo: {('Planta', 'Quito'): 5, ('Planta', 'Guayaquil'): 5, ('Quito', 'Clientes'): 4, ('Quito', 'Guayaquil'): 1, ('Guayaquil', 'Clientes'): 6}
Verificador (capacidad + conservación) -> valor 10
Corte mínimo S = ['Guayaquil', 'Planta', 'Quito'] · capacidad = 10 = flujo ⇒ óptimo
Versión de decisión: ¿≥ 10? True · ¿≥ 11? False
Trabajo realizado: 3 aumentos (cota V·E = 20) y 29 aristas residuales examinadas (cota (aumentos+1)·2E = 40); V = 4, E = 5

==============================================================================
FASE D · N1 · NP · Comparar topologías equivalentes
==============================================================================
RESPUESTA AL CORREO: Sí, las dos redes tienen la misma estructura; correspondencia (certificado) π = (1, 0, 2)  (nodo i de A ↦ nodo π(i) de B).
Verificador(π) = True · Verificador(identidad) = False
Búsqueda: 3 permutaciones probadas (de 3! = 6 posibles)
C6 vs dos triángulos (mismos grados, no isomorfos): None

==============================================================================
FASE D · N2 · NP · ¿Tiene N un factor en este intervalo?
==============================================================================
RESPUESTA AL CORREO: Sí, N tiene un divisor en el rango: d = 7 (2 ≤ 7 ≤ 10 y 91 mod 7 = 0).
Entrada en binario: N = 1011011₂ (7 bits), B = 1010₂ (4 bits)
BUSCAR: 6 divisiones (crece con el VALOR de B, hasta B−1) · VERIFICAR: 1 división · verificar(d) = True
Con B = 6 -> None (7 queda fuera del rango) · verificar(91, 10, 13) = False

==============================================================================
FASE D · N3 · NP · ¿Existe exponente x que produzca h?
==============================================================================
RESPUESTA AL CORREO: Sí, existe un exponente permitido: x = 6 (5^6 ≡ 8 mod 23, 0 ≤ 6 ≤ 10).
BUSCAR lineal: 6 multiplicaciones · BSGS: x = 6, 5 multiplicaciones
VERIFICAR (cuadrado y multiplicación): 5 multiplicaciones · verificar(x) = True · verificar(x=5) = False
Con B = 5 -> None (el único x ≤ 21 con 5^x ≡ 8 es 6)

==============================================================================
FASE D · N4 · NP · ¿La topología tiene una simetría?
==============================================================================
RESPUESTA AL CORREO: Sí, el plano tiene una simetría real: π = (0, 2, 1) (reasignación distinta de la identidad que mantiene todas las adyacencias).
Verificar(π) = True · verificar(identidad) = False · hallado tras 2 permutaciones
Grafo asimétrico de 6 vértices: None -> 'No' tras AGOTAR 720 = 6! permutaciones

==============================================================================
FASE D · C1 · NP-completo · ¿Hay una asignación que cumpla todas las reglas?
==============================================================================
RESPUESTA AL CORREO: Sí, hay un horario candidato que cumple todas las reglas: x1 = verdadero, x2 = falso, x3 = verdadero (DPLL; comprobación independiente: verificar = True).
Comprobación cláusula por cláusula:
  Regla 1 (x1 ∨ ¬x2): se cumple porque x1 es verdadero
  Regla 2 (x2 ∨ x3): se cumple porque x3 es verdadero
DPLL: 1 nodo(s) del árbol · fuerza bruta (referencia): {1: False, 2: False, 3: True}, probó 2 de 2^3 = 8 asignaciones (crece como 2ⁿ)
La instancia es 2-CNF = True ⇒ 2-SAT lineal -> {1: True, 2: False, 3: True} · verificar = True
3-CNF satisfacible (extra): DPLL -> {1: True, 2: True, 3: False, 4: True, 5: True} · verificar = True
3-CNF con las 8 cláusulas (extra): DPLL -> None · fuerza bruta -> None

==============================================================================
FASE D · C2 · NP-completo · ¿Existe una ruta hamiltoniana dentro del presupuesto?
==============================================================================
RESPUESTA AL CORREO: Sí, existe un recorrido dentro de L = 20 km: Planta → Quito → Guayaquil → Planta = 15 km (verificar = True).
Decisión con L = 14: No (el único tour, salvo sentido, cuesta 15)
Optimización (pregunta distinta, Held–Karp): (0, 2, 1, 0) = 15
Reducción HAM→TSP: C4 -> True · estrella K1,3 -> False
Heurística vs exacto (4 centros): vecino más cercano (0, 1, 2, 3, 0) = 13 · Held–Karp (0, 2, 3, 1, 0) = 6

==============================================================================
FASE D · C3 · NP-completo · ¿Bastan k almacenes para cubrir todas las zonas?
==============================================================================
RESPUESTA AL CORREO: Sí, basta con 1 equipo(s) de inspección (k = 1): selección ['B']; cubre todos los corredores (verificar = True).
verificar({'A'}) = False · con k = 0: None (No)
Estrella de 5 hojas: óptimo = {'centro'} · 2-aproximación = ['centro', 'h0'] (tamaño 2 ≤ 2·1)
Reducción IS→VC: ¿IS de tamaño 2 en A-B-C? ⇔ ¿VC de tamaño 1? -> True
```
