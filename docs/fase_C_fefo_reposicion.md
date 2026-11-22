# Fase C · Selección FEFO y regla de reposición

**Responsable:** Luis

## 1. Selección de lotes mediante FEFO

FEFO (*First Expired, First Out*) asigna primero las unidades de los lotes elegibles que vencen antes. Un lote es elegible si corresponde al SKU solicitado, tiene unidades disponibles y su fecha de vencimiento es posterior a la fecha de referencia. Según la política del proyecto, un lote que vence el mismo día de la reserva queda excluido. Si dos lotes vencen el mismo día, se elige primero el de menor código en orden alfabético.

La función `seleccionar_fefo`, en `logistpulse/inventario/fefo.py`, recibe los lotes, el SKU, la cantidad solicitada, la fecha de referencia y la política ante falta de stock. Devuelve un plan por lote, la cantidad pendiente y el estado del pedido. El plan indica qué unidades reservar.

```text
SELECCIONAR_FEFO(lotes, sku, cantidad, fecha, política)
    validar cantidad positiva entera, fecha, política y códigos únicos
    candidatos ← lotes del sku con disponible > 0 y vencimiento > fecha
    ordenar candidatos por (vencimiento ascendente, código ascendente)
    pendiente ← cantidad
    plan ← lista vacía

    para cada lote en candidatos
        si pendiente = 0
            salir del recorrido
        tomar ← mínimo(pendiente, disponible del lote)
        agregar (código del lote, tomar) al plan
        pendiente ← pendiente − tomar

    si pendiente = 0
        devolver (plan, 0, COMPLETO)
    si política = parcial
        devolver (plan, pendiente, PARCIAL)
    si política = rechazar
        devolver (lista vacía, cantidad, RECHAZADO)
    devolver (lista vacía, cantidad, EN_ESPERA)
```

La cantidad tomada se limita tanto al stock del lote como al pendiente del pedido. El orden de selección se cumple porque solo se pasa al lote siguiente cuando todavía faltan unidades. El algoritmo termina tras filtrar y ordenar una lista finita. El recorrido se detiene al cubrir el pedido o al agotar los candidatos.

**Complejidad.** Con (L) lotes de entrada, filtrar y recorrer cuesta **O(L)**. El ordenamiento de los candidatos y el ordenamiento del registro de descartes dan un tiempo total de **O(L log L)** en el peor caso. El espacio es **O(L)** por las listas de lotes, candidatos, descartes y el plan que se genera.

### Resultados de la ejecución

Con fecha de referencia del **20 de noviembre de 2026**, el pedido de **80 unidades de LECHE-1L** toma 30 de L-001, 25 de L-002 y 25 de L-003. L-001 y L-002 vencen el 1 de diciembre, así que el código decide el orden entre ambos. Se excluyen L-004 por vencido, L-005 por falta de stock y L-007 porque vence el día de la reserva.

En un pedido separado de **200 unidades** del mismo SKU, los cuatro lotes elegibles suman **155 unidades**. El resultado depende de la política:

| Política | Estado | Unidades asignadas | Unidades pendientes |
|---|---|---:|---:|
| Parcial | `PARCIAL` | 155 | 45 |
| Rechazar | `RECHAZADO` | 0 | 200 |
| Esperar reposición | `EN_ESPERA` | 0 | 200 |

## 2. Reposición por punto de pedido

Para cada SKU se calcula la **posición de inventario** sumando las unidades en bodega y las unidades pendientes de recibir de órdenes de compra abiertas, y restando las unidades ya reservadas. Cuando la posición es menor o igual al mínimo, se sugiere la cantidad necesaria para alcanzar el objetivo. Las cantidades de entrada son enteros no negativos y el objetivo debe ser mayor o igual al mínimo. La posición calculada puede ser negativa.

```text
SUGERIR_REPOSICIÓN(productos)
    para cada producto
        posición ← disponible + en_orden − reservado
        sugerencia ← 0
        si posición ≤ mínimo
            sugerencia ← máximo(0, objetivo − posición)
        emitir (sku, posición, sugerencia)
```

**Ejemplo del enunciado.** Con 18 unidades disponibles, 10 en órdenes abiertas, 5 reservadas, mínimo de 30 y objetivo de 50, la posición es **18 + 10 − 5 = 23**. Como 23 ≤ 30, se sugieren **50 − 23 = 27 unidades**. Una vez emitida y registrada esa orden, hay 10 + 27 = 37 unidades pendientes de recibir. Si los demás datos siguen iguales, la posición sube a **18 + 37 − 5 = 50** y la nueva sugerencia es **0**. Así se evita duplicar el pedido.

**Terminación y complejidad.** `sugerencias`, en `logistpulse/inventario/reposicion.py`, procesa una vez cada producto de un conjunto finito. Con **P productos**, el tiempo es **O(P)** porque se hacen las mismas operaciones por SKU. El generador entrega una sugerencia a la vez y usa **O(1)** de espacio auxiliar. Si se guardan todas las sugerencias, la salida ocupa **O(P)**.

## 3. Validación

Desde la raíz del repositorio, `python -m logistpulse inventario` reproduce los ejemplos. `python -m unittest tests.test_inventario -v` comprueba los siguientes casos, entre otros:

| Tipo | Caso | Resultado comprobado |
|---|---|---|
| Normal | Pedido de 80 unidades con lotes que vencen el mismo día | Plan de 30, 25 y 25 unidades, con desempate por código. |
| Normal | Pedido de 200 unidades con 155 elegibles | Se aplican las tres políticas de la tabla de resultados. |
| Normal | Orden abierta registrada después de la primera sugerencia | El recálculo sugiere 0 cuando la orden ya cubre el objetivo. |
| Límite | Pedido de exactamente 155 unidades elegibles | Estado `COMPLETO`, con pendiente 0. |
| Límite | Posición igual al mínimo | Con posición y mínimo de 30 y objetivo de 45, se sugieren 15 unidades. |
| Inválida | Cantidad solicitada 0, códigos de lote repetidos u objetivo inferior al mínimo | El programa devuelve un error de validación (`ValueError`). |

En `tests/test_complejidad.py`, `test_fefo_O_L_log_L_y_reposicion_O_P` verifica los conteos del filtro, el recorrido y el ordenamiento de candidatos en FEFO, y comprueba que la regla de reposición procesa cada SKU una sola vez.

### Preguntas de práctica para la defensa oral

1. **¿Qué pasa si dos lotes vencen el mismo día?** Se elige primero el lote con el código que aparece antes en orden alfabético. Así el resultado es reproducible aunque cambie el orden de entrada.
2. **¿Qué pasa si se piden 200 unidades y solo hay 155 elegibles?** Con política parcial se asignan 155 y quedan 45 pendientes. Con rechazo o espera se asignan 0, con el estado correspondiente.
3. **¿Por qué se cuentan las órdenes abiertas?** Porque las unidades pendientes de recibir ya están comprometidas por el proveedor. Al incluirlas en la posición, la siguiente sugerencia cubre únicamente el faltante que todavía activa la regla.

## Checklist

- [x] Pseudocódigo FEFO y de reposición consistente con el código.
- [x] Elegibilidad, regla de desempate y políticas ante stock insuficiente.
- [x] Terminación y Big-O de tiempo y espacio.
- [x] Ejemplo del enunciado y efecto de las órdenes abiertas sobre la siguiente sugerencia.
- [x] Resultados reproducibles y tabla con casos normales, límite e inválidos.
