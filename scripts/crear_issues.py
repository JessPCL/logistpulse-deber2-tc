"""Crea en GitHub un Issue por cada fila del backlog (9 historias de fase + 10 correos).

El enunciado pide que cada correo sea una unidad de trabajo vinculada a su ficha,
su código y sus pruebas: cada Issue enlaza esos tres archivos. Al abrir el PR,
escriban "Closes #N" para que el Issue se cierre solo al aprobarlo.

Uso (en el Codespace, donde `gh` ya está autenticado):
    python scripts/crear_issues.py            # muestra lo que haría (no crea nada)
    python scripts/crear_issues.py --crear    # crea los Issues de verdad (una sola vez)
"""

import re
import shutil
import subprocess
import sys

import _bootstrap  # noqa: F401
from _bootstrap import RAIZ


def filas_backlog():
    texto = (RAIZ / "docs" / "sprints" / "backlog.md").read_text(encoding="utf-8")
    for linea in texto.splitlines():
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if not celdas or not re.match(r"^(F-[A-Z]\d|C-[pnc]\d)$", celdas[0]):
            continue
        if celdas[0].startswith("C-"):
            id_, correo, clase, resp, sprint, ficha, codigo, pruebas, _estado = celdas
            titulo = f"[{id_}] {correo} ({clase})"
            cuerpo = (f"**Unidad de trabajo del correo {id_[2:]}** · Responsable: {resp} · Sprint {sprint}\n\n"
                      f"- Ficha: {ficha}\n- Código: {codigo}\n- Pruebas: {pruebas}\n\n"
                      "Hecho cuando: ficha sin marcas ✍️, lista de verificación marcada, "
                      "`python scripts/verificar_entrega.py` sin pendientes de esta ficha y PR revisado por otro integrante.")
        else:
            id_, historia, fase, resp, sprint, est, _estado, evidencia = celdas
            titulo = f"[{id_}] {historia}"
            cuerpo = (f"Fase {fase} · Responsable: {resp} · Sprint {sprint} · Estimación {est}\n\n"
                      f"Evidencia: {evidencia}\n\nHecho cuando: PR revisado por otro integrante y pruebas en OK.")
        yield titulo, cuerpo


def main() -> int:
    crear = "--crear" in sys.argv
    issues = list(filas_backlog())
    if crear and shutil.which("gh") is None:
        print("No está `gh` (GitHub CLI). En Codespaces viene instalado; localmente: https://cli.github.com")
        return 1
    for titulo, cuerpo in issues:
        if crear:
            r = subprocess.run(["gh", "issue", "create", "--title", titulo, "--body", cuerpo],
                               cwd=RAIZ, capture_output=True, text=True)
            print(("✔ " + r.stdout.strip()) if r.returncode == 0 else f"✘ {titulo}: {r.stderr.strip()}")
        else:
            print(f"· {titulo}")
    if not crear:
        print(f"\n{len(issues)} Issues listos. Para crearlos: python scripts/crear_issues.py --crear")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
