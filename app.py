"""
INTERFAZ GRÁFICA (Streamlit) del Sistema Experto de Fotografía.
Ejecutar con:  streamlit run app.py
"""
import streamlit as st

from base_conocimiento import REGLAS, CONFIGURACIONES, HECHOS
from motor_inferencia import inferir

st.set_page_config(page_title="Sistema Experto de Fotografía", page_icon="📷", layout="centered")

# ------------------------------------------------------------------
# Preguntas: cada una llena un hecho de la base de conocimiento.
# Cada opción es (texto visible, valor del hecho, descripción corta).
# ------------------------------------------------------------------
APERTURAS_FIJA = [
    ("f/1.4", "luminosa", "Muy luminoso"),
    ("f/1.8", "luminosa", "Ej. 50 mm f/1.8"),
    ("f/2.8", "luminosa", "Ej. 24-70 f/2.8"),
    ("f/4", "estandar", "Ej. 24-105 f/4"),
]
APERTURAS_VARIABLE = [
    ("f/3.5-5.6", "estandar", "Lente kit (18-55)"),
    ("f/4-5.6", "estandar", "Ej. 70-300"),
    ("f/4.5-6.3", "estandar", "Ej. 150-600"),
]

PREGUNTAS = [
    {"hecho": "lugar", "titulo": "¿Dónde vas a tomar la foto?",
     "opciones": [("Exterior", "exterior", "Al aire libre"),
                  ("Interior", "interior", "Casa, oficina, salón")]},
    {"hecho": "momento", "titulo": "¿En qué momento del día?",
     "opciones": [("Mañana", "manana", "Luz suave"),
                  ("Mediodía", "mediodia", "Sol alto y fuerte"),
                  ("Tarde", "tarde", "Luz cálida"),
                  ("Noche", "noche", "Poca luz")]},
    {"hecho": "movimiento", "titulo": "¿Tu sujeto se mueve?",
     "opciones": [("Quieto", "quieto", "Retrato, paisaje, producto"),
                  ("Rápido", "rapido", "Deporte, niños, mascotas")]},
    {"hecho": "desenfoque", "titulo": "¿Quieres el fondo desenfocado?",
     "opciones": [("Sí", "si", "Sujeto aislado (bokeh)"),
                  ("No", "no", "Todo nítido")]},
    {"hecho": "tipo_lente", "titulo": "¿Tu lente tiene apertura fija o variable?",
     "opciones": [("Fija", "fija", "Un solo valor f (ej. 50 mm f/1.8)"),
                  ("Variable", "variable", "Dos valores f (ej. 18-55 f/3.5-5.6)")]},
    {"hecho": "apertura_lente", "titulo": "¿Cuál es la apertura máxima de tu lente?",
     "opciones": None},  # depende de la respuesta anterior
    {"hecho": "tripode", "titulo": "¿Tienes trípode?",
     "opciones": [("Sí", "si", "Cámara totalmente estable"),
                  ("No", "no", "Disparo a pulso")]},
    {"hecho": "flash", "titulo": "¿Tienes flash?",
     "opciones": [("Sí", "si", "Integrado o externo"),
                  ("No", "no", "Solo luz disponible")]},
    {"hecho": "ruido", "titulo": "¿Cuánto ruido digital aceptas en la foto?",
     "opciones": [("Bajo", "bajo", "Quiero una imagen limpia"),
                  ("Moderado", "moderado", "Prefiero no perder la foto")]},
]
TOTAL = len(PREGUNTAS)

