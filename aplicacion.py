import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import tempfile

# Datos

data = pd.read_csv("proyecto_final_pl.csv", sep=";")


st.title("Proyecto CPM / PERT Para La planificación del Desarrollo de un Videojuego")
st.subheader("Daniel Santiago Carreño Briceño")
# Parrafo introductorio
st.markdown("En este proyecto se utiliza un modelo CPM/PERT para analizar la ruta de desarrollo de un videojuego. El objetivo es determinar el tiempo total de finalización del proyecto (en semanas), identificar la ruta crítica, calcular las holguras de cada actividad y evaluar la probabilidad de completar el desarrollo en un número específico de semanas.")

st.subheader("Tabla de Actividades")
st.markdown("En la siguiente tabla se muestra el desarrollo completo del modelo CPM/PERT para el proyecto de desarrollo de un videojuego.")
st.markdown("**Leyenda de columnas:**  \n"
"- **Nodos:** Identificador único de cada actividad.  \n"
"- **Actividades:** Breve descripción de la actividad.  \n"
"- **Tiempo Optimista (a) (semanas):** Tiempo mas corto en donde es posible terminar la actividad.  \n"
"- **Tiempo Medio (m) (semanas):** Tiempo más probable en donde se espera terminar la actividad.  \n"
"- **Tiempo Tardio (b) (semanas):** Tiempo más largo en donde es posible terminar la actividad.  \n"
"- **Tiempo_Probable:** Tiempo estimado para completar la actividad, siguiendo la formula (a + 4m + b) / 6.  \n"
"- **Varianza:** Medida de la dispersión del tiempo estimado, calculada como ((b - a) / 6)².  \n"
"- **Nodos_2:** Identificador alternativo de la actividad (igual que Nodos).  \n"
"- **Predecesor:** Actividades que deben completarse antes de iniciar la actividad actual.  \n"
"- **Duración:** Tiempo probable para completar la actividad (igual que Tiempo_Probable).  \n"
"- **TIC (Tiempo Inicio más temprano):** El tiempo más temprano en que una actividad puede comenzar.  \n"
"- **TFC (Tiempo Fin más temprano):** El tiempo más temprano en que una actividad puede finalizar.  \n"
"- **TIL (Tiempo Inicio más lejano):** El tiempo más tardío en que una actividad puede comenzar sin retrasar el proyecto.  \n"
"- **TFL (Tiempo Fin más lejano):** El tiempo más tardío en que una actividad puede finalizar sin retrasar el proyecto.  \n"
"- **Holgura:** Tiempo que una actividad puede retrasarse sin afectar la fecha de finalización del proyecto.  \n"
"- **VE_estimada (Varianza estimada):** Mismo valor que Varianza siempre y cuando la holgura de la actividad sea igual a 0.  \n")

# Mostrar tabla
st.dataframe(data, use_container_width=True)
# Link de la tabla en brightspace
st.markdown("La tabla completa también está disponible en el siguiente [enlace](https://unbosqueeduco-my.sharepoint.com/:x:/g/personal/dcarrenob_unbosque_edu_co/EbolqpvmTQxEjVKXxrh6JSgBmU6lP8UC__r1UaSUQ3g3dQ?e=PdJjCK).")

# Concluciones sobre holguras
st.subheader("Análisis de Holguras")
st.markdown("Las actividades que presentaron holguras fueron las siguientes: " \
"**C = 6,166666667 semanas**, **D = 3 semanas** y **F = 2,166666667 semanas**. Estas actividades tienen una holgura significativa, lo que indica que pueden retrasarse sin afectar la fecha de finalización del proyecto.")



# Grafo De actividades
def generar_grafo(df):
    G = Network(height="600px", width="100%", directed=True)
    for _, row in df.iterrows():
        G.add_node(row["Nodos"], label=row["Nodos"])    
        antecedentes = row["Predecesor"].split(",") if row["Predecesor"] != "-" else []
        for ant in antecedentes:
            ant = ant.strip()
            if ant:
                G.add_edge(ant, row["Nodos"])
    return G

#Grafo de ruta critica (A, B, E, G, H, I, J, K, L)
ruta_critica = ["A", "B", "E", "G", "H", "I", "J", "K", "L"]
def generar_grafo_ruta_critica(df, ruta_critica):
    G = Network(height="600px", width="100%", directed=True)
    ruta_set = set(ruta_critica)


    for _, row in df.iterrows():
        nodo = row["Nodos"]
        color_nodo = "#ff4d4d" if nodo in ruta_set else "#97c2fc"
        G.add_node(nodo, label=nodo, color=color_nodo)


        antecedentes = row["Predecesor"].split(",") if row["Predecesor"] != "-" else []
        for ant in antecedentes:
            ant = ant.strip()
            if ant:
                color_arista = "#ff4d4d" if ant in ruta_set and nodo in ruta_set else "#848484"
                G.add_edge(ant, nodo, color=color_arista)
    return G

