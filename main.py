import streamlit as st
import random

# Configuración de página
st.set_page_config(page_title="ANALYTICA | Bio-Performance", page_icon="📊")

# Estilo visual Pro
st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div.stButton > button:first-child {
        background-color: #00FFC8;
        color: black;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("ANALYTICA 📊")
st.caption("Nutrición Basada en Evidencia - Estándar NHANES 2025")

# --- LISTAS DE COMIDAS ---
pre_entrenos = [
    "🍌 1 Banana madura + 1 puñado de frutos secos.",
    "🍞 2 Tostadas integrales con miel y rodajas de fruta.",
    "🥣 3 cdas de avena instantánea con leche y canela.",
    "🍎 1 Manzana + 1 barrita de cereal de buena calidad."
]

post_entrenos = [
    "🍗 1 Pechuga de pollo + 1 taza de arroz blanco + calabaza.",
    "🍳 Omelette de 3 huevos + 1 lata de atún al natural + 1 tostada.",
    "🍚 1 bife de cuadril magro + 1 papa mediana al horno.",
    "🍦 Yogur natural descremado + 1 fruta + granola."
]

# --- SIDEBAR: DATOS ---
with st.sidebar:
    st.header("Configuración")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    peso = st.number_input("Peso (kg)", 40.0, 150.0, 75.0)
    talla = st.number_input("Talla (m)", 1.40, 2.10, 1.75)
    brazo = st.number_input("Brazo Contraído (cm)", 15.0, 60.0, 32.0)
    hora_gym = st.time_input("Hora de inicio del Gym")

# --- CÁLCULOS ---
imc = peso / (talla**2)
ajuste = 7.0 if imc >= 30 else (3.5 if imc >= 25 else 0)
brazo_final = brazo - ajuste

# --- MOSTRAR RESULTADOS ---
st.write("---")
col1, col2 = st.columns(2)
col1.metric("IMC", f"{imc:.1f}")
col2.metric("Brazo Ajustado", f"{brazo_final:.1f} cm")

# Mensaje de Diagnóstico
if brazo_final >= (28 if sexo == "Masculino" else 25):
    st.success("✅ Nivel de masa muscular adecuado.")
else:
    st.warning("⚠️ Masa muscular por debajo del punto de corte óptimo.")

# --- SECCIÓN DE COMIDAS CON BOTÓN DE INTERCAMBIO ---
st.write("---")
st.subheader("🕒 Recomendación según tu horario")

# Inicializar estados de las comidas si no existen
if 'pre_idx' not in st.session_state: st.session_state.pre_idx = 0
if 'post_idx' not in st.session_state: st.session_state.post_idx = 0

# Fila para Pre-Entreno
st.markdown(f"**Pre-Entreno (90 min antes):**")
st.info(pre_entrenos[st.session_state.pre_idx])
if st.button("🔄 Cambiar opción de Pre-Entreno"):
    st.session_state.pre_idx = (st.session_state.pre_idx + 1) % len(pre_entrenos)
    st.rerun()

# Fila para Post-Entreno
st.markdown(f"**Post-Entreno (Al finalizar):**")
st.success(post_entrenos[st.session_state.post_idx])
if st.button("🔄 Cambiar opción de Post-Entreno"):
    st.session_state.post_idx = (st.session_state.post_idx + 1) % len(post_entrenos)
    st.rerun()
    
# --- SECCIÓN DE RESPALDO CIENTÍFICO ---
with st.expander("🔬 ¿Por qué medimos el brazo? (Base Científica)"):
    st.write("""
        Esta herramienta no utiliza el IMC convencional, ya que este no distingue entre grasa y músculo. 
        En su lugar, aplicamos los **puntos de corte del estudio NHANES 2025** (*Costa-Pereira et al.*).
        
        **Puntos clave del método:**
        1. **Precisión:** La circunferencia del brazo (MUAC) tiene una correlación del 70-80% con la masa muscular esquelética total.
        2. **Ajuste por Grasa:** Aplicamos una corrección matemática según tu IMC para 'filtrar' el tejido adiposo y medir solo el tejido magro.
        3. **Referencia:** Comparamos tu medida con una base de datos de más de 18.000 personas para determinar si estás en un rango de hipertrofia óptimo.
    """)
    st.caption("Fuente: Arm circumference as a marker of muscle mass: cutoff values from NHANES 1999–2006 (AJCN, 2025).")

# --- BOTÓN WHATSAPP ---
st.write("---")
whatsapp_url = "https://wa.me/5491136768018?text=Hola!%20Usé%20Analytica%20y%20quiero%20mejorar%20mi%20masa%20muscular."
st.link_button("🔥 SOLICITAR ASESORÍA 1-A-1", whatsapp_url, use_container_width=True)
