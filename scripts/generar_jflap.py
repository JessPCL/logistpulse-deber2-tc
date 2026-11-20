"""Genera jflap/*.jff y los archivos de entradas para 'Multiple Run' de JFLAP.

Uso:  python scripts/generar_jflap.py
"""

import _bootstrap  # noqa: F401
from _bootstrap import RAIZ

from logistpulse.automatas import AUTOMATAS, SECUENCIAS
from logistpulse.automatas.jflap import guardar_jff


def main() -> None:
    carpeta = RAIZ / "jflap"
    for clave, afd in AUTOMATAS.items():
        ruta = guardar_jff(afd, carpeta / f"{clave}.jff")
        # JFLAP 'Load Inputs' lee una cadena por línea. ε se prueba a mano (fila vacía).
        entradas = [c for c, _, _ in SECUENCIAS[clave] if c]
        (carpeta / f"entradas_{clave}.txt").write_text("\n".join(entradas) + "\n", encoding="utf-8")
        esperado = ["| Cadena | Eventos | Esperado | Por qué |", "|---|---|---|---|"]
        for c, ok, por_que in SECUENCIAS[clave]:
            ev = " → ".join(afd.eventos(c)) if c else "ε (cadena vacía)"
            esperado.append(f"| `{c or 'ε'}` | {ev} | {'Accept' if ok else 'Reject'} | {por_que} |")
        (carpeta / f"esperado_{clave}.md").write_text(
            f"# Resultados esperados en JFLAP · {afd.nombre}\n\n"
            f"Archivo: `{clave}.jff` · entradas: `entradas_{clave}.txt`\n\n"
            "Σ: " + ", ".join(f"`{s}` = {e}" for s, e in afd.alfabeto.items()) + "\n\n"
            + "\n".join(esperado) + "\n", encoding="utf-8")
        print(f"✔ {ruta.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
