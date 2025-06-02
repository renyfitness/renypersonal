
import streamlit as st
import math
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Calculador de Ánodos", layout="centered")

st.markdown("""
<style>
    /* Etiqueta del selectbox */
    div[data-baseweb="select"] > div {
        color: white !important;           /* texto dentro del input */
        background-color: black !important; 
        font-weight: bold !important;
    }

    /* Opciones del dropdown */
    div[data-baseweb="menu"] div {
        color: black !important;
        background-color: white !important;
    }

    /* Texto encima del selectbox */
    .stSelectbox label {
        color: black !important;
        font-weight: bold !important;
    }
</style>


""", unsafe_allow_html=True)


st.markdown("""
    
<style>
    /* Estilo general del fondo y texto */
    html, body, [class*="stApp"]  {
        background-color: #0d0d0d !important;
        color: white !important;
    }

    /* Estilo solo para etiquetas de input numérico y radio */
    div[data-baseweb="input"] label,
    .stNumberInput label,
    .stRadio > label,
    .stRadio div {
        color: white !important;
        font-weight: bold !important;
    }

    /* Estilo para selectboxes: dejar texto oscuro porque tienen fondo claro */
    .stSelectbox label {
        color: white !important;
        font-weight: bold !important;
    }

    /* Asegurar que el texto en selectbox no sea blanco */
    .stSelectbox div[role="combobox"] {
        color: black !important;
        font-weight: bold !important;
    }
</style>

""", unsafe_allow_html=True)

# Estilos personalizados para las tablas
st.markdown("""
    <style>
        table {
            border-collapse: collapse !important;
            width: 100%;
        }
        th, td {
            border: 3px solid #ff0000 !important;
            padding: 8px !important;
            color: white !important;
            font-weight: bold !important;
            text-align: center !important;
        }
        th {
            background-color: #b0acac !important;
        }
        td {
            background-color: #b0acac !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    html, body, [class="css"]  {
        font-size: 18px; / Ajusta este valor si deseas más grande o más pequeño /
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    /* Estilo para st.success() */
    div.stAlert[data-testid="stAlert-success"] {
        background-color: #007700 !important;  /* verde brillante */
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
    }

    /* Estilo para st.info() */
    div.stAlert[data-testid="stAlert-info"] {
        background-color: #004080 !important;  /* azul profundo */
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Aplica a todos los cuadros de alerta: st.success, st.info, etc. */
    div[role="alert"] {
        background-color: #004080 !important;  /* Azul oscuro o cambia a verde según el tipo */
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
    }

    /* Si quieres estilos distintos por tipo, usa nth-of-type si conoces el orden */
    /* O aplica clases con div[data-testid] si logras ver el identificador exacto con devtools */
    </style>
""", unsafe_allow_html=True)


st.markdown('''
<style>
html, body, [class="css"]  {
    font-weight: bold;
}
</style>
''', unsafe_allow_html=True)
st.title("🔩 Calculador de Ánodos para Protección Catódica")
st.markdown("---")
# Paso 0: Selección de tipo de sistema
tipo_sistema = st.radio("**¿Qué tipo de sistema desea calcular?**", ("Ánodos de sacrificio", "Corriente impresa (ICCP)"))
st.markdown("---")

# Cargar la base de datos de ánodos desde archivo JSON
with open("anodos_app_data.json", "r") as f:
    anodos_data = json.load(f)

