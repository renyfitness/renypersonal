import streamlit as st
import math

st.set_page_config(page_title="Calculador de Ánodos", layout="centered")

st.title("🔩 Calculador de Ánodos para Protección Catódica")
st.markdown("---")

# Entradas del usuario
st.header("1. Parámetros de diseño")
area = st.number_input("Área total a proteger (m²):", min_value=0.0, step=0.1)
salinidad = st.number_input("Salinidad (ppt):", min_value=0.0, step=0.1)
vida_util = st.number_input("Vida útil deseada (años):", min_value=1, value=10)
recubrimiento = st.radio("¿La estructura está recubierta?", ("Sí", "No"))
conoce_anodo = st.radio("¿Conoces el tipo de ánodo que deseas usar?", ("No", "Sí"))

# Selección o sugerencia de ánodo
tipo_anodo = ""
peso_anodo = 5.3
capacidad_ah_kg = 2500

if conoce_anodo == "Sí":
    tipo_anodo = st.text_input("Ingresa el tipo de ánodo (ej. FAL-5.3/SO):")
    peso_anodo = st.number_input("Peso neto del ánodo (kg):", min_value=0.1, value=5.3)
    capacidad_ah_kg = st.number_input("Capacidad del ánodo (Ah/kg):", min_value=500, value=2500)
else:
    if salinidad < 1:
        tipo_anodo = "Magnesio AZ63D"
        capacidad_ah_kg = 1200
        peso_anodo = 5.0
    elif salinidad < 17:
        tipo_anodo = "Zinc"
        capacidad_ah_kg = 780
        peso_anodo = 5.0
    else:
        tipo_anodo = "Aluminio tipo barra"
        capacidad_ah_kg = 2500
        peso_anodo = 5.3
    st.info(f"Ánodo sugerido: {tipo_anodo} ({peso_anodo} kg, {capacidad_ah_kg} Ah/kg)")

# Cálculo
st.markdown("---")
st.header("2. Resultados del cálculo")
if area > 0:
    # Densidad de corriente
    if recubrimiento == "Sí":
        densidad_corriente = 0.01  # 10 mA/m²
    else:
        densidad_corriente = 0.1   # 100 mA/m²

    corriente = area * densidad_corriente  # A
    horas = vida_util * 365 * 24
    carga_total = corriente * horas  # Ah

    eficiencia = 0.90
    capacidad_util_anodo = capacidad_ah_kg * peso_anodo * eficiencia
    numero_anodos = math.ceil(carga_total / capacidad_util_anodo)

    st.success(f"Corriente requerida: {corriente:.3f} A")
    st.success(f"Carga total requerida: {carga_total:.1f} Ah")
    st.success(f"Ánodo seleccionado: {tipo_anodo} ({peso_anodo} kg)")
    st.success(f"Capacidad útil por ánodo: {capacidad_util_anodo:.1f} Ah")
    st.success(f"Número de ánodos necesarios: {numero_anodos}")
else:
    st.warning("Por favor ingresa un área válida para realizar el cálculo.")
