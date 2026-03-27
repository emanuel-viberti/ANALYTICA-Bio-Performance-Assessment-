import streamlit as st
from datetime import datetime, timedelta
import urllib.parse

# 1. IDENTIDAD
st.set_page_config(page_title="ANALYTICA", page_icon="📊", layout="centered")

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
st.caption("Nutrición Basada en Evidencia - Estándar NHANES 2026")

# 2. SIDEBAR
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

# 3. LÓGICA DE CÁLCULO
imc = peso / (talla**2)
ajuste = 7.0 if imc >= 30 else (3.5 if imc >= 25 else 0)
brazo_final = brazo - ajuste

def round_5(x):
    return int(5 * round(float(x)/5))

# 4. DIAGNÓSTICO ESTRATIFICADO
st.write("---")
col1, col2 = st.columns(2)
col1.metric("IMC", f"{imc:.1f}")
col2.metric("Brazo Ajustado", f"{brazo_final:.1f} cm")

if sexo == "Masculino":
    if brazo_final < 28:
        st.warning("⚠️ **Bajo el óptimo:** Tu masa muscular está por debajo del estándar de salud. ¡Hora de entrenar fuerte!")
    elif 28 <= brazo_final <= 32:
        st.success("✅ **Nivel Adecuado:** Tenés una base muscular saludable. ¡Hay margen para llegar al alto rendimiento!")
    else:
        st.balloons()
        st.info("🚀 **Alto Rendimiento:** ¡Nivel de hipertrofia sobresaliente! Estás en el rango superior de la población.")
else:
    if brazo_final < 25:
        st.warning("⚠️ **Bajo el óptimo:** Fortalecer tu masa muscular ayudará a proteger tu salud metabólica.")
    elif 25 <= brazo_final <= 29:
        st.success("✅ **Nivel Adecuado:** Composición muscular óptima. ¡Podés seguir escalando hacia la excelencia!")
    else:
        st.balloons()
        st.info("🚀 **Alto Rendimiento:** Excelente desarrollo de tejido magro. Rendimiento deportivo de élite.")

# 5. MENÚS (4 OPCIONES + REDONDEO)
dt_gym = datetime.combine(datetime.today(), hora_gym)
hora_pre = (dt_gym - timedelta(minutes=90)).strftime("%H:%M")
hora_post = (dt_gym + timedelta(minutes=duracion)).strftime("%H:%M")
factor_dur = 1.5 if duracion > 90 else (1.2 if duracion > 60 else 1.0)
ratio_peso = peso / 70

