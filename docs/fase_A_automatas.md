# Fase A · Autómatas de pedido, reserva y orden de compra

**Responsable:** Camila Granda · **Rúbrica:** 2,0 pts (tres modelos correctos; estados, eventos, transiciones aceptadas y no válidas; evidencia JFLAP).

---

## 1. Decisiones generales de modelado

Para garantizar coherencia entre la definición formal, los diagramas, los archivos JFLAP y el código en `logistpulse/automatas/definiciones.py`, se aplican criterios uniformes a los tres autómatas finitos deterministas (AFD):

1. **Criterio único para estados finales $F$ (Decisión A1):** Se definen como estados finales todos los **estados terminales legítimos**, es decir, aquellos donde el ciclo operativo cierra de manera válida. En las Figuras 3 y 4 del enunciado, *Rechazada* aparece marcada como estado final, mientras que en la Figura 2 *Cancelado* no lleva doble círculo. Para mantener un criterio único en los tres procesos, *Cancelado* se incluye en $F$ para el pedido (la variante estricta donde solo *Entregado* es final queda disponible en `PEDIDO_ESTRICTO`).
2. **Símbolos de un carácter (Decisión A2):** Cada evento operativo se codifica con un único símbolo en $\Sigma$ para que la herramienta *Multiple Run* de JFLAP procese una cadena por línea carácter a carácter.
3. **Función de transición total mediante estado sumidero `ERROR` (Decisión A3):** En los diagramas y en JFLAP solo se dibujan las transiciones válidas ($\delta$ parcial); cualquier transición no declarada para un par $(q, a) \in Q \times \Sigma$ se dirige al estado sumidero no final y absorbente `ERROR`, donde $\delta(\text{ERROR}, a) = \text{ERROR}$ para todo $a \in \Sigma$. De este modo, $\delta: Q \times \Sigma \to Q$ es formalmente una función total.
4. **Separación entre rechazo del modelo y dato mal formado (Decisión A4):** Si una cadena contiene un símbolo $a \notin \Sigma$, no pertenece a $\Sigma^*$ y el código lanza `ValueError` en lugar de reportar un rechazo del autómata.
5. **Eventos completados y cierre definitivo (Decisiones A5–A8):**
   * **A5 (Pedido):** La flecha *liberar/cancelar* desde *Reservado* se modela como el evento único `x` (*cancelar*), entendiendo que cancelar un pedido reservado libera automáticamente su reserva.
   * **A6 (Pedido):** No existe transición de cancelación desde *Preparación*, *Empacado* ni *Despachado*, respetando la Figura 2: una vez iniciado el picking, el pedido no se cancela.
   * **A7 (Orden de compra):** Se incorpora el bucle $\delta(\text{Recepcion parcial}, p) = \text{Recepcion parcial}$ para admitir múltiples entregas parciales antes de completar la recepción.
   * **A8 (Todos):** Ningún estado final posee transiciones de salida; un proceso cerrado no puede reabrirse.

---

## 2. Autómata 1: Ciclo de vida del pedido (`M_Pedido`)

### 2.1 Definición formal y significado operativo

$$M_{\text{Pedido}} = (Q, \Sigma, \delta, q_0, F)$$

* **$Q$ (Estados):** `Borrador`, `Confirmado`, `Reservado`, `Preparacion`, `Empacado`, `Despachado`, `Entregado`, `Cancelado`, `ERROR`.
  * `Borrador`: pedido registrado inicialmente, aún sin confirmación comercial.
  * `Confirmado`: pedido validado y aprobado para reservar inventario.
  * `Reservado`: inventario asignado al pedido.
  * `Preparacion`: operarios ejecutando el picking de los productos.
  * `Empacado`: productos embalados y listos para despacho.
  * `Despachado`: pedido entregado al transporte rumbo al cliente.
  * `Entregado`: pedido recibido por el cliente (cierre exitoso).
  * `Cancelado`: pedido anulado antes de iniciar el picking (cierre legítimo sin entrega).
  * `ERROR`: estado sumidero no final que absorbe cualquier secuencia con una transición inválida.
* **$\Sigma$ (Eventos):**
  * `c` = *confirmar* (aprueba el borrador).
  * `r` = *reservar* (asigna inventario al pedido confirmado).
  * `i` = *iniciar_picking* (comienza la preparación física).
  * `e` = *empacar* (finaliza el embalaje).
  * `d` = *despachar* (libera el pedido a transporte).
  * `n` = *entregar* (confirma recepción del cliente).
  * `x` = *cancelar* (anula el pedido; desde *Reservado* implica liberar la reserva).
