import streamlit as st
import pandas as pd

# Configuración de página con estilo oscuro
st.set_page_config(page_title="ANALYTICA | Bio-Performance", page_icon="📊")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #00FFC8; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("ANALYTICA 📊")
st.subheader("Evaluación de Masa Muscular (NHANES 2025)")

# --- SECCIÓN DE ENTRADA ---
with st.sidebar:
    st.header("Datos Biométricos")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    edad = st.number_input("Edad", 18, 80, 25)
    peso = st.number_input("Peso (kg)", 40.0, 150.0, 75.0)
    talla = st.number_input("Talla (m)", 1.40, 2.10, 1.75)
    brazo = st.number_input("Perímetro de Brazo (cm)", 15.0, 60.0, 32.0)
    
    st.header("Entrenamiento")
    hora_gym = st.time_input("Hora de inicio")
    duracion = st.slider("Duración (min)", 30, 180, 90)

# --- LÓGICA DEL PAPER ---
imc = peso / (talla**2)
ajuste = 0
if imc >= 30: ajuste = 7.0
elif imc >= 25: ajuste = 3.5

brazo_ajustado = brazo - ajuste

# --- RESULTADOS ---
st.write("---")
col1, col2 = st.columns(2)
col1.metric("IMC", f"{imc:.1f}")
col2.metric("Brazo Ajustado (Músculo)", f"{brazo_ajustado:.1f} cm")

if brazo_ajustado >= 28 if sexo == "Masculino" else 25:
    st.success("✅ Nivel de masa muscular adecuado según estándar NHANES.")
else:
    st.warning("⚠️ Masa muscular por debajo del punto de corte óptimo.")

# --- RECOMENDACIÓN TIMING ---
st.subheader("🕒 Recomendación de Timing")
st.info(f"**Pre-Entreno:** Priorizá carbohidratos complejos 90 min antes de las {hora_gym.strftime('%H:%M')}.")
st.info(f"**Post-Entreno:** Ventana de recuperación proteica recomendada al finalizar.")

# --- BOTÓN DE CONVERSIÓN WHATSAPP ---
st.markdown("---")
st.markdown("### 🚀 ¿Querés optimizar estos resultados?")
st.write("Recibí un plan 100% personalizado basado en tu biometría.")
whatsapp_url = "https://wa.me/TU_NUMERO_ACA?text=Hola!%20Usé%20Analytica%20y%20quiero%20mi%20plan%20personalizado."
st.link_button("AGENDAR CONSULTA 1-A-1", whatsapp_url)
