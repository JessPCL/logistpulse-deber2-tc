# Resultados esperados en JFLAP · Pedido

Archivo: `pedido.jff` · entradas: `entradas_pedido.txt`

Σ: `c` = confirmar, `r` = reservar, `i` = iniciar_picking, `e` = empacar, `d` = despachar, `n` = entregar, `x` = cancelar

| Cadena | Eventos | Esperado | Por qué |
|---|---|---|---|
| `criedn` | confirmar → reservar → iniciar_picking → empacar → despachar → entregar | Accept | [ENUNCIADO] Borrador→Confirmado→Reservado→Preparacion→Empacado→Despachado→Entregado |
| `x` | cancelar | Accept | Cancelación desde Borrador: cierre legítimo |
| `crx` | confirmar → reservar → cancelar | Accept | Se cancela un pedido reservado: libera la reserva y cierra en Cancelado |
| `d` | despachar | Reject | [ENUNCIADO] Borrador→Despachado: δ(Borrador,d) no existe; no se despacha sin confirmar, reservar, preparar y empacar |
| `crid` | confirmar → reservar → iniciar_picking → despachar | Reject | Despachar desde Preparacion sin empacar: δ(Preparacion,d) no existe |
| `crix` | confirmar → reservar → iniciar_picking → cancelar | Reject | Cancelar durante el picking no está permitido en el modelo: δ(Preparacion,x) no existe |
| `cried` | confirmar → reservar → iniciar_picking → empacar → despachar | Reject | Termina en Despachado ∉ F: falta la entrega |
| `criednd` | confirmar → reservar → iniciar_picking → empacar → despachar → entregar → despachar | Reject | Evento después del estado final Entregado |
| `ε` | ε (cadena vacía) | Reject | Cadena vacía ε: Borrador ∉ F |
