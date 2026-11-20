"""LOGISTPULSE · Deber 2 de Teoría de la Computación (USFQ).

Paquete organizado en tres capas, como pide la Fase E:
  - lectura      -> logistpulse.io_datos         (carga y valida JSON / .jff)
  - procesamiento-> automatas, rutas, inventario, casos  (algoritmos puros)
  - presentación -> logistpulse.presentacion     (texto/tablas para consola)

Ejecutar la demo completa:  python -m logistpulse
Ejecutar las pruebas:       python -m unittest discover -s tests -v
"""

__version__ = "1.0.0"
