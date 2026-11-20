# Plantilla de ficha (una por correo)

**Ficha modelo terminada: [`docs/fichas/p1.md`](fichas/p1.md).** Todas las fichas deben tener ese formato y esa profundidad.

Orden de las secciones = lista "Ficha obligatoria para cada correo" del enunciado, más la
respuesta operativa que pide el simulador ("Contesta el requerimiento operativo…") y la tabla
de conclusión de los ejemplos de clase (docs/referencias/).

```
# Ficha <id> · <asunto del correo>
Remitente · Grupo (A/B/C) · Clasificación propuesta · Responsable
> Solicitud operativa: <pregunta Sí/No>

## 0. Respuesta al correo           (2–3 líneas para el remitente, en lenguaje operativo)
## 1. Resumen del correo            (sin cambiar condiciones ni datos; diagrama si hay red)
## 2. Entrada, salida y restricciones
   - Pregunta de decisión (Sí/No) y lenguaje formal L = {<...> : ...}
   - Entrada (codificación y TAMAÑO: n, V, E, bits…) · Salida · Restricciones
   - ¿Decisión u optimización? Si es optimización: la clasificación se hace sobre la
     versión de DECISIÓN asociada (ej. "¿existe ruta con costo ≤ K?") y se escribe así.
## 3. Clasificación y evidencia     (según el grupo; ver abajo)
## 4. Decidibilidad y computabilidad (modelo de cómputo nombrado; por qué termina SIEMPRE)
## 5. Algoritmo                     (pseudocódigo, justificación, exacto/aproximado/heurístico)
## 6. Complejidad                   (tiempo y espacio; variables definidas; valor vs bits)
## 7. Código, pruebas y salida observada (REAL: generada al ejecutar)
## 8. Observaciones / hallazgos y límites de la inferencia
## ¿Qué concluimos?                 (tabla Decidibilidad | Computabilidad | Complejidad)
## Preguntas para la defensa oral   (3 preguntas probables + respuesta en 2–3 frases)
```

## Evidencia que exige cada grupo
| Grupo | Debe establecer |
|---|---|
| **A · P** | Definición formal + algoritmo polinómico conocido + pseudocódigo/código + complejidad temporal y espacial. |
| **B · NP** | Problema de decisión + certificado + verificador polinómico (en el tamaño de la entrada) + por qué esto prueba pertenencia a NP pero **no** prueba que el problema esté fuera de P ni que sea NP-completo. |
| **C · NPC** | ∈ NP (certificado + verificador) + problema NP-completo de origen + reducción **CONOCIDO ≤p NUESTRO** (construcción, correctitud ⇔ y tiempo polinómico de la transformación) + consecuencia práctica para el tamaño de la instancia. |

## Lista de verificación (pegarla al final de cada ficha y marcarla)
- [ ] Resumen fiel al correo; ninguna condición ni dato cambiado; ambigüedades señaladas con la lectura elegida
- [ ] Pregunta de decisión explícita (lenguaje L); si el correo pide optimización, la clasificación se hace sobre la versión de decisión y está escrito
- [ ] Entrada con su **tamaño** definido (en bits si hay números: el valor B ≠ el tamaño log₂B)
- [ ] Evidencia completa del grupo (tabla de arriba)
- [ ] Modelo de cómputo nombrado (MT determinista / RAM con enteros en binario)
- [ ] Terminación argumentada (cota o variante que decrece), no solo afirmada
- [ ] Algoritmo justificado; dice si es exacto, aproximado o heurístico y qué garantiza
- [ ] Big-O de tiempo **y** espacio, con variables definidas; coincide con el código
- [ ] Ruta al código y a las pruebas (normales, límite, inválidas); salida observada **real**
- [ ] Big-O respaldado por `tests/test_complejidad.py` (conteo de operaciones y/o tiempo real)
- [ ] Respuesta al correo (sección 0) y tabla "¿Qué concluimos?" completas
- [ ] No se afirma P ≠ NP · P ⊆ NP · "NP" no significa "no polinómico" · grupo B no dice "NP-completo"
- [ ] Sin secciones pendientes por redactar (marcas [POR REDACTAR]) y sin emojis
- [ ] 3 preguntas de defensa oral con su respuesta
