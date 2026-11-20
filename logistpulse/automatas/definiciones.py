"""Definición formal de los tres autómatas de la Fase A.

Criterio único para F en los tres modelos (ver docs/DECISIONES_Y_HALLAZGOS.md):
    F = estados TERMINALES LEGÍTIMOS = el ciclo de vida cerró de forma válida.
Una secuencia es aceptada si describe un ciclo de vida COMPLETO y LEGAL.
Por eso Cancelado (pedido), Liberada/Expirada/Rechazada (reserva) y
Rechazada (compra) son finales. En la Figura 2 del enunciado Cancelado aparece
sin doble círculo; lo incluimos en F por consistencia con las Figuras 3 y 4,
donde Rechazada sí es final. Si el equipo prefiere L = "solo pedidos
entregados", basta con usar PEDIDO_ESTRICTO (F = {Entregado}).

Los símbolos son de UN carácter para poder probarlos en JFLAP (Multiple Run).
"""

from __future__ import annotations

from .afd import AFD

# --------------------------------------------------------------------------- PEDIDO
PEDIDO = AFD(
    nombre="Pedido",
    descripcion="Ciclo de vida del pedido (Figura 2).",
    estados=["Borrador", "Confirmado", "Reservado", "Preparacion", "Empacado", "Despachado", "Entregado", "Cancelado"],
    alfabeto={
        "c": "confirmar",
        "r": "reservar",
        "i": "iniciar_picking",
        "e": "empacar",
        "d": "despachar",
        "n": "entregar",
        "x": "cancelar",  # en Reservado implica liberar la reserva y cancelar
    },
    inicial="Borrador",
    finales={"Entregado", "Cancelado"},
    delta={
        ("Borrador", "c"): "Confirmado",
        ("Borrador", "x"): "Cancelado",
        ("Confirmado", "r"): "Reservado",
        ("Confirmado", "x"): "Cancelado",
        ("Reservado", "i"): "Preparacion",
        ("Reservado", "x"): "Cancelado",
        ("Preparacion", "e"): "Empacado",
        ("Empacado", "d"): "Despachado",
        ("Despachado", "n"): "Entregado",
    },
    posiciones={
        "Borrador": (70, 260), "Confirmado": (210, 180), "Reservado": (350, 100),
        "Preparacion": (500, 100), "Empacado": (650, 100), "Despachado": (800, 100),
        "Entregado": (950, 100), "Cancelado": (500, 300),
    },
)

PEDIDO_ESTRICTO = AFD(
    nombre="Pedido_estricto",
    descripcion="Variante: L = solo pedidos entregados (Cancelado ∉ F), tal como dibuja la Figura 2.",
    estados=PEDIDO.estados,
    alfabeto=PEDIDO.alfabeto,
    inicial=PEDIDO.inicial,
    finales={"Entregado"},
    delta=PEDIDO.delta,
    posiciones=PEDIDO.posiciones,
)

# --------------------------------------------------------------------------- RESERVA
RESERVA = AFD(
    nombre="Reserva",
    descripcion="Ciclo de vida de una reserva de inventario (Figura 3).",
    estados=["Solicitada", "Validada", "Reservada", "Consumida", "Liberada", "Expirada", "Rechazada"],
    alfabeto={
        "v": "validar",
        "s": "sin_stock",
        "c": "confirmar",
        "p": "picking",
        "x": "cancelar",
        "t": "vence_plazo",
    },
    inicial="Solicitada",
    finales={"Consumida", "Liberada", "Expirada", "Rechazada"},
    delta={
        ("Solicitada", "v"): "Validada",
        ("Solicitada", "s"): "Rechazada",
        ("Validada", "c"): "Reservada",
        ("Reservada", "p"): "Consumida",
        ("Reservada", "x"): "Liberada",
        ("Reservada", "t"): "Expirada",
    },
    posiciones={
        "Solicitada": (70, 220), "Validada": (240, 160), "Reservada": (420, 160),
        "Consumida": (620, 50), "Liberada": (620, 160), "Expirada": (620, 270), "Rechazada": (240, 320),
    },
)

