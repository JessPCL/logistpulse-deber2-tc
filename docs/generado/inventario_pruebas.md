# Inventario de pruebas

_Generado por `scripts/generar_docs.py`. Total: 141 métodos de prueba (complejidad (conteo): 16 · complejidad (tiempo): 4 · inválida: 33 · límite: 19 · normal: 69). Muchos métodos agrupan varios casos con `subTest`. La categoría se asigna por el nombre del método._

| Archivo | Prueba | Categoría | Descripción |
|---|---|---|---|
| `test_automatas` | `TestEntradasInvalidas.test_definiciones_mal_formadas` | inválida |  |
| `test_automatas` | `TestEntradasInvalidas.test_elemento_no_textual` | normal |  |
| `test_automatas` | `TestEntradasInvalidas.test_evento_desconocido` | normal |  |
| `test_automatas` | `TestEntradasInvalidas.test_simbolo_fuera_de_sigma` | normal |  |
| `test_automatas` | `TestLimites.test_cadena_vacia_rechazada` | inválida |  |
| `test_automatas` | `TestLimites.test_estados_finales_no_tienen_salidas` | normal |  |
| `test_automatas` | `TestLimites.test_sumidero_es_absorbente` | límite |  |
| `test_automatas` | `TestLimites.test_todos_los_estados_alcanzables` | normal |  |
| `test_automatas` | `TestLimites.test_variante_estricta_del_pedido` | normal |  |
| `test_automatas` | `TestSecuencias.test_minimo_dos_validas_y_dos_invalidas_por_automata` | inválida |  |
| `test_automatas` | `TestSecuencias.test_no_se_consume_reserva_sin_confirmar` | límite |  |
| `test_automatas` | `TestSecuencias.test_pruebas_minimas_del_enunciado` | normal |  |
| `test_automatas` | `TestSecuencias.test_todas_las_secuencias_documentadas` | normal |  |
| `test_automatas` | `TestSecuencias.test_traza_identifica_la_transicion_que_rechaza` | inválida |  |
| `test_automatas` | `TestSecuencias.test_varias_recepciones_parciales` | normal |  |
| `test_casos_np` | `TestN1.test_instancia_isomorfa` | normal |  |
| `test_casos_np` | `TestN1.test_limite_tamanos_distintos_y_vacio` | límite |  |
| `test_casos_np` | `TestN1.test_matrices_invalidas` | inválida |  |
| `test_casos_np` | `TestN1.test_mismos_grados_no_isomorfos` | normal |  |
| `test_casos_np` | `TestN1.test_verificador_rechaza_certificados_falsos` | inválida |  |
| `test_casos_np` | `TestN2.test_binario` | normal |  |
| `test_casos_np` | `TestN2.test_instancia_leida_en_binario` | normal |  |
| `test_casos_np` | `TestN2.test_invalidos` | inválida |  |
| `test_casos_np` | `TestN2.test_limites` | límite |  |
| `test_casos_np` | `TestN2.test_verificador_rechaza` | inválida |  |
| `test_casos_np` | `TestN3.test_bsgs_coincide_con_busqueda_lineal` | normal |  |
| `test_casos_np` | `TestN3.test_instancia` | normal |  |
| `test_casos_np` | `TestN3.test_invalidos` | inválida |  |
| `test_casos_np` | `TestN3.test_limites` | límite |  |
| `test_casos_np` | `TestN3.test_potencia_modular_igual_a_pow` | normal |  |
| `test_casos_np` | `TestN3.test_primalidad` | inválida |  |
| `test_casos_np` | `TestN3.test_verificador_rechaza` | inválida |  |
| `test_casos_np` | `TestN4.test_grafo_asimetrico_agota_las_permutaciones` | normal |  |
| `test_casos_np` | `TestN4.test_limite_un_vertice` | límite |  |
| `test_casos_np` | `TestN4.test_triangulo_tiene_simetria` | normal |  |
| `test_casos_np` | `TestN4.test_verificador_rechaza_identidad_y_falsos` | inválida |  |
| `test_casos_npc` | `TestC1.test_3cnf_satisfacible_e_insatisfacible` | normal |  |
| `test_casos_npc` | `TestC1.test_instancia_simulador` | normal |  |
| `test_casos_npc` | `TestC1.test_instancia_simulador_es_2cnf` | normal |  |
| `test_casos_npc` | `TestC1.test_invalidos` | inválida |  |
| `test_casos_npc` | `TestC1.test_limite_sin_clausulas` | límite |  |
| `test_casos_npc` | `TestC1.test_solvers_coinciden_aleatorio` | normal |  |
| `test_casos_npc` | `TestC1.test_verificador_rechaza` | inválida |  |
| `test_casos_npc` | `TestC2.test_held_karp_coincide_con_fuerza_bruta` | normal |  |
| `test_casos_npc` | `TestC2.test_heuristica_valida_pero_no_optima` | normal |  |
| `test_casos_npc` | `TestC2.test_instancia` | normal |  |
| `test_casos_npc` | `TestC2.test_invalidos` | inválida |  |
| `test_casos_npc` | `TestC2.test_limite_presupuesto` | límite |  |
| `test_casos_npc` | `TestC2.test_reduccion_ham_a_tsp` | normal |  |
| `test_casos_npc` | `TestC2.test_verificador_rechaza` | inválida |  |
| `test_casos_npc` | `TestC3.test_exactos_y_aproximacion` | normal |  |
| `test_casos_npc` | `TestC3.test_instancia` | normal |  |
| `test_casos_npc` | `TestC3.test_invalidos` | inválida |  |
| `test_casos_npc` | `TestC3.test_limites` | límite |  |
| `test_casos_npc` | `TestC3.test_reduccion_is_a_vc` | normal |  |
| `test_casos_npc` | `TestC3.test_verificador_rechaza` | inválida |  |
| `test_casos_p` | `TestP1.test_alcanzable` | normal |  |
| `test_casos_p` | `TestP1.test_grafo_dirigido_no_vuelve` | normal |  |
| `test_casos_p` | `TestP1.test_invalidos` | inválida |  |
| `test_casos_p` | `TestP1.test_limite_origen_igual_destino` | límite |  |
| `test_casos_p` | `TestP1.test_no_alcanzable_con_cierre` | normal |  |
| `test_casos_p` | `TestP1.test_traza_bfs_por_niveles` | normal |  |
| `test_casos_p` | `TestP1.test_verificador_de_camino` | normal |  |
| `test_casos_p` | `TestP2.test_bellman_ford_detecta_ciclo_negativo` | inválida |  |
| `test_casos_p` | `TestP2.test_dijkstra_falla_con_pesos_negativos` | inválida |  |
| `test_casos_p` | `TestP2.test_distancias_y_ruta` | normal |  |
| `test_casos_p` | `TestP2.test_grafo_rechaza_pesos_negativos_y_destino_inexistente` | inválida |  |
| `test_casos_p` | `TestP2.test_version_decision_limite` | límite |  |
| `test_casos_p` | `TestP3.test_entradas_invalidas` | inválida |  |
| `test_casos_p` | `TestP3.test_flujo_maximo_y_corte` | normal |  |
| `test_casos_p` | `TestP3.test_limite_sin_camino` | límite |  |
| `test_casos_p` | `TestP3.test_registro_con_cancelacion_de_flujo` | normal | El 2.º camino aumentante usa el tramo inverso b→a: se CANCELA el flujo de a→b. |
| `test_casos_p` | `TestP3.test_registro_de_tramos_usados_y_disponibles` | normal |  |
| `test_casos_p` | `TestP3.test_verificador_detecta_flujo_invalido` | inválida |  |
| `test_casos_p` | `TestP3.test_version_decision` | normal |  |
| `test_complejidad` | `TestConteoOperaciones.test_afd_un_paso_por_simbolo` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_bfs_es_O_V_mas_E` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_dijkstra_operaciones_de_heap_acotadas` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_dos_sat_lineal` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_edmonds_karp_cota_independiente_de_las_capacidades` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_enumeracion_tsp_es_factorial` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_factor_rango_exponencial_en_bits` | complejidad (conteo) | Peor caso (N primo, B = N−1): las divisiones se DUPLICAN con cada bit extra. |
| `test_complejidad` | `TestConteoOperaciones.test_fefo_O_L_log_L_y_reposicion_O_P` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_held_karp_es_n2_por_2n` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_heuristica_vecino_mas_cercano_es_cuadratica` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_log_discreto_lineal_en_B_y_bsgs_en_raiz` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_permutaciones_factoriales` | complejidad (conteo) | Mismos grados y no isomorfos (C_n vs C_3 ∪ C_{n−3}): la búsqueda agota las n! permutaciones. |
| `test_complejidad` | `TestConteoOperaciones.test_sat_fuerza_bruta_2n_y_dpll_acotado` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_verificadores_polinomicos` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_verificar_camino_p1` | complejidad (conteo) |  |
| `test_complejidad` | `TestConteoOperaciones.test_vertex_cover_ramificacion_2_a_la_k` | complejidad (conteo) |  |
| `test_complejidad` | `TestTiemposReales.test_bfs_crece_lineal` | complejidad (tiempo) |  |
| `test_complejidad` | `TestTiemposReales.test_dijkstra_crece_casi_lineal` | complejidad (tiempo) |  |
| `test_complejidad` | `TestTiemposReales.test_enumeracion_tsp_crece_factorial` | complejidad (tiempo) |  |
| `test_complejidad` | `TestTiemposReales.test_factor_rango_se_duplica_por_bit` | complejidad (tiempo) |  |
| `test_inventario` | `TestFEFO.test_entradas_invalidas` | inválida |  |
| `test_inventario` | `TestFEFO.test_excluye_vencidos_que_vencen_hoy_y_sin_stock` | límite |  |
| `test_inventario` | `TestFEFO.test_json_con_fecha_invalida` | inválida |  |
| `test_inventario` | `TestFEFO.test_limite_cantidad_uno_y_lista_vacia` | límite |  |
| `test_inventario` | `TestFEFO.test_limite_exactamente_todo_el_stock_elegible` | límite |  |
| `test_inventario` | `TestFEFO.test_orden_independiente_del_orden_de_entrada` | normal |  |
| `test_inventario` | `TestFEFO.test_pedido_normal_y_desempate_por_codigo` | inválida |  |
| `test_inventario` | `TestFEFO.test_stock_insuficiente_las_tres_politicas` | normal |  |
| `test_inventario` | `TestReposicion.test_ejemplo_del_enunciado` | normal |  |
| `test_inventario` | `TestReposicion.test_entradas_invalidas` | inválida |  |
| `test_inventario` | `TestReposicion.test_limite_minimo_igual_objetivo` | límite |  |
| `test_inventario` | `TestReposicion.test_limite_posicion_igual_al_minimo` | límite |  |
| `test_inventario` | `TestReposicion.test_lote_desde_json` | normal |  |
| `test_inventario` | `TestReposicion.test_no_duplica_si_ya_hay_orden_abierta` | normal |  |
| `test_inventario` | `TestReposicion.test_orden_abierta_parcial_solo_sugiere_la_diferencia` | normal |  |
| `test_inventario` | `TestReposicion.test_posicion_negativa` | inválida |  |
| `test_jflap` | `TestArchivosJFLAP.test_archivo_de_entradas_para_multiple_run` | normal |  |
| `test_jflap` | `TestArchivosJFLAP.test_jff_acepta_y_rechaza_lo_mismo` | inválida |  |
| `test_jflap` | `TestArchivosJFLAP.test_jff_igual_a_la_definicion` | normal |  |
| `test_jflap` | `TestJFLAPInvalido.test_ida_y_vuelta` | normal |  |
| `test_jflap` | `TestJFLAPInvalido.test_no_determinista` | normal |  |
| `test_jflap` | `TestJFLAPInvalido.test_sin_inicial_y_tipo_incorrecto` | límite |  |
| `test_jflap` | `TestJFLAPInvalido.test_transicion_lambda` | normal |  |
| `test_registro` | `TestCapas.test_casos_sin_datos_de_expediente_incrustados` | límite |  |
| `test_registro` | `TestCapas.test_procesamiento_no_lee_archivos_ni_imprime` | normal |  |
| `test_registro` | `TestMatrizTrazabilidad.test_citas_existen` | normal |  |
| `test_registro` | `TestRegistro.test_clase_coherente_con_grupo` | normal |  |
| `test_registro` | `TestRegistro.test_distribucion_3_4_3` | normal |  |
| `test_registro` | `TestRegistro.test_grupo_c_declara_reduccion_y_b_no_afirma_npc` | normal |  |
| `test_registro` | `TestRegistro.test_modulos_existen_y_demos_corren` | normal |  |
| `test_registro` | `TestRegistro.test_optimizacion_declara_version_de_decision` | normal |  |
| `test_rutas` | `TestDirigidoYAleatorio.test_arista_de_un_solo_sentido` | normal |  |
| `test_rutas` | `TestDirigidoYAleatorio.test_dijkstra_coincide_con_fuerza_bruta` | normal | Compara contra la enumeración de todos los caminos simples en grafos pequeños. |
| `test_rutas` | `TestInvalidos.test_json_con_vertice_no_declarado` | normal |  |
| `test_rutas` | `TestInvalidos.test_json_mal_formado_y_campos_faltantes` | inválida |  |
| `test_rutas` | `TestInvalidos.test_lazo_y_duplicada` | normal |  |
| `test_rutas` | `TestInvalidos.test_origen_destino_y_bloqueos_invalidos` | inválida |  |
| `test_rutas` | `TestInvalidos.test_pesos_invalidos` | inválida |  |
| `test_rutas` | `TestPlanta.test_bfs_minimiza_tramos_no_costo` | normal |  |
| `test_rutas` | `TestPlanta.test_bloqueos` | normal |  |
| `test_rutas` | `TestPlanta.test_destino_bloqueado_no_tiene_ruta` | normal |  |
| `test_rutas` | `TestPlanta.test_origen_igual_destino` | normal |  |
| `test_rutas` | `TestPlanta.test_ruta_base_costo_11` | normal |  |
| `test_rutas` | `TestPlanta.test_ruta_de_la_figura_es_optima_y_empata` | normal |  |
| `test_rutas` | `TestPlanta.test_tamano_y_tipo` | normal |  |
| `test_rutas` | `TestPlanta.test_traza_reproducible` | normal |  |
