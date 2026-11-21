"""Crea en GitHub un Issue por cada fila del backlog (historias de fase + 10 correos) y los asigna.

El enunciado pide que cada correo sea una unidad de trabajo vinculada a su ficha,
su código y sus pruebas: cada Issue enlaza esos tres archivos. Al abrir el PR,
escriban "Closes #N" para que el Issue se cierre solo al hacer merge.

Uso (en el Codespace, donde `gh` ya está autenticado):
    python scripts/crear_issues.py            # muestra lo que haría (no crea nada)
    python scripts/crear_issues.py --crear    # crea SOLO los que faltan (se puede repetir sin duplicar)
    python scripts/crear_issues.py --asignar Camila=usuario1 Luis=usuario2 Jessica=usuario3
                                              # pone a cada Issue su responsable (usuarios de GitHub)
"""

import json
import re
import shutil
import subprocess
import sys

import _bootstrap  # noqa: F401
from _bootstrap import RAIZ

# Quién tiene el rol de "Implementación y validación" en cada sprint (equipo/ROLES_Y_PROMPTS.md).
VALIDACION_POR_SPRINT = {"1": "Luis", "2": "Jessica", "3": "Camila"}


def filas_backlog():
    """(id, título, cuerpo, responsable, sprint) por cada fila de docs/sprints/backlog.md."""
    texto = (RAIZ / "docs" / "sprints" / "backlog.md").read_text(encoding="utf-8")
    for linea in texto.splitlines():
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if not celdas or not re.match(r"^(F-[A-Z]\d|C-[pnc]\d)$", celdas[0]):
            continue
        if celdas[0].startswith("C-"):
            id_, correo, clase, resp, sprint, ficha, codigo, pruebas, _estado = celdas
            titulo = f"[{id_}] {correo} ({clase})"
            cuerpo = (f"**Unidad de trabajo del correo {id_[2:]}** · Responsable: {resp} · Sprint {sprint}\n\n"
                      f"- Ficha: {ficha}\n- Código: {codigo.replace('`casos/', '`logistpulse/casos/')}\n- Pruebas: {pruebas.replace('`test_', '`tests/test_')}\n\n"
                      "Hecho cuando: ficha sin secciones pendientes por redactar, lista de verificación marcada, "
                      "`python scripts/verificar_entrega.py` sin pendientes de esta ficha y PR revisado por otro integrante.")
        else:
            id_, historia, fase, resp, sprint, est, _estado, evidencia = celdas
            titulo = f"[{id_}] {historia}"
            cuerpo = (f"Fase {fase} · Responsable: {resp} · Sprint {sprint} · Estimación {est}\n\n"
                      f"Evidencia: {evidencia}\n\nHecho cuando: PR revisado por otro integrante y pruebas en OK.")
        yield id_, titulo, cuerpo, resp, sprint


def gh(*args):
    return subprocess.run(["gh", *args], cwd=RAIZ, capture_output=True, text=True)


def issues_en_github() -> dict:
    """{id del backlog: número del Issue}, leyendo el prefijo [ID] de los títulos (abiertos y cerrados)."""
    r = gh("issue", "list", "--state", "all", "--limit", "300", "--json", "number,title")
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "no se pudo listar los Issues")
    existentes = {}
    for it in json.loads(r.stdout or "[]"):
        m = re.match(r"^\[([^\]]+)\]", it["title"])
        if m:
            existentes[m.group(1)] = it["number"]
    return existentes


def responsable_de(resp: str, sprint: str, usuarios: dict):
    """Nombre del backlog → usuario de GitHub. 'Rol de validación' → quien lo tiene en ese sprint."""
    for nombre, usuario in usuarios.items():
        if nombre.lower() in resp.lower():
            return usuario
    if "validaci" in resp.lower():
        return usuarios.get(VALIDACION_POR_SPRINT.get(sprint, "").lower())
    return None


def leer_usuarios(args) -> dict:
    usuarios = {}
    for a in args:
        if "=" in a:
            nombre, usuario = a.split("=", 1)
            usuarios[nombre.strip().lower()] = usuario.strip().lstrip("@")
    return usuarios


def main() -> int:
    crear, asignar = "--crear" in sys.argv, "--asignar" in sys.argv
    filas = list(filas_backlog())
    if not (crear or asignar):
        for _id, titulo, *_ in filas:
            print(f"- {titulo}")
        print(f"\n{len(filas)} Issues en el backlog. Para crearlos: python scripts/crear_issues.py --crear")
        return 0
    if shutil.which("gh") is None:
        print("No está `gh` (GitHub CLI). En Codespaces viene instalado; localmente: https://cli.github.com")
        return 1
    try:
        existentes = issues_en_github()
    except RuntimeError as e:
        print(f"ERROR {e}")
        return 1

    if crear:
        nuevos = 0
        for id_, titulo, cuerpo, *_ in filas:
            if id_ in existentes:
                continue
            r = gh("issue", "create", "--title", titulo, "--body", cuerpo)
            if r.returncode == 0:
                nuevos += 1
                url = r.stdout.strip()
                existentes[id_] = int(url.rstrip("/").rsplit("/", 1)[-1]) if url.rsplit("/", 1)[-1].isdigit() else None
                print(f"OK creado {titulo} → {url}")
            else:
                print(f"ERROR {titulo}: {r.stderr.strip()}")
        print(f"{nuevos} Issues nuevos · {len(filas) - nuevos} ya existían")

    if asignar:
        usuarios = leer_usuarios(sys.argv[sys.argv.index("--asignar") + 1:])
        if not usuarios:
            print("Falta decir los usuarios: --asignar Camila=usuario1 Luis=usuario2 Jessica=usuario3")
            return 1
        errores = 0
        for id_, titulo, _cuerpo, resp, sprint in filas:
            numero, usuario = existentes.get(id_), responsable_de(resp, sprint, usuarios)
            if numero is None:
                print(f"SIN ISSUE {titulo} (créalo con --crear)")
                continue
            if usuario is None:
                print(f"SIN ASIGNAR #{numero} {titulo}: responsable '{resp}' no está en la lista")
                continue
            r = gh("issue", "edit", str(numero), "--add-assignee", usuario)
            if r.returncode == 0:
                print(f"OK #{numero} → {usuario}")
            else:
                errores += 1
                print(f"ERROR #{numero} → {usuario}: {r.stderr.strip()} "
                      "(¿aceptó la invitación de colaborador? ¿el usuario está bien escrito?)")
        return 1 if errores else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
