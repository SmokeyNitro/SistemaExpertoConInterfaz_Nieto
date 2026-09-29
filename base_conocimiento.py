"""
BASE DE CONOCIMIENTO
Sistema Experto de Fotografía - asistente de parámetros de exposición.

El conocimiento proviene de la experiencia del autor como fotógrafo:
según la luz, el sujeto y el equipo disponible, el sistema recomienda
una configuración de cámara (modo, apertura, velocidad e ISO).
"""

# ------------------------------------------------------------------
# HECHOS (10)
# 9 hechos de entrada (los responde el usuario) y 1 hecho intermedio
# (luz) que el sistema deduce con las reglas R1, R2 y R3.
# ------------------------------------------------------------------
HECHOS = {
    "lugar":          "Dónde se toma la foto: exterior | interior",
    "momento":        "Momento del día: manana | mediodia | tarde | noche",
    "movimiento":     "Cómo está el sujeto: quieto | rapido",
    "desenfoque":     "Quiere el fondo desenfocado: si | no",
    "tipo_lente":     "Apertura del lente: fija | variable",
    "apertura_lente": "Luminosidad del lente: luminosa (f/2.8 o menos) | estandar",
    "tripode":        "Tiene trípode: si | no",
    "flash":          "Tiene flash: si | no",
    "ruido":          "Ruido que tolera en la foto: bajo | moderado",
    "luz":            "(intermedio) Nivel de luz de la escena: alta | media | baja",
}

DIA = ["manana", "mediodia", "tarde"]

# ------------------------------------------------------------------
# REGLAS (9)
# "si": lista de condiciones (hecho, valor). Si el valor es una lista,
#       basta con que el hecho tenga cualquiera de esos valores.
# "entonces": (hecho, valor) que se agrega a la base de hechos.
# El orden de la lista es la PRIORIDAD usada para desempatar conflictos.
# ------------------------------------------------------------------
REGLAS = [
    # --- Reglas que deducen el nivel de luz (hecho intermedio) ---
    {"id": "R1",  # De día y al aire libre hay mucha luz
     "si": [("lugar", "exterior"), ("momento", DIA)],
     "entonces": ("luz", "alta")},

    {"id": "R2",  # De día, pero bajo techo, la luz baja varios pasos
     "si": [("lugar", "interior"), ("momento", DIA)],
     "entonces": ("luz", "media")},

    {"id": "R3",  # De noche la luz siempre es escasa
     "si": [("momento", "noche")],
     "entonces": ("luz", "baja")},

    # --- Reglas que recomiendan una configuración ---
    {"id": "R4",  # Con buena luz: diafragma cerrado, todo nítido, ISO base
     "si": [("luz", "alta")],
     "entonces": ("configuracion", "Escena nítida con buena luz")},

    {"id": "R5",  # Sujeto rápido con buena luz: velocidad alta para congelar
     "si": [("luz", "alta"), ("movimiento", "rapido")],
     "entonces": ("configuracion", "Congelar el movimiento")},

    {"id": "R6",  # Fondo desenfocado: solo es posible con un lente fijo luminoso
     "si": [("luz", ["alta", "media"]), ("movimiento", "quieto"),
            ("desenfoque", "si"), ("tipo_lente", "fija"),
            ("apertura_lente", "luminosa")],
     "entonces": ("configuracion", "Retrato con fondo desenfocado")},

    {"id": "R7",  # Poca luz + trípode + sujeto quieto: exposición larga a ISO base
     "si": [("luz", "baja"), ("movimiento", "quieto"), ("tripode", "si")],
     "entonces": ("configuracion", "Larga exposición con trípode")},

    {"id": "R8",  # Falta luz pero hay flash: se agrega luz artificial
     "si": [("luz", ["media", "baja"]), ("flash", "si")],
     "entonces": ("configuracion", "Flash rebotado")},

    {"id": "R9",  # Falta luz y se acepta ruido: se sube el ISO
     "si": [("luz", ["media", "baja"]), ("ruido", "moderado")],
     "entonces": ("configuracion", "ISO alto a pulso")},
]

# ------------------------------------------------------------------
# CONCLUSIONES: ajustes de cámara de cada configuración
# ------------------------------------------------------------------
CONFIGURACIONES = {
    "Escena nítida con buena luz": {
        "modo": "Prioridad de apertura (A/Av)", "apertura": "f/8",
        "velocidad": "1/250 s", "iso": "100", "enfoque": "AF-S",
        "consejo": "f/8 da nitidez desde el primer plano hasta el fondo. "
                   "Si es mediodía, cuida las sombras duras."},
    "Congelar el movimiento": {
        "modo": "Prioridad de velocidad (S/Tv)", "apertura": "f/4",
        "velocidad": "1/1000 s", "iso": "Auto (100-800)", "enfoque": "AF-C + ráfaga",
        "consejo": "El enfoque continuo sigue al sujeto y la ráfaga aumenta la "
                   "probabilidad de capturar el momento exacto."},
    "Retrato con fondo desenfocado": {
        "modo": "Prioridad de apertura (A/Av)", "apertura": "máxima",
        "velocidad": "1/250 s", "iso": "100-400", "enfoque": "AF-S punto único",
        "consejo": "A máxima apertura la profundidad de campo es mínima: "
                   "enfoca siempre al ojo más cercano."},
    "Larga exposición con trípode": {
        "modo": "Manual (M)", "apertura": "f/8",
        "velocidad": "5-15 s", "iso": "100", "enfoque": "Manual",
        "consejo": "Desactiva el estabilizador y usa el temporizador de 2 s "
                   "para evitar vibraciones."},
    "Flash rebotado": {
        "modo": "Manual (M)", "apertura": "f/4",
        "velocidad": "1/200 s", "iso": "400", "enfoque": "AF-S",
        "consejo": "Apunta el flash al techo o a una pared blanca para obtener "
                   "una luz suave y sin sombras duras."},
    "ISO alto a pulso": {
        "modo": "Prioridad de apertura (A/Av)", "apertura": "máxima",
        "velocidad": "1/125 s", "iso": "3200-6400", "enfoque": "AF-S",
        "consejo": "Aparecerá algo de ruido: dispara en RAW para reducirlo "
                   "en la edición."},
}
