# Guía: trabajar el Deber 2 en GitHub Codespaces

**Por qué Codespaces y no Colab:** el criterio de gestión (1,0 pt) pide historial, ramas o commits identificables, revisiones y una versión etiquetada. En Codespaces cada persona hace commits con **su** cuenta de GitHub, así que en el historial aparecen los 3 autores. Además, la terminal y Git ya vienen listos, y los tres tienen exactamente el mismo entorno (`.devcontainer/`). Colab queda como plan B para correr algo rápido sin abrir el Codespace.

> **Límite:** JFLAP es un programa de escritorio (Java) y no abre en Codespaces. Camila lo usa en su computadora y sube las capturas arrastrándolas a `jflap/capturas/` en el explorador del Codespace.

> **Cuota gratis:** cada cuenta personal tiene 120 horas-núcleo al mes (unas 60 h en la máquina de 2 núcleos) y 15 GB de almacenamiento. El Codespace se detiene solo después de un rato sin uso. Al terminar cada sesión, deténganlo (`Codespaces → Stop current codespace`) y borren los que ya no usen.

---

## 1. Configuración inicial (una sola vez · Jessica)
> **Decisión del equipo: repo PÚBLICO.** El profesor abre el enlace sin invitación y GitHub Actions corre las pruebas **gratis** en cada push y PR (`.github/workflows/pruebas.yml`). Público **no** significa que cualquiera pueda modificarlo: solo los colaboradores suben cambios. Lo que implica (otros equipos pueden verlo) está en «Repo público: qué implica», al final.

1. En GitHub: **New repository** → nombre `logistpulse-deber2-tc` → **Public** → marca **Add a README file** → *Create*.
2. **Settings → Collaborators → Add people** → agrega a Camila y a Luis (cada uno acepta la invitación que le llega por correo).
3. En el repo: **Code → Codespaces → Create codespace on main**.
4. Arrastra `logistpulse-deber2-tc-v3.3.zip` al explorador de archivos del Codespace y, en la terminal:
   ```bash
   unzip -q logistpulse-deber2-tc-v3.3.zip
   shopt -s dotglob && cp -r logistpulse-deber2-tc/* . && rm -rf logistpulse-deber2-tc logistpulse-deber2-tc-v3.3.zip
   git add -A
   git commit -m "Sprint 1: base del proyecto (código, pruebas, plantillas). Desarrollado con apoyo de IA; ver README"
   git push
   ```
5. **Recrea el Codespace** para que se instale el entorno del repo (`.devcontainer`): Code → Codespaces → `…` → *Delete*, y luego *Create codespace on main* otra vez. Al crearlo corre solo las pruebas; en el registro de creación debe decir `OK`.
6. **Protege `main`**: *Settings → Rules → Rulesets → New ruleset → New branch ruleset*.
   - *Ruleset name*: `proteger-main` · *Enforcement status*: cambia **Disabled → Active** (si no, la regla no hace nada).
   - *Bypass list*: vacía.
   - *Target branches → Add target → **Include default branch*** (esa es `main`).
   - Marca **Require a pull request before merging** → *Required approvals*: **1**.
   - Marca **Require status checks to pass** → *Add checks* → escribe `pruebas` → elige **`pruebas (3.10)`** y **`pruebas (3.12)`** (se llaman como el *job* del workflow más la versión de Python).
   - Deja marcados *Restrict deletions* y *Block force pushes* → **Create**.
   - Prueba que funciona: `git checkout main && git commit --allow-empty -m "prueba" && git push` debe ser **rechazado**; deshazlo con `git reset --hard origin/main`.

7. Crea los Issues del backlog (uno por correo y uno por historia de fase):
   ```bash
   python scripts/crear_issues.py           # revisar la lista
   python scripts/crear_issues.py --crear   # crea solo los que faltan (repetirlo no duplica)
   python scripts/crear_issues.py --asignar Camila=usuario1 Luis=usuario2 Jessica=usuario3
   ```
   `--asignar` pone a cada Issue su responsable según el backlog (usuarios de GitHub; cada uno tiene que haber aceptado la invitación).

> **Capturas de gestión:** van en `docs/evidencias/` con el prefijo del sprint (`s1_`, `s2_`, `s3_`, `final_`). La lista, con el momento de cada una, está en `docs/EMPIEZA_AQUI.md`, sección 8.

## 2. Cada integrante (Camila, Luis, Jessica)
1. Repo → **Code → Codespaces → Create codespace on main** (cada uno el suyo; consume la cuota de su propia cuenta).
2. Crea **tu rama** (una sola vez):
   ```bash
   git checkout -b camila/fase-a-fichas-np      # Luis: luis/fase-bc-fichas-p · Jessica: jessica/fase-df-gestion
   ```