* **$q_0$:** `Borrador`.
* **$F$:** `{Entregado, Cancelado}`.

### 2.2 Tabla de transiciones ($\delta$ total)

| Estado | `c` (confirmar) | `r` (reservar) | `i` (iniciar_picking) | `e` (empacar) | `d` (despachar) | `n` (entregar) | `x` (cancelar) |
|---|---|---|---|---|---|---|---|
| → Borrador | Confirmado | ERROR | ERROR | ERROR | ERROR | ERROR | Cancelado |
| Confirmado | ERROR | Reservado | ERROR | ERROR | ERROR | ERROR | Cancelado |
| Reservado | ERROR | ERROR | Preparacion | ERROR | ERROR | ERROR | Cancelado |
| Preparacion | ERROR | ERROR | ERROR | Empacado | ERROR | ERROR | ERROR |
| Empacado | ERROR | ERROR | ERROR | ERROR | Despachado | ERROR | ERROR |
| Despachado | ERROR | ERROR | ERROR | ERROR | ERROR | Entregado | ERROR |
| Entregado * | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |
| Cancelado * | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |
| ERROR (sumidero) | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |

*Diagrama:* `docs/diagramas/afd_pedido.png` · *Archivo JFLAP:* `jflap/pedido.jff`.

### 2.3 Secuencias válidas e inválidas

| Tipo | Cadena | Secuencia de eventos / estados | Resultado | Transición clave que acepta o rechaza |
|---|---|---|---|---|
| Válida 1 (enunciado) | `criedn` | Borrador → Confirmado → Reservado → Preparacion → Empacado → Despachado → Entregado | **Aceptada** | $\delta(\text{Despachado}, n) = \text{Entregado} \in F$. |
| Válida 2 | `crx` | Borrador → Confirmado → Reservado → Cancelado | **Aceptada** | $\delta(\text{Reservado}, x) = \text{Cancelado} \in F$ (cierre legítimo con liberación de reserva). |
| Inválida 1 (enunciado) | `d` | Borrador $\xrightarrow{d}$ ERROR | **Rechazada** | $\delta(\text{Borrador}, d) = \text{ERROR}$: no se puede despachar sin confirmar, reservar, preparar y empacar. |
| Inválida 2 (Decisión A6) | `crix` | Borrador → Confirmado → Reservado → Preparacion $\xrightarrow{x}$ ERROR | **Rechazada** | $\delta(\text{Preparacion}, x) = \text{ERROR}$: una vez iniciado el picking, el pedido no admite cancelación. |

---

## 3. Autómata 2: Ciclo de vida de la reserva (`M_Reserva`)

### 3.1 Definición formal y significado operativo

$$M_{\text{Reserva}} = (Q, \Sigma, \delta, q_0, F)$$

* **$Q$ (Estados):** `Solicitada`, `Validada`, `Reservada`, `Consumida`, `Liberada`, `Expirada`, `Rechazada`, `ERROR`.
  * `Solicitada`: petición de reserva ingresada al sistema.
  * `Validada`: existencia de stock confirmada preliminarmente.
  * `Reservada`: unidades bloqueadas formalmente para el pedido.
  * `Consumida`: inventario retirado durante el picking (cierre exitoso).
  * `Liberada`: inventario devuelto a disponible por cancelación (cierre legítimo).
  * `Expirada`: inventario liberado por vencimiento de plazo (cierre legítimo).
  * `Rechazada`: solicitud denegada por falta de stock (cierre legítimo).
  * `ERROR`: estado sumidero absorbente.
* **$\Sigma$ (Eventos):**
  * `v` = *validar* (verifica disponibilidad de stock).
  * `s` = *sin_stock* (rechaza la solicitud por inventario insuficiente).
  * `c` = *confirmar* (bloquea efectivamente las unidades).
  * `p` = *picking* (consume el inventario reservado).
  * `x` = *cancelar* (libera una reserva activa).
  * `t` = *vence_plazo* (caduca la reserva por tiempo).
* **$q_0$:** `Solicitada`.
* **$F$:** `{Consumida, Liberada, Expirada, Rechazada}`.

### 3.2 Tabla de transiciones ($\delta$ total)

