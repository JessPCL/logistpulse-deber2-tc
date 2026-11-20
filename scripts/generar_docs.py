"""Genera la documentación derivada del código (fuente única = logistpulse/casos/__init__.py).

  docs/generado/tabla_resumen.md          (se REESCRIBE siempre)
  docs/generado/salidas_observadas.md     (se REESCRIBE siempre: ejecuta la demo)
  docs/generado/tablas_transiciones.md    (se REESCRIBE siempre)
  docs/generado/inventario_pruebas.md     (se REESCRIBE siempre)
  docs/fichas/<id>.md                     si NO existe: crea el esqueleto.
                                          si existe: SOLO actualiza el bloque de salida observada
                                          entre <!-- SALIDA:INICIO --> y <!-- SALIDA:FIN -->;
                                          el resto (lo que redactó el equipo) no se toca.
                                          Para recrear un esqueleto, borra el archivo.

Uso:  python scripts/generar_docs.py
"""

import io
import sys
from contextlib import redirect_stdout
from datetime import date

import _bootstrap  # noqa: F401
from _bootstrap import RAIZ

from logistpulse import __main__ as demo
from logistpulse.automatas import AUTOMATAS
from logistpulse.casos import CASOS
from logistpulse.io_datos import cargar_casos
from logistpulse.presentacion_casos import DEMOS

GEN = RAIZ / "docs" / "generado"
FICHAS = RAIZ / "docs" / "fichas"
RESPONSABLE = {"A": "Luis", "B": "Camila", "C": "Jessica"}
TEST = {"A": "tests/test_casos_p.py", "B": "tests/test_casos_np.py", "C": "tests/test_casos_npc.py"}
GUIA_GRUPO = {
    "A": "Definición formal; algoritmo polinómico conocido; pseudocódigo o código; complejidad temporal y espacial.",
    "B": "Problema de decisión; certificado; verificador polinómico; por qué esto prueba pertenencia a NP pero "
         "NO prueba por sí solo que el problema no esté en P ni que sea NP-completo.",
    "C": "Problema de decisión; verificador polinómico; problema NPC de origen y reducción polinómica "
         "(dirección correcta: CONOCIDO ≤p NUESTRO); consecuencia práctica para el tamaño de instancia.",
}


def tabla_resumen() -> str:
    """Columnas pedidas por el enunciado: tipo de problema, decidibilidad, algoritmo,
    complejidad y estrategia exacta/heurística (+ clase, que es el objetivo de la fase D)."""
    f = ["# Tabla resumen de los 10 correos", "",
         "_Generada por `scripts/generar_docs.py` desde `logistpulse/casos/__init__.py`. No editar a mano._", "",
         "| Correo | Clase | Tipo de problema | Decidible | Algoritmo | Complejidad (tiempo · espacio) | Estrategia |",
         "|--------------------|----------|-------------|----------|--------------------|------------------|-----------|"]
    for c in CASOS:
        tipo = "Decisión" if c.version.startswith("Decisión") else "Optimización → se clasifica su versión de decisión"
        f.append(f"| **{c.id}** {c.asunto} | {c.clase} | {tipo} | Sí | {c.algoritmo} | {c.tiempo} · {c.espacio} | {c.tipo} |")
    f += ["", "Evidencia de cada clase (detalle en cada ficha):", ""]
    for c in CASOS:
        f.append(f"- **{c.id}** ({c.clase}): {c.evidencia}")
    f += ["", "Grupo A = algoritmo polinómico conocido · B = pertenencia a NP con certificado (sin afirmar NPC) · "
          "C = NP-completo con reducción. Distribución: A = 3 (p1, p2, p3) · B = 4 (n1–n4) · C = 3 (c1–c3).", ""]
    return "\n".join(f)


def capturar(func) -> str:
    buf = io.StringIO()
    with redirect_stdout(buf):
        print(func())
    return buf.getvalue().rstrip()


DATOS = cargar_casos()


def salida_caso(c) -> str:
    return DEMOS[c.id](DATOS[c.id])


def _nodo(nombre: str) -> str:
    """Id ASCII + etiqueta original (Mermaid no acepta tildes en los ids)."""
    import unicodedata
    ident = "".join(ch for ch in unicodedata.normalize("NFKD", nombre) if ch.isalnum() and ch.isascii())
    return f'{ident}["{nombre}"]'


INICIO, FIN = "<!-- SALIDA:INICIO (generado por scripts/generar_docs.py; no editar) -->", "<!-- SALIDA:FIN -->"


def bloque_salida(c) -> str:
    return f"{INICIO}\n```text\n{salida_caso(c)}\n```\n{FIN}"


def actualizar_salida(texto: str, c) -> str:
    """Reemplaza solo el bloque marcado; devuelve el texto sin cambios si no hay marcas."""
    if INICIO not in texto or FIN not in texto:
        return texto
    antes, resto = texto.split(INICIO, 1)
    _, despues = resto.split(FIN, 1)
    return antes + bloque_salida(c) + despues