3. Trabaja con tu prompt de `equipo/ROLES_Y_PROMPTS.md` y pega lo que entregue tu IA en **tus** archivos.
4. Antes de cada commit:
   ```bash
   python scripts/generar_docs.py                 # actualiza las salidas observadas (no toca lo que redactaste)
   python -m unittest discover -s tests           # debe terminar en OK
   python scripts/verificar_entrega.py            # qué falta, criterio por criterio
   ```
5. Commit y Pull Request (en el PR escribe `Closes #N` con el número de los Issues que resuelves):
   ```bash
   git add docs/ jflap/capturas/
   git commit -m "Sprint 1 · Fase A: autómatas redactados y capturas JFLAP"
   git push -u origin camila/fase-a-fichas-np
   gh pr create --base main --fill
   ```
6. En el PR, GitHub Actions corre las pruebas solo (pestaña **Checks**, con Python 3.10 y 3.12). **No se aprueba un PR con el check en rojo (fallido).**
7. **Revisión cruzada** (Camila revisa a Luis, Luis a Jessica, Jessica a Camila). Quien revisa:
   ```bash
   gh pr list
   gh pr checkout <número>                         # trae la rama del compañero
   python -m unittest discover -s tests && python scripts/verificar_entrega.py
   gh pr review <número> --approve --body "Revisado: pruebas OK, lista de verificación completa"
   gh pr merge <número> --merge                    # --merge conserva los commits y sus autores
   git checkout main && git pull
   ```
   Si hay que corregir algo: `gh pr review <número> --request-changes --body "…"`.
8. Para seguir trabajando después de un merge:
   ```bash
   git checkout main && git pull && git checkout <tu-rama> && git merge main
   ```

## 3. Cierre de sprint (quien tenga el rol de Coordinación esa semana)
- Actualiza `docs/sprints/sprint_N.md` (tareas, PR, revisor, retrospectiva) y el estado del backlog, con commit y PR como todo lo demás.

## 4. Entrega final (Sprint 3 · Jessica)
```bash
python scripts/armar_informe.py                   # docs/generado/INFORME.docx
```
1. Descarga `INFORME.docx` (clic derecho → *Download*), ábrelo en Word o Google Docs, actualiza el índice y exporta a PDF.
2. Arrastra el PDF a `docs/` con el nombre `INFORME_Deber2_LOGISTPULSE.pdf`, haz commit y PR.
3. Cuando `verificar_entrega.py` quede sin pendientes:
   ```bash
   git checkout main && git pull
   git tag -a v1.0 -m "Entrega final Deber 2"
   git push origin v1.0
   gh release create v1.0 docs/INFORME_Deber2_LOGISTPULSE.pdf --title "Deber 2 · v1.0" --notes "Entrega final: código, JFLAP, informe y fichas"
   ```
4. **Acceso del profesor:** abre el enlace del repo en una ventana de incógnito. Como es público, tiene que verse sin iniciar sesión, con el check verde de Actions en el último commit.
5. En el espacio del curso suben el **enlace al repositorio** y el **PDF**.

## Repo público: qué implica
| Aspecto | Con repo público |
|---|---|
| Quién puede subir cambios | Solo los colaboradores invitados (paso 1.2). Público da permiso de **lectura** a todos, no de escritura |
| El profesor | Abre el enlace directo, sin invitación |
| GitHub Actions | Gratis en repos públicos: corre las pruebas en cada push y PR |
| Codespaces | Igual que en privado: cada uno gasta su propia cuota |
| Otros equipos del curso (mismos 10 correos) | **Pueden verlo y copiarlo** |

Para cuidarse frente a copias:
- El **historial de Git** (fechas, autores, PR, Issues) prueba quién lo hizo primero; por eso es importante trabajar con commits y PR desde ya.
- **No suban** el enunciado (.docx) ni el simulador (.html), que son material del curso; el zip no los trae. Tampoco datos personales.
- Si el profesor indica otra cosa, la visibilidad se cambia en *Settings → General → Danger Zone → Change repository visibility*; nada más de esta guía cambia.

## Problemas comunes
| Síntoma | Solución |
|---|---|
| `Permission denied` al hacer push | Aún no aceptaste la invitación de colaborador (también pasa con repo público: leer ≠ escribir). |
| El PR no deja hacer merge | Falta 1 aprobación o los checks `pruebas (3.10)` / `pruebas (3.12)` están en rojo: la protección de `main` está funcionando. |
| Actions en rojo pero en el Codespace pasa | Abre el log del check; casi siempre es un archivo que no se subió (`git status`). |
| Falla solo una prueba de **tiempo** | El Codespace estaba ocupado: vuelve a correr. Las pruebas de conteo no fallan por azar. |
| No se ven los diagramas Mermaid | Abre la vista previa del Markdown (`Ctrl+Shift+V`); la extensión ya está instalada. |
| `dot: command not found` o no hay `pandoc` | El Codespace se creó antes del `.devcontainer`: `sudo apt-get install -y graphviz pandoc` o recréalo. |