| Estado | `v` (validar) | `s` (sin_stock) | `c` (confirmar) | `p` (picking) | `x` (cancelar) | `t` (vence_plazo) |
|---|---|---|---|---|---|---|
| → Solicitada | Validada | Rechazada | ERROR | ERROR | ERROR | ERROR |
| Validada | ERROR | ERROR | Reservada | ERROR | ERROR | ERROR |
| Reservada | ERROR | ERROR | ERROR | Consumida | Liberada | Expirada |
| Consumida * | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |
| Liberada * | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |
| Expirada * | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |
| Rechazada * | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |
| ERROR (sumidero) | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |

*Diagrama:* `docs/diagramas/afd_reserva.png` · *Archivo JFLAP:* `jflap/reserva.jff`.

### 3.3 Secuencias válidas e inválidas

| Tipo | Cadena | Secuencia de eventos / estados | Resultado | Transición clave que acepta o rechaza |
|---|---|---|---|---|
| Válida 1 (enunciado) | `vcp` | Solicitada → Validada → Reservada → Consumida | **Aceptada** | $\delta(\text{Reservada}, p) = \text{Consumida} \in F$. |
| Válida 2 | `vct` | Solicitada → Validada → Reservada → Expirada | **Aceptada** | $\delta(\text{Reservada}, t) = \text{Expirada} \in F$. |
| Inválida 1 | `vp` | Solicitada → Validada $\xrightarrow{p}$ ERROR | **Rechazada** | $\delta(\text{Validada}, p) = \text{ERROR}$: impide consumir una reserva que nunca fue confirmada. |
| Inválida 2 | `sv` | Solicitada → Rechazada $\xrightarrow{v}$ ERROR | **Rechazada** | $\delta(\text{Rechazada}, v) = \text{ERROR}$: una reserva rechazada es final y no puede validarse después. |

---

## 4. Autómata 3: Ciclo de vida de la orden de compra (`M_OrdenCompra`)

### 4.1 Definición formal y significado operativo

$$M_{\text{OrdenCompra}} = (Q, \Sigma, \delta, q_0, F)$$

* **$Q$ (Estados):** `Borrador`, `En aprobacion`, `Aprobada`, `Rechazada`, `Enviada`, `Recepcion parcial`, `Recibida`, `ERROR`.
  * `Borrador`: orden creada antes de someterse a revisión.
  * `En aprobacion`: orden pendiente de autorización administrativa.
  * `Aprobada`: orden autorizada, lista para emitirse al proveedor.
  * `Rechazada`: orden denegada en aprobación (cierre legítimo).
  * `Enviada`: orden emitida al proveedor, en espera de mercancía.
  * `Recepcion parcial`: parte de la mercancía recibida; restan entregas pendientes.
  * `Recibida`: totalidad de la orden ingresada en bodega (cierre exitoso).
  * `ERROR`: estado sumidero absorbente.
* **$\Sigma$ (Eventos):**
  * `s` = *solicitar_aprobacion* (envía el borrador a revisión).
  * `a` = *aprobar* (autoriza la compra).
  * `r` = *rechazar* (deniega la compra).
  * `e` = *emitir_orden* (despacha la orden al proveedor).
  * `p` = *recibir_parte* (registra un ingreso parcial).
  * `c` = *recibir_completa* (registra el ingreso total en una sola entrega).
  * `f` = *completar_recepcion* (cierra la recepción tras uno o más ingresos parciales).
* **$q_0$:** `Borrador`.
* **$F$:** `{Rechazada, Recibida}`.

### 4.2 Tabla de transiciones ($\delta$ total)

| Estado | `s` (solicitar_aprobacion) | `a` (aprobar) | `r` (rechazar) | `e` (emitir_orden) | `p` (recibir_parte) | `c` (recibir_completa) | `f` (completar_recepcion) |
|---|---|---|---|---|---|---|---|
| → Borrador | En aprobacion | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |
| En aprobacion | ERROR | Aprobada | Rechazada | ERROR | ERROR | ERROR | ERROR |
| Aprobada | ERROR | ERROR | ERROR | Enviada | ERROR | ERROR | ERROR |
| Rechazada * | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |
| Enviada | ERROR | ERROR | ERROR | ERROR | Recepcion parcial | Recibida | ERROR |
| Recepcion parcial | ERROR | ERROR | ERROR | ERROR | Recepcion parcial | ERROR | Recibida |
| Recibida * | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |
| ERROR (sumidero) | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |

*Diagrama:* `docs/diagramas/afd_orden_compra.png` · *Archivo JFLAP:* `jflap/orden_compra.jff`.

### 4.3 Secuencias válidas e inválidas

| Tipo | Cadena | Secuencia de eventos / estados | Resultado | Transición clave que acepta o rechaza |
|---|---|---|---|---|
| Válida 1 | `saec` | Borrador → En aprobacion → Aprobada → Enviada → Recibida | **Aceptada** | $\delta(\text{Enviada}, c) = \text{Recibida} \in F$. |
| Válida 2 (Decisión A7) | `saeppf` | Borrador → En aprobacion → Aprobada → Enviada → Recepcion parcial → Recepcion parcial → Recibida | **Aceptada** | El bucle $\delta(\text{Recepcion parcial}, p) = \text{Recepcion parcial}$ permite múltiples parciales y $\delta(\text{Recepcion parcial}, f) = \text{Recibida} \in F$ cierra la orden. |
| Inválida 1 (enunciado) | `sre` | Borrador → En aprobacion → Rechazada $\xrightarrow{e}$ ERROR | **Rechazada** | $\delta(\text{Rechazada}, e) = \text{ERROR}$: un estado final rechazado no habilita la emisión de la orden. |
| Inválida 2 | `saep` | Borrador → En aprobacion → Aprobada → Enviada → Recepcion parcial | **Rechazada** | Termina en `Recepcion parcial` $\notin F$: la orden quedó incompleta sin cerrar la recepción. |

---

## 5. Prevención de transiciones imposibles

Al modelar cada proceso como un AFD determinista con función de transición total hacia `ERROR`, el sistema impone un contrato estricto sobre el orden de los eventos:

* **No se puede consumir una reserva no confirmada:** el evento `p` (*picking*) solo tiene transición válida desde `Reservada`. Si ocurre en `Solicitada` o `Validada`, el autómata transita a `ERROR` y rechaza la operación.
* **No se puede despachar un pedido sin preparación:** el evento `d` (*despachar*) solo es válido desde `Empacado`; cualquier intento desde `Borrador`, `Confirmado` o `Reservado` cae en `ERROR`.
* **No se pueden reabrir procesos cerrados:** ningún estado en $F$ tiene transiciones válidas de salida (Decisión A8), bloqueando operaciones ilegales como emitir una orden `Rechazada` o cancelar un pedido `Entregado`.

---

## 6. Validación, pruebas y complejidad

La verificación se realizó en dos niveles complementarios y trazables:

1. **Pruebas en JFLAP 7.1:** Los archivos `jflap/pedido.jff`, `jflap/reserva.jff` y `jflap/orden_compra.jff` se generaron directamente desde el código Python (`python scripts/generar_jflap.py`). Para cada autómata se ejecutó:
   * *Test → Highlight Nondeterminism* (confirmando determinismo): `jflap/capturas/<automata>_determinismo.png`.
   * *Input → Multiple Run* cargando `jflap/entradas_<automata>.txt` y contrastando contra `jflap/esperado_<automata>.md`: `jflap/capturas/<automata>_multiple_run.png`.
   * *Input → Step by State* sobre una cadena válida y una inválida: `jflap/capturas/<automata>_traza_valida.png` y `jflap/capturas/<automata>_traza_invalida.png`.
   * La cadena vacía $\varepsilon$ se rechaza porque $q_0 \notin F$ en los tres modelos (cubierto por `tests/test_automatas.py::test_cadena_vacia_rechazada`).
2. **Pruebas automatizadas en Python (`unittest`):**
   * `tests/test_automatas.py` verifica las secuencias válidas, inválidas, cadena vacía, estados finales y el rechazo de símbolos fuera de $\Sigma$ (`ValueError`).
   * `tests/test_jflap.py` comprueba estructuralmente que cada archivo `.jff` coincide exactamente en estados, estado inicial, estados finales y transiciones con el AFD definido en `logistpulse/automatas/definiciones.py`.
3. **Complejidad:** Evaluar una cadena de longitud $n$ en cualquiera de los tres AFD toma tiempo $O(n)$ (exactamente una consulta a la tabla de transiciones por símbolo) y espacio auxiliar $O(1)$, respaldado empíricamente por `tests/test_complejidad.py::test_afd_un_paso_por_simbolo`.