def mermaid(c) -> str:
    """Diagrama del grafo del expediente (solo casos con red explícita)."""
    d = DATOS[c.id]
    if c.id == "p1":
        aristas = [f"    {_nodo(u)} --> {_nodo(v)}" for u, v in d["conexiones"]]
    elif c.id == "p2":
        aristas = [f"    {_nodo(u)} -- {w} --> {_nodo(v)}" for u, v, w in d["tramos"]]
    elif c.id == "p3":
        aristas = [f"    {_nodo(u)} -- {w} --> {_nodo(v)}" for u, vs in d["capacidades"].items() for v, w in vs.items()]
    elif c.id == "c3":
        aristas = [f"    {_nodo(u)} --- {_nodo(v)}" for u, v in d["aristas"]]
    else:
        return ""
    return "```mermaid\nflowchart LR\n" + "\n".join(aristas) + "\n```\n"


def salidas() -> str:
    partes = ["# Salidas observadas", "",
              f"_Generado el {date.today().isoformat()} ejecutando `python -m logistpulse`. Reproducible: mismos datos, "
              "mismo orden de desempate._", ""]
    for nombre, func in demo.SECCIONES.items():
        partes += [f"## {nombre}", "", "```text", capturar(func), "```", ""]
    return "\n".join(partes)


def tablas_transiciones() -> str:
    partes = ["# Tablas de transiciones (Fase A)", "", "_Generadas desde `logistpulse/automatas/definiciones.py`._", ""]
    for clave, afd in AUTOMATAS.items():
        partes += [f"## {afd.nombre}", "", afd.descripcion, "", "```text", afd.definicion_formal(), "```", "",
                   afd.tabla_markdown(), "", f"Diagrama: `docs/diagramas/afd_{clave}.png` · JFLAP: `jflap/{clave}.jff`", ""]
    return "\n".join(partes)


def ficha(c) -> str:
    quien = RESPONSABLE[c.grupo]
    return f"""# Ficha {c.id} · {c.asunto}

**Remitente:** {c.remitente} · **Grupo:** {c.grupo} · **Clasificación propuesta:** {c.clase}
**Responsable de redacción:** {quien}

> Esqueleto generado desde el código. Los datos técnicos ya están verificados con pruebas.
> Formato y profundidad a imitar: docs/fichas/p1.md (ficha modelo terminada).
> Las secciones marcadas ✍️ las redacta {quien} (con su IA) sin cambiar las condiciones del correo.
> Lo que debe establecer este grupo: {GUIA_GRUPO[c.grupo]}

> **Solicitud operativa:** {c.pregunta}

## 0. Respuesta al correo (para {c.remitente.split(' · ')[0]})
✍️ 2–3 líneas en lenguaje operativo, basadas en la salida observada de la sección 7 (primera línea).

## 1. Resumen del correo
✍️ (2–4 líneas, sin cambiar condiciones del problema)
{mermaid(c)}
## 2. Entrada, salida y restricciones
- **Pregunta de decisión:** {c.pregunta}
- **Entrada:** {c.entrada}
- **Salida:** {c.salida}
- **Versión analizada:** {c.version}
- ✍️ Restricciones del correo (pesos ≥ 0, binario, presupuesto, etc.)

## 3. Clasificación y evidencia
- **Clase:** {c.clase}
- **Evidencia:** {c.evidencia}
- **Certificado / verificador:** {c.certificado}
- **Reducción:** {c.reduccion}

✍️ Justificación formal (ver guía del grupo arriba).

## 4. Decidibilidad y computabilidad
- **Modelo de cómputo supuesto:** máquina de Turing determinista (equivalente: modelo RAM con enteros codificados en binario).
- **¿Decidible?** {c.decidible}
- ✍️ Qué función/relación se computa y por qué el procedimiento termina para TODA entrada válida.

## 5. Algoritmo seleccionado
- **Algoritmo:** {c.algoritmo}
- **Tipo de solución:** {c.tipo}
- ✍️ Por qué este algoritmo y qué garantiza.

## 6. Complejidad (Big-O)
- **Variables:** {c.variables}
- **Tiempo:** {c.tiempo}
- **Espacio:** {c.espacio}
- ✍️ Justificación de la cota (de dónde sale cada factor).

## 7. Código, pruebas y salida observada
- **Código:** `{c.modulo}`
- **Pruebas:** `{TEST[c.grupo]}` (normales, límite e inválidas)
- **Datos del expediente:** `data/casos_simulador.json` → `"{c.id}"` (leídos con `io_datos.cargar_casos`)
- **Pruebas de complejidad:** `tests/test_complejidad.py` (conteo de operaciones + tiempos reales)
- **Reproducir:** `python -m logistpulse casos` · `python -m unittest {TEST[c.grupo].replace('/', '.').replace('.py', '')} -v`

{bloque_salida(c)}

## 8. Observaciones
{c.observaciones}

## ¿Qué concluimos?
| Decidibilidad | Computabilidad | Complejidad |
|---|---|---|
| ✍️ (¿siempre termina y responde Sí/No?) | ✍️ (¿qué función/relación calcula y con qué modelo?) | {c.clase} · {c.tiempo} |

## Preguntas para la defensa oral
✍️ 3 preguntas que podría hacer el profesor + respuesta en 2–3 frases.

## ✅ Lista de verificación (docs/PLANTILLA_FICHA.md)
- [ ] Resumen fiel al correo; ninguna condición ni dato cambiado; ambigüedades señaladas
- [ ] Pregunta de decisión explícita; si es optimización, clasificada por su versión de decisión
- [ ] Entrada con su tamaño definido (bits si hay números)
- [ ] Evidencia completa del grupo {c.grupo}
- [ ] Modelo de cómputo nombrado · terminación argumentada
- [ ] Algoritmo justificado (exacto / aproximado / heurístico)
- [ ] Big-O de tiempo y espacio con variables definidas, coherente con el código
- [ ] Código + pruebas + salida observada real · Big-O respaldado por tests/test_complejidad.py
- [ ] Respuesta al correo (sección 0) y tabla "¿Qué concluimos?" completas
- [ ] No se afirma P ≠ NP; P ⊆ NP; "NP" ≠ "no polinómico"
- [ ] Sin marcas ✍️ pendientes · 3 preguntas de defensa respondidas
"""