# Diccionario de estructuras y sus ánodos recomendados
estructuras = {
    "Miter Gate Compartments": ["ALUMINUM-INDIUM ANODE 40 lbs", "MAGNESIUM ANODE 50 lbs", "ZINC ANODE 38 lbs"],
    "Locks Chamber-Bulkhead Slots": ["ALUMINUM-INDIUM ANODE 150 lbs"],
    "Locks Chamber-Miter Gates": ["DURICHLOR D51 ANODE 44 lbs"],
    "Locks Culverts": ["MAGNETITE ANODE 13 lbs"],
    "Rising Stem Valve Spacers": ["MAGNESIUM ANODE 5 lbs", "ZINC ANODE 5 lbs"],
    "Rising Steam Valve Body": ["MAGNESIUM ANODE 22 lbs", "MAGNESIUM ANODE 44 lbs", "ZINC ANODE 24 lbs", "ZINC ANODE 38 lbs"],
    "Regulating Valve": ["MAGNESIUM ANODE 24 lbs"],
    "Culvert Rising Stem Valve Wall Castings": ["MAGNESIUM ANODE 21 lbs", "ZINC ANODE 26 lbs"],
    "Vehicular Bridge Gates": ["ZINC ANODE 12 lbs"],
    "Miter Gate Bottom": ["ZINC ANODE 24 lbs"],
    "Caisson": ["ZINC ANODE 24 lbs"],
    "Cylindrical Valves": ["ZINC ANODE 26 lbs"],
    "North Approach Curtain Wall": ["ZINC ANODE 38 lbs"]
}

