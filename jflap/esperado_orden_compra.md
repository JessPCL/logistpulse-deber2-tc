# Resultados esperados en JFLAP · OrdenCompra

Archivo: `orden_compra.jff` · entradas: `entradas_orden_compra.txt`

Σ: `s` = solicitar_aprobacion, `a` = aprobar, `r` = rechazar, `e` = emitir_orden, `p` = recibir_parte, `c` = recibir_completa, `f` = completar_recepcion

| Cadena | Eventos | Esperado | Por qué |
|---|---|---|---|
| `saec` | solicitar_aprobacion → aprobar → emitir_orden → recibir_completa | Accept | Borrador→En aprobacion→Aprobada→Enviada→Recibida (recepción completa) |
| `saepf` | solicitar_aprobacion → aprobar → emitir_orden → recibir_parte → completar_recepcion | Accept | Una recepción parcial y luego se completa |
| `saeppf` | solicitar_aprobacion → aprobar → emitir_orden → recibir_parte → recibir_parte → completar_recepcion | Accept | Dos recepciones parciales (bucle) y luego se completa |
| `sr` | solicitar_aprobacion → rechazar | Accept | Orden rechazada: cierre legítimo |
| `sre` | solicitar_aprobacion → rechazar → emitir_orden | Reject | [ENUNCIADO] Rechazada→Enviada: un estado final rechazado no habilita emisión |
| `e` | emitir_orden | Reject | Emitir sin solicitar ni aprobar |
| `sac` | solicitar_aprobacion → aprobar → recibir_completa | Reject | Recibir mercadería de una orden aprobada pero nunca emitida |
| `saep` | solicitar_aprobacion → aprobar → emitir_orden → recibir_parte | Reject | Termina en Recepcion parcial ∉ F: falta completar la recepción |
| `saecp` | solicitar_aprobacion → aprobar → emitir_orden → recibir_completa → recibir_parte | Reject | Recibir después de Recibida |
