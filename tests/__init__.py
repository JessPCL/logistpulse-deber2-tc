"""Permite correr las pruebas desde cualquier carpeta (agrega la raíz del repo al path)."""
import sys
from pathlib import Path

_RAIZ = str(Path(__file__).resolve().parent.parent)
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)
