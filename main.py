import streamlit as st
from datetime import datetime, timedelta
import urllib.parse

# 1. CONFIGURACIÓN Y ESTILO PRO
st.set_page_config(page_title="ANALYTICA | Bio-Performance", page_icon="📊")

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

# 2. SIDEBAR (DATOS DE ENTRADA)
with st.sidebar:
    st.header("Configuración")
    sexo = st.radio("Sexo", ["Masculino", "Femenino"])
    peso = st.number_input("Peso (kg)", 40.0, 150.0, 75.0)
    talla = st.number_input("Talla (m)", 1.40, 2.10, 1.75)
    brazo = st.number_input("Brazo Contraído (cm)", 15.0, 60.0, 32.0)
    
    st.write("---")
    st.header("Tu Sesión")
    tipo_entreno = st.selectbox("Tipo de entrenamiento", ["Pesas / Hipertrofia", "Running / HIIT", "Funcional / Crossfit"])
    duracion = st.slider("Duración (minutos)", 30, 180, 60)
    hora_gym = st.time_input("Hora de inicio")

# 3. LÓGICA DE HORARIOS Y PORCIONES
dt_gym = datetime.combine(datetime.today(), hora_gym)
hora_pre = (dt_gym - timedelta(minutes=90)).strftime("%H:%M")
hora_post = (dt_gym + timedelta(minutes=duracion)).strftime("%H:%M")

factor_duracion = 1.5 if duracion > 90 else (1.2 if duracion > 60 else 1.0)
ratio_peso = peso / 70

recetas = {
    "Pesas / Hipertrofia": {
        "pre": [f"🥣 {round(40 * factor_duracion)}g de avena + 1 banana + 1 cda manteca de maní.", 
                f"🍞 2 tostadas integrales + 3 claras + {round(15 * factor_duracion)}g de miel."],
        "post": [f"🍗 {round(150 * ratio_peso)}g de pollo + {round(200 * factor_duracion)}g de arroz + vegetales.", 
                 f"🍳 Omelette de 3 huevos + 1 lata de atún + 2 rodajas de pan integral."]
    },
    "Running / HIIT": {
        "pre": [f"🍌 1 banana grande + {round(40 * factor_duracion)}g de dulce de membrillo.", 
                f"🥪 Sándwich de pan blanco con mermelada (bajo en fibra)."],
        "post": [f"🍝 {round(120 * factor_duracion)}g de fideos secos con aceite de oliva y 2 huevos.", 
                 f"🥤 Licuado: 2 frutas + 300ml leche + {round(40 * factor_duracion)}g de cereales."]
    },
    "Funcional / Crossfit": {
        "pre": ["🍎 1 manzana + 1 yogur descremado + puñado de frutos secos.", 
                "☕ 1 café + 1 tostada con queso crema y 1 huevo duro."],
        "post": [f"🌯 Wrap de tortilla + {round(120 * ratio_peso)}g de proteína + legumbres.", 
                 f"🥗 Bowl: {round(150 * ratio_peso)}g de carne magra + {round(150 * factor_duracion)}g de papa/batata."]
    }
}

# 4. CÁLCULOS BIOMÉTRICOS
imc = peso / (talla**2)
ajuste = 7.0 if imc >= 30 else (3.5 if imc >= 25 else 0)
brazo_final = brazo - ajuste
punto_corte = 28 if sexo == "Masculino" else 25

# 5. RESULTADOS
st.write("---")
col1, col2 = st.columns(2)
col1.metric("IMC", f"{imc:.1f}")
col2.metric("Brazo Ajustado", f"{brazo_final:.1f} cm")

if brazo_final >= punto_corte:
    st.success("✅ Nivel de masa muscular adecuado.")
else:
    st.warning("⚠️ Masa muscular por debajo del estándar óptimo.")

# 6. RECOMENDACIÓN DINÁMICA
st.write("---")
st.subheader(f"🍴 Plan para {tipo_entreno}")
st.caption(f"Ajustado para {duracion} min y {peso}kg de peso corporal.")

if 'idx' not in st.session_state: st.session_state.idx = 0

opciones_pre = recetas[tipo_entreno]["pre"]
opciones_post = recetas[tipo_entreno]["post"]

st.info(f"**Pre-Entreno (Consumir a las {hora_pre}):**\n\n{opciones_pre[st.session_state.idx % len(opciones_pre)]}")
st.success(f"**Post-Entreno (Consumir a las {hora_post}):**\n\n{opciones_post[st.session_state.idx % len(opciones_post)]}")

if st.button("🔄 Cambiar combinaciones"):
    st.session_state.idx += 1
    st.rerun()

# 7. GUÍA DE MEDICIÓN
st.write("---")
st.subheader("📏 Guía: Cómo medir tu brazo")
st.write("""
1. **Punto de medición:** Medí en el punto medio entre el hombro y el codo.
2. **Contracción:** Flexioná el brazo a 90° y hacé fuerza máxima (bíceps contraído).
3. **Cinta:** La cinta debe estar firme pero sin apretar la piel. Tomá la medida en la zona de mayor relieve.
""")

# 8. BASE CIENTÍFICA EXTENDIDA
with st.expander("🔬 ¿Por qué medimos el brazo? (Base Científica)"):
    st.write("""
        Esta herramienta aplica los **puntos de corte del estudio NHANES 2025** (*Costa-Pereira et al.*).
        
        **Puntos clave del método:**
        1. **Precisión:** La circunferencia del brazo (MUAC) tiene una correlación de hasta el 80% con la masa muscular esquelética total, siendo superior al IMC en contextos deportivos.
        2. **Ajuste por Grasa:** Aplicamos una corrección matemática (-3.5cm o -7cm) según tu IMC para filtrar el tejido adiposo y obtener una métrica real de hipertrofia.
        3. **Referencia Científica:** Los datos se contrastan con una base de datos de más de 18.000 sujetos para determinar rangos de funcionalidad y salud metabólica.
    """)
    st.caption("Fuente: Arm circumference as a marker of muscle mass: NHANES (AJCN, 2025).")

# 9. WHATSAPP INTELIGENTE
mensaje_wa = f"Hola Emmanuel! Usé Analytica. Mi IMC es {imc:.1f} y mi brazo ajustado dio {brazo_final:.1f} cm. Entreno {tipo_entreno} y quiero un plan personalizado."
mensaje_encoded = urllib.parse.quote(mensaje_wa)
whatsapp_url = f"https://wa.me/5491136768018?text={mensaje_encoded}"

st.link_button("🔥 SOLICITAR ASESORÍA 1-A-1", whatsapp_url, use_container_width=True)
