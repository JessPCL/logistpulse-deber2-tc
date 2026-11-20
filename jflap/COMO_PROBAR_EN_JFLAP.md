# Cómo probar los autómatas en JFLAP (evidencia de la Fase A)

Archivos: `pedido.jff`, `reserva.jff`, `orden_compra.jff`, generados desde `logistpulse/automatas/definiciones.py` con `python scripts/generar_jflap.py`.
`tests/test_jflap.py` comprueba que cada .jff es **exactamente** el autómata que prueban las pruebas de Python.

## 1. Abrir
1. Descarga **JFLAP 7.1** desde https://www.jflap.org (necesita Java). Ejecuta `java -jar JFLAP7.1.jar`.
2. `File → Open…` → `jflap/pedido.jff`. Si los estados quedan amontonados, puedes moverlos con el mouse (no cambia el autómata).

## 2. Comprobar que es determinista
`Test → Highlight Nondeterminism`: no debe resaltarse ningún estado. **Captura**: `jflap/capturas/<automata>_determinismo.png`.

## 3. Multiple Run (la evidencia principal)
1. `Input → Multiple Run`.
2. Botón **Load Inputs** → elige `jflap/entradas_<automata>.txt` (una cadena por línea).
3. Botón **Run Inputs**. La columna *Result* debe coincidir con `jflap/esperado_<automata>.md` (Accept / Reject).
4. **Captura** de la tabla completa: `jflap/capturas/<automata>_multiple_run.png`.

> La cadena vacía ε no va en el .txt. Pruébala con `Input → Fast Run` dejando el campo vacío: el resultado debe ser **Reject** (el estado inicial no es final). Si tu versión de JFLAP no deja enviar una entrada vacía, menciona que ε está cubierta por `tests/test_automatas.py::test_cadena_vacia_rechazada`.

## 4. Traza paso a paso (para el informe y la exposición)
`Input → Step by State` con una cadena válida y otra inválida de cada autómata (por ejemplo `criedn` y `crid` en pedido). Avanza con **Step** hasta el final. **Capturas**: `jflap/capturas/<automata>_traza_valida.png` y `_traza_invalida.png`.

## 5. Símbolos
| Autómata | Σ |
|---|---|
| Pedido | c confirmar · r reservar · i iniciar_picking · e empacar · d despachar · n entregar · x cancelar |
| Reserva | v validar · s sin_stock · c confirmar · p picking · x cancelar · t vence_plazo |
| Orden de compra | s solicitar_aprobacion · a aprobar · r rechazar · e emitir_orden · p recibir_parte · c recibir_completa · f completar_recepcion |

Si se modifica un autómata, se cambia **en Python** y se regenera (`python scripts/generar_jflap.py`). No se edita el .jff a mano, porque entonces dejaría de coincidir con las pruebas.
