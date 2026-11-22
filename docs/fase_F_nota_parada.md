# Fase F · Decidibilidad, computabilidad, complejidad y el problema de la parada
**Responsable: Jessica** · 1 página

- **Decidibilidad:** ¿hay un algoritmo que siempre termine y responda bien para toda entrada válida? Ej.: el AFD de pedidos da un paso por símbolo y siempre se detiene (A_DFA es decidible, Sipser Teo. 4.1).
- **Computabilidad:** ¿qué función o relación se calcula, y en qué modelo? Ej.: en p2, f(planta, R, D) = distancia mínima de R a D y un camino que la logra, en una máquina de Turing determinista (o RAM).
- **Complejidad:** ¿cuánto tiempo y memoria usa según el tamaño de la entrada? Ej.: Dijkstra, O((V + E) log V); TSP-DEC exacto, O(n!) u O(n²·2ⁿ).
- **Práctica:** ¿responde en tiempo útil con tamaños reales? Ej.: Dijkstra resuelve la planta del enunciado (7 zonas) al instante y 50 000 ubicaciones en 0,3 s; TSP-DEC con 20 centros tardaría unos 4 800 años.

"Decidible" no implica "eficiente", y "NP-completo" no significa "indecidible".

## Caso límite: decidible, pero impracticable
En c2 (TSP-DEC: ¿hay un recorrido por los n centros con costo ≤ L?), una instancia finita tiene (n − 1)! órdenes. Revisarlos todos siempre termina con la respuesta correcta: el problema es **decidible**. Pero lo medimos (`docs/generado/crecimiento.md`): 10 centros, 0,46 s; 20 centros, unos 4 800 años; 25 centros, unos 2,5·10¹⁰ años. Lo mismo pasa en c1 (SAT, 60 variables: unos 70 000 años) y en c3 (k = 60: unos 55 000 años). Es un límite de **complejidad**, no de decidibilidad: la respuesta llegaría, pero después de la vida útil del almacén. Por eso, en tamaños reales se usan heurísticas o aproximaciones.

## Contraste: "¿este programa arbitrario terminará para toda entrada?"
Aquí no hay cota: si una simulación no ha terminado, no se sabe si terminará después o nunca. HALT_TM = { ⟨M, w⟩ : M se detiene con la entrada w } es **indecidible** (Sipser, Teo. 5.1, por reducción desde A_TM, Teo. 4.11). **Idea de la diagonalización:** si existiera un decisor H, construiríamos D que, con la entrada ⟨M⟩, le pregunta a H si M se detiene con ⟨M⟩ y hace lo contrario (entra en un ciclo infinito si H dice "sí" y se detiene si dice "no"). Con la entrada ⟨D⟩, D se detiene si y solo si no se detiene: contradicción. "Para toda entrada" es aún más difícil: la máquina M′ que ignora su entrada y simula M con w termina con toda entrada ⇔ M se detiene con w, así que decidirlo permitiría decidir HALT_TM.

## Cómo probamos que nuestros algoritmos sí terminan
No hay un decisor **general**, pero sí se puede probar que un programa **concreto** termina, con una cota finita o una cantidad que decrece: AFD, un paso por símbolo; BFS y Dijkstra, cada zona se cierra una vez; Edmonds–Karp, ≤ V·E aumentos; FEFO y reposición, listas finitas; DPLL (c1) y ramificación (c3), profundidad ≤ n y ≤ k. `tests/test_complejidad.py` comprueba estas cotas contando operaciones.

## Checklist
- [x] Definiciones: decidibilidad, computabilidad (función/relación + modelo), complejidad y la diferencia en la práctica
- [x] Caso límite: una variante finita es decidible pero su búsqueda exhaustiva es impracticable (con números)
- [x] Contraste con HALT_TM: no existe un decisor general (idea de la diagonalización)
- [x] Cómo probamos la terminación de NUESTROS algoritmos (variante / cota finita)