st.markdown("""
<style>
.block-container {max-width: 760px; padding-top: 2rem;}
div.stButton > button {min-height: 3.4rem; border-radius: 12px; font-weight: 600;}
.titulo {font-size: 2.2rem; font-weight: 800; margin-bottom: 0;}
.sub {color: #8a8f98; margin-top: 0;}
.pregunta {font-size: 1.5rem; font-weight: 700; margin: 1rem 0 .5rem;}
.desc {color: #8a8f98; font-size: .85rem; text-align: center; margin-top: -.4rem;}
.tarjeta {background: linear-gradient(135deg,#1f2a44,#2d1f44); color: #fff;
          border-radius: 16px; padding: 1.4rem 1.6rem; margin: .5rem 0 1rem;}
.tarjeta h3 {margin: 0 0 .3rem; color: #fff;}
.dato {font-size: .8rem; color: #b9c0d0; text-transform: uppercase; letter-spacing: .05em;}
.valor {font-size: 1.5rem; font-weight: 800;}
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------
# Estado de la sesión
# ------------------------------------------------------------------
if "paso" not in st.session_state:
    st.session_state.paso = -1          # -1 = pantalla de bienvenida
    st.session_state.hechos = {}
    st.session_state.etiquetas = {}


def responder(hecho, valor, etiqueta):
    st.session_state.hechos[hecho] = valor
    st.session_state.etiquetas[hecho] = etiqueta
    st.session_state.paso += 1


def reiniciar():
    st.session_state.paso = -1
    st.session_state.hechos = {}
    st.session_state.etiquetas = {}


def texto_condicion(hecho, valor):
    if isinstance(valor, list):
        return f"{hecho} ∈ {{{', '.join(valor)}}}"
    return f"{hecho} = {valor}"


# ------------------------------------------------------------------
# Barra lateral: base de conocimiento visible
# ------------------------------------------------------------------
with st.sidebar:
    st.header("Base de conocimiento")
    with st.expander(f"Hechos ({len(HECHOS)})"):
        for nombre, descripcion in HECHOS.items():
            st.markdown(f"**{nombre}**: {descripcion}")
    with st.expander(f"Reglas ({len(REGLAS)})", expanded=True):
        for r in REGLAS:
            condiciones = " **Y** ".join(texto_condicion(h, v) for h, v in r["si"])
            h, v = r["entonces"]
            st.markdown(f"**{r['id']}**: SI {condiciones} → **{h} = {v}**")

st.markdown('<p class="titulo">📷 Sistema Experto de Fotografía</p>', unsafe_allow_html=True)
st.markdown('<p class="sub">Sistema experto basado en reglas para configurar '
            'la exposición de tu cámara</p>', unsafe_allow_html=True)

paso = st.session_state.paso

# ------------------------------------------------------------------
# Pantalla de bienvenida
# ------------------------------------------------------------------
if paso == -1:
    st.info("Responde 9 preguntas sobre la escena, tu equipo y tus preferencias. "
            "El sistema deducirá el nivel de luz y te recomendará el **modo, la "
            "apertura, la velocidad y el ISO** para tu foto.")
    c1, c2, c3 = st.columns(3)
    c1.metric("Hechos", len(HECHOS))
    c2.metric("Reglas", len(REGLAS))
    c3.metric("Preguntas", TOTAL)
    if st.button("Comenzar", type="primary", use_container_width=True):
        st.session_state.paso = 0
        st.rerun()

# ------------------------------------------------------------------
# Preguntas (una por pantalla)
# ------------------------------------------------------------------
elif paso < TOTAL:
    pregunta = PREGUNTAS[paso]
    opciones = pregunta["opciones"]
    if opciones is None:
        opciones = (APERTURAS_FIJA if st.session_state.hechos.get("tipo_lente") == "fija"
                    else APERTURAS_VARIABLE)

    st.progress(paso / TOTAL, text=f"Pregunta {paso + 1} de {TOTAL}")
    st.markdown(f'<p class="pregunta">{pregunta["titulo"]}</p>', unsafe_allow_html=True)

    columnas = st.columns(len(opciones))
    for col, (etiqueta, valor, descripcion) in zip(columnas, opciones):
        with col:
            if st.button(etiqueta, key=f"{pregunta['hecho']}_{etiqueta}",
                         use_container_width=True):
                responder(pregunta["hecho"], valor, etiqueta)
                st.rerun()
            st.markdown(f'<p class="desc">{descripcion}</p>', unsafe_allow_html=True)

    st.write("")
    if paso > 0 and st.button("← Atrás"):
        st.session_state.paso -= 1
        st.rerun()

# ------------------------------------------------------------------
# Resultado: se ejecuta el motor de inferencia
# ------------------------------------------------------------------
else:
    hechos_finales, traza = inferir(st.session_state.hechos, REGLAS)
    etiquetas = st.session_state.etiquetas
    nombre = hechos_finales.get("configuracion")

    st.progress(1.0, text="Inferencia completada")

    if nombre:
        cfg = CONFIGURACIONES[nombre]
        apertura = cfg["apertura"]
        if apertura == "máxima":
            apertura = f"{etiquetas['apertura_lente'].split('-')[0]} (máxima)"

        st.markdown(f"""
        <div class="tarjeta">
          <div class="dato">Configuración recomendada</div>
          <h3>{nombre}</h3>
          <div class="dato">{cfg['modo']} · Enfoque {cfg['enfoque']}</div>
        </div>""", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Apertura", apertura)
        c2.metric("Velocidad", cfg["velocidad"])
        c3.metric("ISO", cfg["iso"])
        st.success(f"**Consejo del experto:** {cfg['consejo']}")
        if hechos_finales.get("tipo_lente") == "variable" and hechos_finales.get("desenfoque") == "si":
            st.warning("Con un lente de apertura variable no se consigue un buen "
                       "desenfoque. Un lente fijo luminoso (ej. 50 mm f/1.8) lo lograría.")
    else:
        st.error("**No hay una configuración viable.** Con poca luz, sin trípode, "
                 "sin flash y exigiendo ruido bajo, ninguna regla permite exponer "
                 "correctamente la foto.")
        st.markdown("Opciones: usar un **trípode** (si el sujeto está quieto), "
                    "usar un **flash** o **aceptar algo de ruido** subiendo el ISO.")

    st.subheader("¿Cómo llegó el sistema a esta conclusión?")
    for paso_traza in traza:
        with st.container(border=True):
            h, v = paso_traza["nuevo_hecho"]
            st.markdown(f"**Ciclo {paso_traza['ciclo']}**")
            st.markdown(
                f"1️⃣ **Equiparación** · conjunto conflicto: "
                f"`{', '.join(paso_traza['conjunto_conflicto'])}`  \n"
                f"2️⃣ **Resolución de conflictos** · se elige **{paso_traza['regla']}** "
                f"— {paso_traza['criterio']}  \n"
                f"3️⃣ **Ejecución** · nuevo hecho: `{h} = {v}`")
    if nombre is None:
        st.caption("Ciclo final: la equiparación no encontró más reglas aplicables.")

    with st.expander("Base de hechos final"):
        st.json(hechos_finales)

    if st.button("Nueva consulta", type="primary", use_container_width=True):
        reiniciar()
        st.rerun()