if tipo_sistema == "Ánodos de sacrificio":
    st.header("1. Selección de estructura a proteger")
    opciones_estructuras = list(estructuras.keys()) + ["Quiero usar un tipo diferente de ánodo", "Sugerencia de ánodo"]
    seleccion = st.selectbox("**Selecciona la estructura:**", opciones_estructuras)

    anodo_manual = False
    sugerencia = False
    anodo_seleccionado = ""

    if seleccion in estructuras:
        anodo_seleccionado = st.selectbox("**Selecciona uno de los ánodos recomendados:**", estructuras[seleccion])
        datos_anodo = next((a for a in anodos_data if a["Nombre"] == anodo_seleccionado), None)
        if anodo_seleccionado and datos_anodo:
            st.markdown("### 🧪 Especificaciones del Ánodo Seleccionado")
            st.table({
                "**Parámetro**": [
                    "Aleación", "Peso (lbs)", "Densidad (g/cm³)", "Eficiencia (%)",
                    "Capacidad (Ah/kg)", "Potencial (Abierto)", "Potencial (Cerrado)",
                    "Conexión", "Uso"
                ],
                "**Valor**": [
                    datos_anodo["Aleación"], datos_anodo["Peso (lbs)"], datos_anodo["Densidad (g/cm³)"],
                    datos_anodo["Eficiencia (%)"], datos_anodo["Capacidad (Ah/kg)"],
                    f"{datos_anodo['Potencial abierto (mV)']} mV",
                    f"{datos_anodo['Potencial cerrado (mV)']} mV",
                    datos_anodo["Conexión"], datos_anodo["Uso"]
                ]
            })

    elif seleccion == "Quiero usar un tipo diferente de ánodo":
        anodo_manual = True
        nombres_anodos = [anodo["Nombre"] for anodo in anodos_data]
        anodo_seleccionado = st.selectbox("Selecciona el ánodo que deseas utilizar:", nombres_anodos)
        datos_anodo = next((a for a in anodos_data if a["Nombre"] == anodo_seleccionado), None)
        if datos_anodo:
            st.markdown("### 🧪 Especificaciones del Ánodo Seleccionado")
            st.table({
                "Parámetro": [
                    "Aleación", "Peso (lbs)", "Densidad (g/cm³)", "Eficiencia (%)",
                    "Capacidad (Ah/kg)", "Potencial (Abierto)", "Potencial (Cerrado)",
                    "Conexión", "Uso"
                ],
                "Valor": [
                    datos_anodo["Aleación"], datos_anodo["Peso (lbs)"], datos_anodo["Densidad (g/cm³)"],
                    datos_anodo["Eficiencia (%)"], datos_anodo["Capacidad (Ah/kg)"],
                    f"{datos_anodo['Potencial abierto (mV)']} mV",
                    f"{datos_anodo['Potencial cerrado (mV)']} mV",
                    datos_anodo["Conexión"], datos_anodo["Uso"]
                ]
            })

    elif seleccion == "Sugerencia de ánodo":
        sugerencia = True

    # Preguntas 2 a 6
    st.header("2. Parámetros de cálculo")
    st.markdown('<span style="color:white; font-weight:bold;">Área sumergida total a proteger (m²):</span>', unsafe_allow_html=True)
    area = st.number_input("", min_value=0.0, step=0.01)
    st.markdown('<span style="color:white; font-weight:bold;">¿La estructura está recubierta?</span>', unsafe_allow_html=True)
    recubrimiento = st.radio("", ("Sí", "No"))
    st.markdown('<span style="color:white; font-weight:bold;">Salinidad del agua:</span>', unsafe_allow_html=True)
    salinidad = st.number_input("", min_value=0.0, step=0.1)
    st.markdown('<span style="color:white; font-weight:bold;">Vida útil deseada (años):</span>', unsafe_allow_html=True)
    vida_util = st.number_input("", min_value=1, value=10)

    # --- Sección: Salinidad Lago Gatún ---
    st.markdown("## 🌊 Monitoreo de Salinidad en el Lago Gatún (2019–2025)")

    # Datos extraídos previamente
    valores_salinidad = [
    0.250, 0.300, 0.300, 0.340, 0.420, 0.390, 0.380, 0.360, 0.325, 0.290,
    0.245, 0.250, 0.250, 0.257, 0.270, 0.300, 0.270, 0.270, 0.220, 0.170,
    0.180, 0.190, 0.200, 0.220, 0.220, 0.200, 0.200, 0.200, 0.170, 0.160,
    0.160, 0.160, 0.150, 0.140, 0.130, 0.140, 0.160, 0.220, 0.280, 0.290,
    0.320, 0.340, 0.338, 0.344, 0.400, 0.510, 0.600, 0.630, 0.520, 0.490,
    0.390, 0.300, 0.280, 0.310, 0.280, 0.280, 0.269, 0.250
    ]

    # Fechas correspondientes (una por mes desde enero 2019)
    fechas = pd.date_range(start="2019-01-01", periods=len(valores_salinidad), freq="M")

    # Crear gráfica interactiva
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fechas, y=valores_salinidad, mode='lines+markers',
                         name='Salinidad Lago Gatún', line=dict(color='red')))

    fig.update_layout(
    title="Variación de Salinidad en el Lago Gatún (2019–2025)",
    xaxis_title="Año",
    yaxis_title="Salinidad (ppt)",
    hovermode="x unified",
    template="plotly_white"
    )

    # Mostrar gráfica en la app
    st.plotly_chart(fig, use_container_width=True)

    if sugerencia:
        if salinidad < 1:
            anodo_seleccionado = "MAGNESIUM ANODE 5 lbs"
        elif salinidad < 17:
            anodo_seleccionado = "ZINC ANODE 12 lbs"
        else:
            anodo_seleccionado = "ALUMINUM-INDIUM ANODE 40 lbs"
        datos_anodo = next((a for a in anodos_data if a["Nombre"] == anodo_seleccionado), None)
        st.success(f"Ánodo sugerido: {anodo_seleccionado}")
        if datos_anodo:
            st.markdown("### 🧪 Especificaciones del Ánodo Sugerido")
            st.table({
                "Parámetro": [
                    "Aleación", "Peso (lbs)", "Densidad (g/cm³)", "Eficiencia (%)",
                    "Capacidad (Ah/kg)", "Potencial (Abierto)", "Potencial (Cerrado)",
                    "Conexión", "Uso"
                ],
                "Valor": [
                    datos_anodo["Aleación"], datos_anodo["Peso (lbs)"], datos_anodo["Densidad (g/cm³)"],
                    datos_anodo["Eficiencia (%)"], datos_anodo["Capacidad (Ah/kg)"],
                    f"{datos_anodo['Potencial abierto (mV)']} mV",
                    f"{datos_anodo['Potencial cerrado (mV)']} mV",
                    datos_anodo["Conexión"], datos_anodo["Uso"]
                ]
            })

    if datos_anodo and area > 0:
        densidad_corriente = 0.01 if recubrimiento == "Sí" else 0.1
        corriente = area * densidad_corriente
        horas = vida_util * 365 * 24
        carga_total = corriente * horas
        peso_anodo = datos_anodo["Peso (lbs)"] * 0.453592
        capacidad_ah_kg = datos_anodo["Capacidad (Ah/kg)"]
        eficiencia = datos_anodo["Eficiencia (%)"] / 100
        capacidad_util = capacidad_ah_kg * peso_anodo * eficiencia
        numero_anodos = math.ceil(carga_total / capacidad_util)

        st.markdown("---")
        st.header("3. Resultados del cálculo")
