# Sistema Experto de Fotografía

Sistema experto de parámetros para fotografía elaborado por **José Nieto** como tarea de *Base de Conocimiento*, PAO 7, ESPOCH.

Sistema experto basado en reglas que recomienda cómo configurar la cámara (modo, apertura, velocidad e ISO) según la escena, el equipo y las preferencias del fotógrafo. El conocimiento de las reglas proviene de la experiencia del autor como fotógrafo.

## Ejecución

```bash
pip install -r requirements.txt
streamlit run app.py
```

Se abre en el navegador en `http://localhost:8501`.

## Estructura

| Archivo | Contenido |
|---|---|
| `base_conocimiento.py` | 10 hechos, 9 reglas y las configuraciones (conclusiones) |
| `motor_inferencia.py` | Motor de encadenamiento hacia adelante con sus 3 fases |
| `app.py` | Interfaz gráfica en Streamlit |

## Hechos (10)

| Hecho | Valores | Origen |
|---|---|---|
| lugar | exterior, interior | Usuario |
| momento | manana, mediodia, tarde, noche | Usuario |
| movimiento | quieto, rapido | Usuario |
| desenfoque | si, no | Usuario |
| tipo_lente | fija, variable | Usuario |
| apertura_lente | luminosa, estandar | Usuario |
| tripode | si, no | Usuario |
| flash | si, no | Usuario |
| ruido | bajo, moderado | Usuario |
| luz | alta, media, baja | Deducido (R1–R3) |

## Reglas (9)

| Regla | SI | ENTONCES |
|---|---|---|
| R1 | lugar = exterior Y momento es de día | luz = alta |
| R2 | lugar = interior Y momento es de día | luz = media |
| R3 | momento = noche | luz = baja |
| R4 | luz = alta | Escena nítida con buena luz |
| R5 | luz = alta Y movimiento = rapido | Congelar el movimiento |
| R6 | luz alta o media Y quieto Y desenfoque = si Y lente fijo Y luminoso | Retrato con fondo desenfocado |
| R7 | luz = baja Y quieto Y tripode = si | Larga exposición con trípode |
| R8 | luz media o baja Y flash = si | Flash rebotado |
| R9 | luz media o baja Y ruido = moderado | ISO alto a pulso |

## Motor de inferencia

En cada ciclo se ejecutan tres fases:

1. **Equiparación:** se buscan las reglas cuyas condiciones se cumplen con los hechos actuales. Así se forma el *conjunto conflicto*. Se excluyen las reglas ya disparadas (refracción) y las que concluyen un hecho que ya se conoce.
2. **Resolución de conflictos:** gana la regla más **específica** (la que tiene más condiciones). Si hay empate, gana la de mayor **prioridad** (la que aparece primero en la base).
3. **Ejecución:** la conclusión de la regla elegida se agrega a la base de hechos.

El ciclo se repite hasta que no quedan reglas aplicables. La interfaz muestra la traza de cada ciclo.

## Uso de inteligencia artificial

La interfaz gráfica (`app.py`) y la documentación de este README se realizaron con ayuda de inteligencia artificial (Claude, de Anthropic). La base de conocimiento (hechos y reglas) proviene de la experiencia del autor como fotógrafo.
