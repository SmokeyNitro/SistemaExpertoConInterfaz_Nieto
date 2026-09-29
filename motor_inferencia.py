"""
MOTOR DE INFERENCIA - encadenamiento hacia adelante.
Cada ciclo tiene tres fases:
  1. Equiparación:            buscar las reglas cuyas condiciones se cumplen.
  2. Resolución de conflictos: si hay varias, elegir solo una.
  3. Ejecución:                agregar la conclusión de esa regla a los hechos.
"""


def cumple(condicion, hechos):
    hecho, valor = condicion
    if isinstance(valor, list):
        return hechos.get(hecho) in valor
    return hechos.get(hecho) == valor


# FASE 1: EQUIPARACIÓN
def equiparacion(hechos, reglas, disparadas):
    conjunto_conflicto = []
    for regla in reglas:
        if regla["id"] in disparadas:          # refracción: no repetir reglas
            continue
        if regla["entonces"][0] in hechos:     # su conclusión ya se conoce
            continue
        if all(cumple(c, hechos) for c in regla["si"]):
            conjunto_conflicto.append(regla)
    return conjunto_conflicto


# FASE 2: RESOLUCIÓN DE CONFLICTOS
# Estrategia: gana la regla más específica (más condiciones).
# Si hay empate, gana la de mayor prioridad (la que aparece primero).
def resolucion_conflictos(conjunto_conflicto):
    maximo = max(len(r["si"]) for r in conjunto_conflicto)
    candidatas = [r for r in conjunto_conflicto if len(r["si"]) == maximo]
    elegida = candidatas[0]

    if len(conjunto_conflicto) == 1:
        criterio = "Única regla aplicable"
    elif len(candidatas) == 1:
        criterio = f"Especificidad: es la regla con más condiciones ({maximo})"
    else:
        criterio = f"Empate en especificidad ({maximo}); gana por prioridad"
    return elegida, criterio


# FASE 3: EJECUCIÓN
def ejecucion(regla, hechos):
    hecho, valor = regla["entonces"]
    hechos[hecho] = valor
    return hecho, valor


def inferir(hechos_iniciales, reglas):
    hechos = dict(hechos_iniciales)
    disparadas = []
    traza = []

    while True:
        conjunto = equiparacion(hechos, reglas, disparadas)
        if not conjunto:
            break
        regla, criterio = resolucion_conflictos(conjunto)
        nuevo_hecho = ejecucion(regla, hechos)
        disparadas.append(regla["id"])
        traza.append({
            "ciclo": len(traza) + 1,
            "conjunto_conflicto": [r["id"] for r in conjunto],
            "regla": regla["id"],
            "criterio": criterio,
            "nuevo_hecho": nuevo_hecho,
        })
    return hechos, traza