# Cálculos detallados - Ánodos de Sacrificio
if tipo_sistema == "Ánodos de sacrificio" and datos_anodo and area > 0:
    st.subheader("📐 Cálculos detallados - Ánodos de Sacrificio")

    st.markdown("### 📘 Fórmulas Utilizadas")
    st.latex(r"""
    Q = I \cdot t \cdot 8760
    """)
    st.markdown("- **Q**: Carga total requerida (Ah)")
    st.markdown("- **I**: Corriente requerida (A)")
    st.markdown("- **t**: Vida útil deseada (años)")

    st.latex(r"""
    C_{\text{útil}} = \text{Capacidad} \times \text{Masa} \times \text{Eficiencia}
    """)
    st.markdown("- **C_útil**: Capacidad útil de un ánodo (Ah)")
    st.markdown("- **Capacidad**: Capacidad del ánodo (Ah/kg)")
    st.markdown("- **Masa**: Peso del ánodo (kg)")
    st.markdown("- **Eficiencia**: Eficiencia de utilización del ánodo (decimal)")

    st.latex(r"""
    N = \frac{Q}{C_{\text{útil}}}
    """)
    st.markdown("- **N**: Número de ánodos requeridos")

    # Mostrar resultados reales con las variables calculadas
    st.markdown("### 🧮 Resultados Obtenidos")
    st.latex(f"Q = {corriente:.3f} \\cdot {vida_util} \\cdot 8760 = {carga_total:.2f} \\, Ah")
    st.latex(f"C_{{útil}} = {capacidad_ah_kg} \\cdot {peso_anodo:.2f} \\cdot {eficiencia:.2f} = {capacidad_util:.2f} \\, Ah")
    st.latex(f"N = \\frac{{{carga_total:.2f}}}{{{capacidad_util:.2f}}} = {numero_anodos}")

    st.success(f"Corriente requerida: {corriente:.3f} A")
    st.success(f"Carga total requerida: {carga_total:.1f} Ah")
    st.success(f"Ánodo seleccionado: {anodo_seleccionado} ({peso_anodo:.2f} kg)")
    st.success(f"Capacidad útil por ánodo: {capacidad_util:.1f} Ah")
    st.success(f"Número de ánodos necesarios: {numero_anodos}")


