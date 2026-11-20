# Resultados esperados en JFLAP · Reserva

Archivo: `reserva.jff` · entradas: `entradas_reserva.txt`

Σ: `v` = validar, `s` = sin_stock, `c` = confirmar, `p` = picking, `x` = cancelar, `t` = vence_plazo

| Cadena | Eventos | Esperado | Por qué |
|---|---|---|---|
| `vcp` | validar → confirmar → picking | Accept | [ENUNCIADO] Solicitada→Validada→Reservada→Consumida |
| `s` | sin_stock | Accept | Sin stock: Solicitada→Rechazada |
| `vcx` | validar → confirmar → cancelar | Accept | Reserva cancelada: Reservada→Liberada |
| `vct` | validar → confirmar → vence_plazo | Accept | Vence el plazo: Reservada→Expirada |
| `vp` | validar → picking | Reject | Consumir una reserva que nunca fue confirmada: δ(Validada,p) no existe |
| `p` | picking | Reject | Picking directo desde Solicitada |
| `vcpx` | validar → confirmar → picking → cancelar | Reject | Cancelar una reserva ya consumida |
| `vc` | validar → confirmar | Reject | Termina en Reservada ∉ F: la reserva sigue abierta |
| `sv` | sin_stock → validar | Reject | Validar una solicitud ya rechazada |
