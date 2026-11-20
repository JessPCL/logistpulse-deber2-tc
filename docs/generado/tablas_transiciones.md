# Tablas de transiciones (Fase A)

_Generadas desde `logistpulse/automatas/definiciones.py`._

## Pedido

Ciclo de vida del pedido (Figura 2).

```text
M_Pedido = (Q, Σ, δ, q0, F)
Q  = {Borrador, Confirmado, Reservado, Preparacion, Empacado, Despachado, Entregado, Cancelado} ∪ {ERROR}
Σ  = {c=confirmar, r=reservar, i=iniciar_picking, e=empacar, d=despachar, n=entregar, x=cancelar}
q0 = Borrador
F  = {Entregado, Cancelado}
|δ declarada| = 9 transiciones (el resto va a ERROR)
```

| Estado | c (confirmar) | r (reservar) | i (iniciar_picking) | e (empacar) | d (despachar) | n (entregar) | x (cancelar) |
|---|---|---|---|---|---|---|---|
| → Borrador | Confirmado | ∅ | ∅ | ∅ | ∅ | ∅ | Cancelado |
| Confirmado | ∅ | Reservado | ∅ | ∅ | ∅ | ∅ | Cancelado |
| Reservado | ∅ | ∅ | Preparacion | ∅ | ∅ | ∅ | Cancelado |
| Preparacion | ∅ | ∅ | ∅ | Empacado | ∅ | ∅ | ∅ |
| Empacado | ∅ | ∅ | ∅ | ∅ | Despachado | ∅ | ∅ |
| Despachado | ∅ | ∅ | ∅ | ∅ | ∅ | Entregado | ∅ |
| Entregado * | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| Cancelado * | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| ERROR (sumidero) | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |

→ = estado inicial · * = estado final · ∅ = va al sumidero ERROR

Diagrama: `docs/diagramas/afd_pedido.png` · JFLAP: `jflap/pedido.jff`

## Reserva

Ciclo de vida de una reserva de inventario (Figura 3).

```text
M_Reserva = (Q, Σ, δ, q0, F)
Q  = {Solicitada, Validada, Reservada, Consumida, Liberada, Expirada, Rechazada} ∪ {ERROR}
Σ  = {v=validar, s=sin_stock, c=confirmar, p=picking, x=cancelar, t=vence_plazo}
q0 = Solicitada
F  = {Consumida, Liberada, Expirada, Rechazada}
|δ declarada| = 6 transiciones (el resto va a ERROR)
```

| Estado | v (validar) | s (sin_stock) | c (confirmar) | p (picking) | x (cancelar) | t (vence_plazo) |
|---|---|---|---|---|---|---|
| → Solicitada | Validada | Rechazada | ∅ | ∅ | ∅ | ∅ |
| Validada | ∅ | ∅ | Reservada | ∅ | ∅ | ∅ |
| Reservada | ∅ | ∅ | ∅ | Consumida | Liberada | Expirada |
| Consumida * | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| Liberada * | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| Expirada * | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| Rechazada * | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| ERROR (sumidero) | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |

→ = estado inicial · * = estado final · ∅ = va al sumidero ERROR

Diagrama: `docs/diagramas/afd_reserva.png` · JFLAP: `jflap/reserva.jff`

## OrdenCompra

Ciclo de vida de una orden de compra (Figura 4). Se agrega el bucle δ(Recepcion parcial, p) = Recepcion parcial para admitir varias entregas parciales.

```text
M_OrdenCompra = (Q, Σ, δ, q0, F)
Q  = {Borrador, En aprobacion, Aprobada, Rechazada, Enviada, Recepcion parcial, Recibida} ∪ {ERROR}
Σ  = {s=solicitar_aprobacion, a=aprobar, r=rechazar, e=emitir_orden, p=recibir_parte, c=recibir_completa, f=completar_recepcion}
q0 = Borrador
F  = {Rechazada, Recibida}
|δ declarada| = 8 transiciones (el resto va a ERROR)
```

| Estado | s (solicitar_aprobacion) | a (aprobar) | r (rechazar) | e (emitir_orden) | p (recibir_parte) | c (recibir_completa) | f (completar_recepcion) |
|---|---|---|---|---|---|---|---|
| → Borrador | En aprobacion | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| En aprobacion | ∅ | Aprobada | Rechazada | ∅ | ∅ | ∅ | ∅ |
| Aprobada | ∅ | ∅ | ∅ | Enviada | ∅ | ∅ | ∅ |
| Rechazada * | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| Enviada | ∅ | ∅ | ∅ | ∅ | Recepcion parcial | Recibida | ∅ |
| Recepcion parcial | ∅ | ∅ | ∅ | ∅ | Recepcion parcial | ∅ | Recibida |
| Recibida * | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| ERROR (sumidero) | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR | ERROR |

→ = estado inicial · * = estado final · ∅ = va al sumidero ERROR

Diagrama: `docs/diagramas/afd_orden_compra.png` · JFLAP: `jflap/orden_compra.jff`