elif tipo_sistema == "Corriente impresa (ICCP)":
    st.header("⚡ Diseño de Sistema ICCP")

    # Paso 1: Parámetros base
    # NUEVO: Selección de método para ingresar el área
    st.markdown("### 🧱 Selección de método para ingresar áreas")
    metodo_area = st.radio(
        "**¿Cómo deseas ingresar el área a proteger?**",
        ["Área total sumergida", "Dividir por zonas"]
    )

    if metodo_area == "Área total sumergida":
        area = st.number_input("Área total sumergida (m²):", min_value=0.0, step=0.01)
        area_splash = area_seca = 0
        area_sumergida = area
    else:
        area_seca = st.number_input("Área de zona seca (m²):", min_value=0.0, step=0.01)
        area_splash = st.number_input("Área de splash zone (m²):", min_value=0.0, step=0.01)
        area_sumergida = st.number_input("Área de zona sumergida (m²):", min_value=0.0, step=0.01)
        area = area_seca + area_splash + area_sumergida

    st.markdown('<span style="color:white; font-weight:bold;">¿La estructura está recubierta?</span>', unsafe_allow_html=True)
    recubrimiento = st.radio("", ("Sí", "No"))
    st.markdown('<span style="color:white; font-weight:bold;">Salinidad del agua:</span>', unsafe_allow_html=True)
    salinidad = st.number_input("", min_value=0.0, step=0.1)
    resistividad = 1000 / (salinidad + 1)  # Ω·cm
    resistividad_metros = resistividad * 0.01  # Ω·m
    st.markdown('<span style="color:white; font-weight:bold;">Vida útil deseada (años):</span>', unsafe_allow_html=True)
    vida_util = st.number_input("", min_value=1, value=10)

    # --- Sección: Salinidad Lago Gatún ---
    st.markdown("## 🌊 Monitoreo de Salinidad en el Lago Gatún (2019–2025)")

    # Datos extraídos previamente
    valores_salinidad = [
    0.250, 0.300, 0.300, 0.340, 0.420, 0.390, 0.380, 0.360, 0.325, 0.290,
    0.245, 0.250, 0.250, 0.257, 0.270, 0.300, 0.270, 0.270, 0.220, 0.170,
    0.180, 0.190, 0.200, 0.220, 0.220, 0.200, 0.200, 0.200, 0.170, 0.160,
    0.160, 0.160, 0.150, 0.140, 0.130, 0.140, 0.160, 0.220, 0.280, 0.290,
    0.320, 0.340, 0.338, 0.344, 0.400, 0.510, 0.600, 0.630, 0.520, 0.490,
    0.390, 0.300, 0.280, 0.310, 0.280, 0.280, 0.269, 0.250
    ]

    # Fechas correspondientes (una por mes desde enero 2019)
    fechas = pd.date_range(start="2019-01-01", periods=len(valores_salinidad), freq="M")

    # Crear gráfica interactiva
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fechas, y=valores_salinidad, mode='lines+markers',
                         name='Salinidad Lago Gatún', line=dict(color='red')))

    fig.update_layout(
    title="Variación de Salinidad en el Lago Gatún (2019–2025)",
    xaxis_title="Año",
    yaxis_title="Salinidad (ppt)",
    hovermode="x unified",
    template="plotly_white"
    )

    # Mostrar gráfica en la app
    st.plotly_chart(fig, use_container_width=True)

    if recubrimiento == "Sí":
     if salinidad < 1:
        densidad_iccp = 0.005  # agua dulce recubierta
     elif salinidad <= 17:
        densidad_iccp = 0.01  # agua brackish recubierta
     else:
        densidad_iccp = 0.015  # agua salada recubierta
    else:
     if salinidad < 1:
        densidad_iccp = 0.02  # agua dulce sin recubrimiento
     elif salinidad <= 17:
        densidad_iccp = 0.05  # agua brackish sin recubrimiento
     else:
        densidad_iccp = 0.1  # agua salada sin recubrimiento
     # Cálculo de corriente con factor splash
    factor_splash = 0.5
    if metodo_area == "Dividir por zonas":
        area_efectiva = area_sumergida + factor_splash * area_splash
    else:
        area_efectiva = area

    corriente_total = area_efectiva * densidad_iccp

    zonas = ["Zona seca", "Splash zone", "Zona sumergida"]
    distribucion = [
    area_seca * densidad_iccp,
    area_splash * densidad_iccp,
    area_sumergida * densidad_iccp
    ]
    colores = ["#9a5626", "#FFA500", "#1E90FF"]

    fig, ax = plt.subplots()
    ax.bar(zonas, distribucion, color=colores)
    ax.set_ylabel("Corriente (A)")
    ax.set_title("Distribución de Corriente por Zona de la Estructura")
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown("""
    **¿Qué representa esta gráfica?**

    Esta gráfica muestra cómo se distribuye la corriente de protección catódica en las distintas zonas de la estructura:

    - 🟤 **Zona seca**: Corriente mínima o nula.
    - 🟠 **Splash zone**: Alta corrosividad. Requiere atención.
    - 🔵 **Zona sumergida**: Mayor necesidad de protección eléctrica.

    La corriente en cada zona se calcula multiplicando su área por la densidad de corriente seleccionada según salinidad y recubrimiento.
    """)

    carga_total = corriente_total * vida_util * 365 * 24

    # Paso 2: Selección o recomendación de rectificador
    st.markdown("---")
    st.subheader("🔌 Selección de Rectificador")
    rectificadores = {
        "ABB CP500i": {"corriente": 100, "voltaje": 50},
        "Cath-Tech Smart": {"corriente": 40, "voltaje": 50},
        "Cath-Tech CT800": {"corriente": 80, "voltaje": 50},
        "Corrpro RMU500": {"corriente": 50, "voltaje": 30},
        "Corrpro RMU3200": {"corriente": 50, "voltaje": 50},
        "Farwest MiniMod": {"corriente": 10, "voltaje": 15},
        "MESA TCR": {"corriente": 75, "voltaje": 60},
        "Tinker & Razor RM-12": {"corriente": 25, "voltaje": 24},
        "Universal UCP-100": {"corriente": 100, "voltaje": 100}
    }
    modo_rectificador = st.radio("**¿Deseas seleccionar el rectificador o recibir una sugerencia?**", ["Recomiéndalo tú", "Yo lo escojo"])
    if modo_rectificador == "Yo lo escojo":
        modelo_rectificador = st.selectbox("**Selecciona un modelo:**", list(rectificadores.keys()))
    else:
        modelo_rectificador = min(
    (modelo for modelo, datos in rectificadores.items() if datos["corriente"] >= corriente_total),
    key=lambda m: rectificadores[m]["corriente"] - corriente_total,
    default="Universal UCP-100"
)
        st.success(f"**Rectificador recomendado: {modelo_rectificador}**")
    datos_rect = rectificadores[modelo_rectificador]

    # Paso 3: Selección o recomendación de ánodo
    st.markdown("---")
    st.subheader("🔩 Selección de Ánodo Inerte")
    anodos_iccp = {
        "Durichlor D51": {"corriente": 2.0, "vida": 30},
        "MMO": {"corriente": 2.5, "vida": 40},
        "Magnetita": {"corriente": 1.5, "vida": 20},
        "Grafito": {"corriente": 1.2, "vida": 15},
        "Silicio-Hierro": {"corriente": 1.8, "vida": 25},
        "Platino-Titanio": {"corriente": 3.0, "vida": 50}
    }
    modo_anodo = st.radio("**¿Deseas seleccionar el tipo de ánodo o recibir una sugerencia?**", ["Recomiéndalo tú", "Yo lo escojo"])
    if modo_anodo == "Yo lo escojo":
        tipo_anodo = st.selectbox("**Selecciona el tipo de ánodo:**", list(anodos_iccp.keys()))
    else:
        tipo_anodo = max(anodos_iccp, key=lambda a: anodos_iccp[a]["corriente"])
        st.success(f"**Ánodo recomendado: {tipo_anodo}**")
    datos_anodo = anodos_iccp[tipo_anodo]
    numero_anodos = math.ceil(corriente_total / datos_anodo["corriente"])
    
    # Paso 4: Recomendación de cable
    st.markdown("---")
    st.subheader("🧵 Recomendación de Cableado")
    if datos_rect["voltaje"] > 60 or datos_anodo["corriente"] > 2.5:
        cable_sugerido = "XLPE/PVC 4 AWG - alta resistencia térmica y mecánica"
    else:
        cable_sugerido = "XLPE/PVC 6 AWG - inmersión continua y resistencia química"
    st.info(f"**Cable recomendado para seguridad y eficiencia: {cable_sugerido}**")

    # Paso 5: Electrodos de referencia
    st.markdown("---")
    st.subheader("🎯 Electrodos de Referencia")
    modo_electrodo = st.radio("**¿Deseas seleccionar el electrodo de referencia o recibir una sugerencia?**", ["Recomiéndalo tú", "Yo lo escojo"])
    electrodos = {
        "Cu/CuSO₄": "agua dulce",
        "Ag/AgCl": "agua salada",
        "Zinc": "ambientes marinos"
    }
    if modo_electrodo == "Yo lo escojo":
        tipo_electrodo = st.selectbox("**Selecciona el tipo:**", list(electrodos.keys()))
    else:
        tipo_electrodo = "Cu/CuSO₄" if salinidad < 1 else "Ag/AgCl"
        st.success(f"**Electrodo recomendado: {tipo_electrodo}**")

    # Paso 6: Monitoreo
    st.markdown("---")
    st.subheader("📡 Sistema de Monitoreo (en proceso)")
    st.info("**Esta sección será implementada cuando se confirme el sistema de monitoreo a utilizar.**")