# --------------------------------------------------------------------------- ORDEN DE COMPRA
ORDEN_COMPRA = AFD(
    nombre="OrdenCompra",
    descripcion="Ciclo de vida de una orden de compra (Figura 4). Se agrega el bucle "
    "δ(Recepcion parcial, p) = Recepcion parcial para admitir varias entregas parciales.",
    estados=["Borrador", "En aprobacion", "Aprobada", "Rechazada", "Enviada", "Recepcion parcial", "Recibida"],
    alfabeto={
        "s": "solicitar_aprobacion",
        "a": "aprobar",
        "r": "rechazar",
        "e": "emitir_orden",
        "p": "recibir_parte",
        "c": "recibir_completa",
        "f": "completar_recepcion",
    },
    inicial="Borrador",
    finales={"Recibida", "Rechazada"},
    delta={
        ("Borrador", "s"): "En aprobacion",
        ("En aprobacion", "a"): "Aprobada",
        ("En aprobacion", "r"): "Rechazada",
        ("Aprobada", "e"): "Enviada",
        ("Enviada", "p"): "Recepcion parcial",
        ("Enviada", "c"): "Recibida",
        ("Recepcion parcial", "p"): "Recepcion parcial",
        ("Recepcion parcial", "f"): "Recibida",
    },
    posiciones={
        "Borrador": (70, 220), "En aprobacion": (230, 220), "Aprobada": (390, 130),
        "Rechazada": (390, 320), "Enviada": (550, 130), "Recepcion parcial": (720, 40), "Recibida": (880, 130),
    },
)

AUTOMATAS = {"pedido": PEDIDO, "reserva": RESERVA, "orden_compra": ORDEN_COMPRA}

# --------------------------------------------------------------------------- SECUENCIAS DE PRUEBA
# (cadena, ¿se espera aceptación?, explicación). Las marcadas [ENUNCIADO] son las
# pruebas mínimas que pide el documento del deber.
SECUENCIAS = {
    "pedido": [
        ("criedn", True, "[ENUNCIADO] Borrador→Confirmado→Reservado→Preparacion→Empacado→Despachado→Entregado"),
        ("x", True, "Cancelación desde Borrador: cierre legítimo"),
        ("crx", True, "Se cancela un pedido reservado: libera la reserva y cierra en Cancelado"),
        ("d", False, "[ENUNCIADO] Borrador→Despachado: δ(Borrador,d) no existe; no se despacha sin confirmar, reservar, preparar y empacar"),
        ("crid", False, "Despachar desde Preparacion sin empacar: δ(Preparacion,d) no existe"),
        ("crix", False, "Cancelar durante el picking no está permitido en el modelo: δ(Preparacion,x) no existe"),
        ("cried", False, "Termina en Despachado ∉ F: falta la entrega"),
        ("criednd", False, "Evento después del estado final Entregado"),
        ("", False, "Cadena vacía ε: Borrador ∉ F"),
    ],
    "reserva": [
        ("vcp", True, "[ENUNCIADO] Solicitada→Validada→Reservada→Consumida"),
        ("s", True, "Sin stock: Solicitada→Rechazada"),
        ("vcx", True, "Reserva cancelada: Reservada→Liberada"),
        ("vct", True, "Vence el plazo: Reservada→Expirada"),
        ("vp", False, "Consumir una reserva que nunca fue confirmada: δ(Validada,p) no existe"),
        ("p", False, "Picking directo desde Solicitada"),
        ("vcpx", False, "Cancelar una reserva ya consumida"),
        ("vc", False, "Termina en Reservada ∉ F: la reserva sigue abierta"),
        ("sv", False, "Validar una solicitud ya rechazada"),
    ],
    "orden_compra": [
        ("saec", True, "Borrador→En aprobacion→Aprobada→Enviada→Recibida (recepción completa)"),
        ("saepf", True, "Una recepción parcial y luego se completa"),
        ("saeppf", True, "Dos recepciones parciales (bucle) y luego se completa"),
        ("sr", True, "Orden rechazada: cierre legítimo"),
        ("sre", False, "[ENUNCIADO] Rechazada→Enviada: un estado final rechazado no habilita emisión"),
        ("e", False, "Emitir sin solicitar ni aprobar"),
        ("sac", False, "Recibir mercadería de una orden aprobada pero nunca emitida"),
        ("saep", False, "Termina en Recepcion parcial ∉ F: falta completar la recepción"),
        ("saecp", False, "Recibir después de Recibida"),
    ],
}