st.subheader("Grafo de Actividades")
g = generar_grafo(data)
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
    temp_path = tmp.name

g.save_graph(temp_path)

with open(temp_path, "r", encoding="utf-8") as f:
    html = f.read()
st.components.v1.html(html, height=600)

# Grafo con ruta crítica
st.subheader("Grafo con Ruta Crítica (en rojo)")
g2 = generar_grafo_ruta_critica(data, ruta_critica)
temp_path2 = tempfile.NamedTemporaryFile(delete=False, suffix=".html").name
g2.save_graph(temp_path2)
st.components.v1.html(open(temp_path2, "r", encoding="utf-8").read(), height=600)

# analisis sobre ruta critica
st.subheader("Análisis de la Ruta Crítica")
st.markdown("La ruta crítica del proyecto es la secuencia de actividades que determina la duración total del proyecto. Cualquier retraso en estas actividades afectará directamente la fecha de finalización del proyecto. La ruta crítica identificada es: **A → B → E → G → H → I → J → K → L**.")
st.markdown("El tiempo total estimado para completar el proyecto, basado en la ruta crítica, es de **64,33 semanas**.")
st.markdown("Además, se ha calculado la varianza total de la ruta crítica, que es una medida de la incertidumbre asociada con la duración del proyecto. La varianza total de la ruta crítica es de **4,17 semanas²**. Y con una desviación estándar de aproximadamente **2,04 semanas**.")
st.markdown("Con estos valores podemos dar respuesta a algunas preguntas de probabilidad relacionadas con la finalización del proyecto:")

# Probabilidades sobre finalización del proyecto
st.subheader("Probabilidades de Finalización del Proyecto")
st.markdown("1. **Probabilidad de completar el proyecto en 70 semanas o menos:**  \n"
"Utilizando la distribución normal, podemos calcular la probabilidad de completar el proyecto en 70 semanas o menos. La fórmula para calcular el valor Z es:  \n")
st.latex(r"""
Z = \frac{X - \mu}{\sigma} = \frac{70 - 64.33}{2.04} \approx 2.78
""")
st.markdown("Consultando una tabla de la distribución normal estándar, encontramos que la probabilidad correspondiente a un valor Z de 2.78 es aproximadamente **0.9973** o **99.73%**.")
st.markdown("2. **Probabilidad de completar el proyecto en 60 semanas o menos:**  \n"
"Calculamos el valor Z para 60 semanas:  \n")
st.latex(r"""
Z = \frac{X - \mu}{\sigma} = \frac{60 - 64.33}{2.04} \approx -2.13
""")
st.markdown("Consultando la tabla de la distribución normal estándar, encontramos que la probabilidad correspondiente a un valor Z de -2.13 es aproximadamente **0.0166** o **1.66%**.")
st.markdown("3. **Probabilidad de completar el proyecto entre 62 y 68 semanas:**  \n"
"Calculamos los valores Z para 62 y 68 semanas:  \n")
st.latex(r"""
Z_{62} = \frac{62 - 64.33}{2.04} \approx -1.14
""")
st.latex(r"""
Z_{68} = \frac{68 - 64.33}{2.04} \approx 1.80
""")
st.markdown("Consultando la tabla de la distribución normal estándar, encontramos que la probabilidad correspondiente a un valor Z de -1.14 es aproximadamente **0.1271** o **12.71%**, y para un valor Z de 1.80 es aproximadamente **0.9641** o **96.41%**.  \n"
"La probabilidad de completar el proyecto entre 62 y 68 semanas es entonces:  \n")
st.latex(r"""
P(62 < X < 68) = P(Z_{68}) - P(Z_{62}) = 0.9641 - 0.1271 = 0.8370
""")
st.markdown("Por lo tanto, la probabilidad de completar el proyecto entre 62 y 68 semanas es aproximadamente **83.70%**.")

# Conclusiones finales
st.subheader("Conclusiones Finales")
st.markdown("El análisis CPM/PERT realizado para el proyecto de desarrollo de un videojuego ha proporcionado una visión clara de la planificación y gestión del tiempo del proyecto. La identificación de la ruta crítica ha sido fundamental para entender cuáles actividades requieren una atención especial debido a su impacto directo en la duración total del proyecto. Además, el cálculo de las probabilidades asociadas con diferentes tiempos de finalización ha permitido evaluar los riesgos y establecer expectativas realistas para la entrega del proyecto. En resumen, este análisis no solo facilita una mejor gestión del tiempo, sino que también contribuye a la toma de decisiones informadas durante el desarrollo del proyecto.")