# Mostrar cálculos ICCP reorganizados
if tipo_sistema == "Corriente impresa (ICCP)" and area > 0:
    st.markdown("### 🔋 Cálculos Detallados - Sistema ICCP")

   # Cálculo de distancia sugerida estructura-ánodo para ICCP
    potencial_minimo = -0.85  # V
    corriente_anodo = datos_anodo["corriente"]  # A (por defecto, puede cambiarse según tipo de ánodo seleccionado)
    sigma = 1 / resistividad_metros  # S/m
    distancia_sugerida = max(1.0, corriente_anodo / (4 * np.pi * sigma * abs(potencial_minimo)))

    resistencia_anodo = 0.5  # Ω por defecto (puedes adaptar esta fórmula según tipo)
    
    resistencia_electrolito = resistividad_metros / (4 * math.pi * distancia_sugerida)
    resistencia_total = resistencia_anodo + resistencia_electrolito
    voltaje_requerido = corriente_total * resistencia_total
    eficiencia_sistema = (corriente_total / datos_rect["corriente"]) * 100

    # Barra personalizada de eficiencia con color visual
    st.markdown("### 📊 Indicador Visual de Eficiencia del Sistema ICCP")

    if eficiencia_sistema >= 90:
        color_barra = "#00cc44"  # verde
        emoji = "🟢"
    elif eficiencia_sistema >= 70:
        color_barra = "#ffcc00"  # amarillo
        emoji = "🟡"
    else:
        color_barra = "#ff3300"  # rojo
        emoji = "🔴"

    st.write(f"**Eficiencia estimada:** {eficiencia_sistema:.1f}% {emoji}")

    st.markdown(f"""
    <div style="background-color: #ddd; border-radius: 13px; padding: 3px; margin-bottom: 15px;">
      <div style="width: {min(eficiencia_sistema,100)}%; background-color: {color_barra}; 
              padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; color: black;">
        {eficiencia_sistema:.1f}%
      </div>
    </div>
    """, unsafe_allow_html=True)


