import streamlit as st

# Configuración de la página en ancho completo
st.set_page_config(
    page_title="Test de Articulación de Fonemas - Lámina Interactiva",
    page_icon="🗣️",
    layout="wide"
)

# Estilo visual personalizado para imitar la lámina gráfica
st.markdown("""
    <style>
    .stButton button {
        border-radius: 8px;
        font-weight: bold;
        border: 1px solid rgba(49, 51, 63, 0.2);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🗣️ Lámina Gráfica Interactiva de Fonemas")
st.write("Haz clic directamente en cualquier tarjeta de fonema para alternar su estado de evaluación.")

# Definición de los grupos de fonemas en formato de arreglo gráfico
grupos_fonemas = {
    "Vocales y Diptongo": ["/a/", "/e/", "/i/", "/o/", "/u/", "dip"],
    "Consonantes Principales": ["/p/", "/m/", "/b/", "/t/", "/d/", "/f/", "/k/", "/l/", "/n/", "/ch/", "/g/", "/ñ/", "/y/", "/j/", "/s/"],
    "Líquidas y Trabantes": ["/r/", "/ua/", "/bl/", "/pl/", "/tl/", "/lt/", "/ls/", "/mp/", "/mb/", "/sm/", "/sp/", "/sk/", "/st/"],
    "Fonosucesiones / Sínfones": ["/fl/", "/kl/", "/gl/", "/nd/", "/nt/", "/ns/", "/tr/", "/br/", "/pr/", "/fr/", "/kr/", "/gr/", "/dr/", "/rm/", "/rd/", "/rb/", "/rt/", "/rk/", "/mbr/", "/mpr/", "/str/", "/skr/"]
}

# Inicializar los estados en la sesión
todos_los_tokens = [f for lista in grupos_fonemas.values() for f in lista]

if "estados_graficos" not in st.session_state:
    st.session_state.estados_graficos = {token: "Logra 🟢" for token in todos_los_tokens}

# Barra superior de datos generales
with st.container():
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1:
        nombre_paciente = st.text_input("Nombre del paciente o alumno:")
    with c2:
        edad = st.number_input("Edad:", min_value=1, max_value=18, value=5)
    with c3:
        evaluador = st.text_input("Terapeuta / Evaluador:")

st.markdown("---")

# Leyenda de referencia gráfica
st.markdown("### 📋 Leyenda de Estados")
st.caption("🟢 **Logra** (Correcto) ➔ 🟡 **No logra** (Sustitución) ➔ 🟠 **Omisión** ➔ 🔴 **Distorsión**")

# Generación del arreglo gráfico por categorías y filas
for categoria, tokens in grupos_fonemas.items():
    st.subheader(f"📌 {categoria}")
    
    # Distribución en filas de 6 elementos para mantener el orden de la lámina
    elementos_por_fila = 6
    filas = [tokens[i:i + elementos_por_fila] for i in range(0, len(tokens), elementos_por_fila)]
    
    for fila in filas:
        cols = st.columns(elementos_por_fila)
        for idx, token in enumerate(fila):
            estado_actual = st.session_state.estados_graficos[token]
            
            # Formato visual corto para que luzca limpio en la tarjeta
            if "Logra" in estado_actual:
                etiqueta_boton = f"{token}\n🟢"
            elif "No logra" in estado_actual:
                etiqueta_boton = f"{token}\n🟡"
            elif "Omisión" in estado_actual:
                etiqueta_boton = f"{token}\n🟠"
            else:
                etiqueta_boton = f"{token}\n🔴"

            with cols[idx]:
                if st.button(etiqueta_boton, key=f"graf_{token}", use_container_width=True):
                    # Rotar estados al hacer clic de forma cíclica
                    if "Logra" in estado_actual:
                        st.session_state.estados_graficos[token] = "No logra 🟡"
                    elif "No logra" in estado_actual:
                        st.session_state.estados_graficos[token] = "Omisión 🟠"
                    elif "Omisión" in estado_actual:
                        st.session_state.estados_graficos[token] = "Distorsión 🔴"
                    else:
                        st.session_state.estados_graficos[token] = "Logra 🟢"
                    st.rerun()

st.markdown("---")

# Observaciones y Guardado
st.subheader("📝 Observaciones Clínicas")
observaciones = st.text_area("Anota detalles de la evaluación fonológica:")

if st.button("💾 Guardar y Procesar Evaluación", type="primary", use_container_width=True):
    if not nombre_paciente.strip():
        st.warning("⚠️ Por favor, ingresa el nombre del paciente antes de guardar.")
    else:
        st.success(f"¡Evaluación registrada exitosamente para **{nombre_paciente}**!")
        
        # Filtrar alteraciones detectadas
        alteraciones = {t: e for t, e in st.session_state.estados_graficos.items() if "Logra" not in e}
        
        if alteraciones:
            st.warning(f"Se detectaron **{len(alteraciones)}** elementos con alteraciones:")
            for token, estado in alteraciones.items():
                st.write(f"- **{token}**: {estado}")
        else:
            st.balloons()
            st.success("🎉 ¡Excelente desempeño! No se registraron alteraciones fonológicas.")