def inventario_pruebas() -> str:
    """Lista cada prueba con su categoría (normal / límite / inválida / complejidad)."""
    import unittest
    suite = unittest.defaultTestLoader.discover(str(RAIZ / "tests"), top_level_dir=str(RAIZ))

    def aplanar(s):
        for t in s:
            if isinstance(t, unittest.TestSuite):
                yield from aplanar(t)
            else:
                yield t

    filas, conteo = [], {}
    for t in sorted(aplanar(suite), key=lambda t: t.id()):
        modulo, clase, metodo = t.id().split(".")[-3:]
        nombre = metodo.lower()
        if modulo == "test_complejidad":
            cat = "complejidad (tiempo)" if clase == "TestTiemposReales" else "complejidad (conteo)"
        elif "invalid" in nombre or "rechaz" in nombre or "mal" in nombre or "falla" in nombre or "negativ" in nombre:
            cat = "inválida"
        elif "limite" in nombre or "vacia" in nombre or "sin_" in nombre or "sumidero" in nombre:
            cat = "límite"
        else:
            cat = "normal"
        conteo[cat] = conteo.get(cat, 0) + 1
        doc = (t.shortDescription() or "").replace("|", "/")
        filas.append(f"| `{modulo}` | `{clase}.{metodo}` | {cat} | {doc} |")
    resumen = " · ".join(f"{k}: {v}" for k, v in sorted(conteo.items()))
    return "\n".join(["# Inventario de pruebas", "",
                       f"_Generado por `scripts/generar_docs.py`. Total: {sum(conteo.values())} métodos de prueba ({resumen}). "
                       "Muchos métodos agrupan varios casos con `subTest`. La categoría se asigna por el nombre del método._", "",
                       "| Archivo | Prueba | Categoría | Descripción |", "|---|---|---|---|"] + filas) + "\n"


def main() -> None:
    GEN.mkdir(parents=True, exist_ok=True)
    FICHAS.mkdir(parents=True, exist_ok=True)
    (GEN / "tabla_resumen.md").write_text(tabla_resumen(), encoding="utf-8")
    (GEN / "salidas_observadas.md").write_text(salidas(), encoding="utf-8")
    (GEN / "tablas_transiciones.md").write_text(tablas_transiciones(), encoding="utf-8")
    (GEN / "inventario_pruebas.md").write_text(inventario_pruebas(), encoding="utf-8")
    print("✔ docs/generado/{tabla_resumen, salidas_observadas, tablas_transiciones, inventario_pruebas}.md")
    for c in CASOS:
        ruta = FICHAS / f"{c.id}.md"
        if not ruta.exists():
            ruta.write_text(ficha(c), encoding="utf-8")
            print(f"✔ {ruta.relative_to(RAIZ)} (esqueleto nuevo)")
            continue
        viejo = ruta.read_text(encoding="utf-8")
        nuevo = actualizar_salida(viejo, c)
        if INICIO not in viejo:
            print(f"⚠ {ruta.relative_to(RAIZ)}: sin marcas SALIDA; su salida observada no se puede actualizar sola")
        elif nuevo != viejo:
            ruta.write_text(nuevo, encoding="utf-8")
            print(f"✔ {ruta.relative_to(RAIZ)}: salida observada actualizada (redacción intacta)")
        else:
            print(f"· {ruta.relative_to(RAIZ)}: salida observada al día")


if __name__ == "__main__":
    main()