# Alerta por eficiencia baja
    if eficiencia_sistema < 50:
         st.error(
             f"¡Advertencia! La eficiencia del sistema es baja ({eficiencia_sistema:.2f}%). "
             "Revisa el tipo de ánodo, el rectificador seleccionado y la configuración general del sistema. "
             "Una eficiencia baja puede indicar un sobredimensionamiento o mala distribución del sistema."
         )

    st.markdown("---")

    st.markdown("### 🔥 Mapa Térmico de Distribución de Corriente")

    # Parámetros del área (estructura protegida)
    col1, col2, col3 = st.columns(3)
    with col1:
        largo_estructura = st.number_input("Largo de la estructura (m)", value=10.0)
    with col2:
        alto_estructura = st.number_input("Altura de la estructura (m)", value=12.0)
    with col3:
        distancia_horizontal_anodo = st.number_input("Distancia horizontal del ánodo (m)", value=3.0, min_value=0.0)

    distancia_vertical_anodo = st.number_input("Distancia vertical del ánodo (m)", value=1.0, min_value=0.0)

    # Coordenadas del ánodo en el centro de la estructura
    anodo_x = largo_estructura / 2 - distancia_horizontal_anodo
    anodo_y = -distancia_vertical_anodo

    # Corriente total real del sistema ICCP
    corriente_total_iccp = datos_anodo["corriente"] * numero_anodos  # A
    st.markdown("### 🔍 Verificación de corriente utilizada para el mapa térmico")
    st.write("🔢 Número de ánodos:", numero_anodos)
    st.write("⚡ Corriente por ánodo (A):", datos_anodo["corriente"])
    st.write("🔋 Corriente total ICCP (A):", corriente_total_iccp)

    # Crear grilla
    res = 100
    x = np.linspace(0, largo_estructura, res)
    y = np.linspace(0, alto_estructura, res)
    X, Y = np.meshgrid(x, y)

    # Calcular densidad estimada de corriente
    Z = (corriente_total_iccp * 1000) / (np.sqrt((X - anodo_x)**2 + (Y - anodo_y)**2) + 0.5)

    # Mapa térmico
    fig, ax = plt.subplots()
    heatmap = ax.pcolormesh(X, Y, Z, shading='auto', cmap='plasma')
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.set_label("Densidad estimada de corriente (mA/m²)")
    ax.set_title("Distribución de Corriente sobre la Superficie Protegida")
    ax.set_xlabel("Largo de la estructura (m)")
    ax.set_ylabel("Altura de la estructura (m)")

    st.pyplot(fig)

    # Bloque visual con fórmulas
    st.markdown(f"""
    <div style='background-color: #2a2a2a; padding: 15px; border-radius: 10px; color: white;'>
    <b>1. Densidad de corriente (J):</b><br>
    <span style='font-family: monospace; font-size: 18px;'>J = {densidad_iccp:.3f} A/m²</span><br>

    <b>2. Corriente por ánodo:</b><br>
    <span style='font-family: monospace; font-size: 18px; font-weight: bold;'>I_anodo = {datos_anodo["corriente"]:.2f} A</span><br>

    <b>3. Corriente total requerida (I):</b><br>
    $$ I = A \\cdot J = {area:.2f} \\cdot {densidad_iccp:.3f} = {corriente_total:.2f}\\ \\text{{A}} $$<br>

    <b>4. Carga total requerida (Q):</b><br>
    $$ Q = I \\cdot t = {corriente_total:.2f} \\cdot {vida_util} \\cdot 365 \\cdot 24 = {carga_total:.2f}\\ \\text{{Ah}} $$<br>

    <b>5. Eficiencia del sistema:</b><br>
    $$ \\eta = \\frac{{I_{{usada}}}}{{I_{{máxima}}}} \\cdot 100 = \\frac{{{corriente_total:.2f}}}{{{datos_rect["corriente"]}}} \\cdot 100 = {eficiencia_sistema:.1f}\\% $$<br>
    
    <b>6. Número de ánodos requeridos:</b><br>
    $$ N = \\left\\lceil \\frac{{I}}{{I_{{anodo}}}} \\right\\rceil = \\left\\lceil \\frac{{{corriente_total:.2f}}}{{{datos_anodo["corriente"]}}} \\right\\rceil = {numero_anodos} $$<br>

    <b>7. Resistencia del ánodo (Rᴀ):</b><br>
    $$ R_{{anodo}} = {resistencia_anodo:.2f}\\ \\Omega $$<br>

    <b>8. Resistencia del electrolito (Rₑ):</b><br>
    $$ R_{{electrolito}} = \\frac{{\\rho}}{{4 \\pi d}} = \\frac{{{resistividad_metros}}}{{4 \\pi \\cdot {distancia_sugerida:.2f}}} = {resistencia_electrolito:.2f}\\ \\Omega $$<br>

    <b>9. Resistencia total:</b><br>
    $$ R_{{total}} = R_{{anodo}} + R_{{electrolito}} = {resistencia_total:.2f}\\ \\Omega $$<br>

    <b>10. Voltaje requerido:</b><br>
    $$ V = I \\cdot R_{{total}} = {corriente_total:.2f} \\cdot {resistencia_total:.2f} = {voltaje_requerido:.2f}\\ \\text{{V}} $$<br>

    <b>11. Distancia estructura-ánodo:</b><br>
    $$ d = {distancia_sugerida}\\ \\text{{m}} $$
    </div>
    """, unsafe_allow_html=True)

    # Mostrar resumen aparte
    st.markdown("### 📋 Resumen del sistema ICCP")
    st.markdown(f"""
- _**Densidad de corriente:**_ **{densidad_iccp:.3f} A/m²**  
- _**Corriente total requerida:**_ **{corriente_total:.2f} A**  
- _**Carga total (Ah):**_ **{carga_total:.1f} Ah**  
- _**Eficiencia del sistema:**_ **{eficiencia_sistema:.1f}%**  
- _**Rectificador seleccionado:**_ **{modelo_rectificador}**  
- _**Tipo de ánodo:**_ **{tipo_anodo}**  
- _**Número de ánodos requeridos:**_ **{numero_anodos}**  
- _**Resistencia total estimada:**_ **{resistencia_total:.2f} Ω**  
- _**Voltaje requerido:**_ **{voltaje_requerido:.2f} V**  
- _**Cable recomendado:**_ **{cable_sugerido}**  

    
- _**Electrodo de referencia:**_ **{tipo_electrodo}**
""")

