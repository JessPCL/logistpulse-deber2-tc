from itertools import product


def verificar(clausulas, asig):
    """Comprobación independiente: cada cláusula necesita un literal verdadero. O(m·k)."""
    return all(any(asig[abs(l)] == (l > 0) for l in c) for c in clausulas)


def simplificar(clausulas, lit):
    """Fija lit = verdadero: quita las cláusulas que ya se cumplen y borra el literal opuesto."""
    return [[l for l in c if l != -lit] for c in clausulas if lit not in c]


def dpll(clausulas, asig=None):
    """DPLL: propagación unitaria + literal puro + ramificación. Peor caso O(2ⁿ·n·m·k)."""
    asig = dict(asig or {})
    unit = next((c[0] for c in clausulas if len(c) == 1), None)
    while unit is not None:
        asig[abs(unit)] = unit > 0
        clausulas = simplificar(clausulas, unit)
        unit = next((c[0] for c in clausulas if len(c) == 1), None)
    if any(len(c) == 0 for c in clausulas):
        return None
    literales = {l for c in clausulas for l in c}
    for l in literales:
        if -l not in literales:
            asig[abs(l)] = l > 0
            clausulas = simplificar(clausulas, l)
    if not clausulas:
        return asig
    x = abs(clausulas[0][0])
    for lit in (x, -x):
        r = dpll(simplificar(clausulas, lit), {**asig, x: lit > 0})
        if r is not None:
            return r
    return None


def resolver(clausulas, n):
    r = dpll(clausulas)
    return None if r is None else {i: r.get(i, False) for i in range(1, n + 1)}


# Entrada: x1, x2, x3 (decisiones vehículo-franja) y las reglas (x1 o no x2) y (x2 o x3)
n, reglas = 3, [[1, -2], [2, 3]]
horario = resolver(reglas, n)
print("Horario candidato:", horario, "| posibilidades con", n, "decisiones:", 2 ** n)

# Pruebas: el verificador acepta el horario, DPLL coincide con fuerza bruta y detecta una fórmula sin solución
assert horario == {1: True, 2: False, 3: True} and verificar(reglas, horario)
assert not verificar(reglas, {1: False, 2: True, 3: False})
insatisfacible = [[a * 1, b * 2, c * 3] for a in (1, -1) for b in (1, -1) for c in (1, -1)]
assert resolver(insatisfacible, 3) is None
assert not any(verificar(insatisfacible, dict(zip((1, 2, 3), v))) for v in product((True, False), repeat=3))
tres_cnf = [[1, 2, 3], [-1, -2, 4], [-3, -4, 5], [2, 4, -5], [-1, 3, 5]]
assert verificar(tres_cnf, resolver(tres_cnf, 5))
print("Pruebas OK")