recetas = {
    "Pesas / Hipertrofia": {
        "pre": [
            f"🥣 {round_5(40 * factor_dur)}g de avena + 1 banana + 1 cda manteca de maní.",
            f"🍞 2 tostadas integrales + 3 claras de huevo + {round_5(15 * factor_dur)}g de miel.",
            f"🥞 Pancakes: 1 huevo + 2 claras + {round_5(40 * factor_dur)}g de harina de avena.",
            f"🥛 Yogur griego + {round_5(30 * factor_dur)}g de granola + 1 fruta picada."
        ],
        "post": [
            f"🍗 {round_5(150 * ratio_peso)}g de pollo + {round_5(200 * factor_dur)}g de arroz blanco.",
            f"🍳 Omelette de 3 huevos + 1 lata de atún + 2 rodajas de pan integral.",
            f"🥩 {round_5(150 * ratio_peso)}g de carne magra + {round_5(200 * factor_dur)}g de puré de papa.",
            f"🍝 {round_5(100 * factor_dur)}g de fideos secos + {round_5(120 * ratio_peso)}g de carne picada."
        ]
    },
    "Running / HIIT": {
        "pre": [
            f"🍌 1 banana grande + {round_5(40 * factor_dur)}g de dulce de membrillo.",
            f"🥪 Sándwich de pan blanco con mermelada y queso untable.",
            f"🥣 {round_5(50 * factor_dur)}g de cereales de maíz + leche descremada.",
            f"🥤 Licuado de agua con 1 manzana + {round_5(15 * factor_dur)}g de miel."
        ],
        "post": [
            f"🍝 {round_5(120 * factor_dur)}g de fideos secos con aceite de oliva y 2 huevos.",
            f"🥤 Batido: 2 frutas + 300ml leche + {round_5(40 * factor_dur)}g de cereales.",
            f"🍚 {round_5(250 * factor_dur)}g de arroz con pollo desmenuzado.",
            f"🍞 3 tostadas blancas con {round_5(100 * ratio_peso)}g de queso cottage."
        ]
    },
    "Funcional / Crossfit": {
        "pre": [
            "🍎 1 manzana + 1 yogur descremado + puñado de frutos secos.",
            "☕ 1 café + 1 tostada con queso crema y 1 huevo duro.",
            "🍐 1 pera + 2 galletas de arroz con mermelada.",
            f"🥣 {round_5(30 * factor_dur)}g de avena instantánea con agua y canela."
        ],
        "post": [
            f"🌯 Wrap de tortilla + {round_5(120 * ratio_peso)}g de proteína + legumbres.",
            f"🥗 Bowl: {round_5(150 * ratio_peso)}g de carne magra + {round_5(150 * factor_dur)}g de papa.",
            f"🍗 {round_5(150 * ratio_peso)}g de pollo + {round_5(150 * factor_dur)}g de batata al horno.",
            "🌮 2 Tacos de carne picada magra con palta y ensalada."
        ]
    }
}

st.write("---")
st.subheader(f"🍴 Menú Sugerido: {tipo_entreno}")
if 'idx' not in st.session_state: st.session_state.idx = 0
opciones_pre = recetas[tipo_entreno]["pre"]
opciones_post = recetas[tipo_entreno]["post"]

st.info(f"**Pre-Entreno ({hora_pre}):**\n\n{opciones_pre[st.session_state.idx % len(opciones_pre)]}")
st.success(f"**Post-Entreno ({hora_post}):**\n\n{opciones_post[st.session_state.idx % len(opciones_post)]}")

if st.button("🔄 Ver otra opción de menú"):
    st.session_state.idx += 1
    st.rerun()

# 6. BASE CIENTÍFICA CON TABLA DE CORTES
st.write("---")
with st.expander("🔬 Referencia y Puntos de Corte"):
    st.write("""
    Esta herramienta utiliza la **Circunferencia de Brazo Ajustada (CBA)** basada en el estándar **NHANES 2026**. 
    
    ### Tabla de Referencia Muscular:
    """)
    
    data = {
        "Nivel": ["Bajo el óptimo", "Nivel Adecuado", "Alto Rendimiento"],
        "Hombres (cm)": ["< 28.0", "28.0 - 32.0", "> 32.0"],
        "Mujeres (cm)": ["< 25.0", "25.0 - 29.0", "> 29.0"]
    }
    st.table(data)
    
    st.write("""
    **Interpretación:**
    - **Nivel Adecuado:** Estás en el rango de salud metabólica óptima.
    - **Alto Rendimiento:** Posees una reserva de masa muscular superior, ideal para atletas o personas enfocadas en la hipertrofia.
    - **Margen de Crecimiento:** Si estás en el nivel adecuado, tu objetivo es trabajar hacia el límite superior de tu rango para maximizar tu capacidad anabólica.
    """)
    st.caption("Fuente: Costa-Pereira et al. (AJCN, 2026). Análisis de población NHANES.")

# 7. WHATSAPP
mensaje_wa = f"Hola Emmanuel! Mi CBA dio {brazo_final:.1f} cm. Entreno {tipo_entreno} y quiero un plan personalizado."
mensaje_encoded = urllib.parse.quote(mensaje_wa)
st.link_button("🔥 SOLICITAR ASESORÍA PERSONALIZADA", f"https://wa.me/5491136768018?text={mensaje_encoded}", use_container_width=True)
