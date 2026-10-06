import streamlit as st

# Configuración de la página en ancho completo
st.set_page_config(
    page_title="Test de Articulación de Fonemas",
    page_icon="🗣️",
    layout="wide"
)

# Estilos CSS dinámicos para colorear el fondo completo de los botones según su estado
st.markdown("""
    <style>
    /* Estilo base para los botones de fonemas */
    .stButton button {
        width: 100%;
        border-radius: 6px;
        font-weight: 700;
        font-size: 14px;
        padding: 8px 4px;
        border: 1px solid rgba(0,0,0,0.15);
        transition: all 0.2s ease-in-out;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🗣️ Lámina de Articulación de Fonemas - Panel Gráfico")
st.write("Haz clic sobre cada tarjeta para colorear el cuadro completo y cambiar su estado de evaluación.")

# Definición de los grupos de fonemas
grupos_fonemas = {
    "Vocales y Diptongo": ["/a/", "/e/", "/i/", "/o/", "/u/", "dip"],
    "Consonantes": ["/p/", "/m/", "/b/", "/t/", "/d/", "/f/", "/k/", "/l/", "/n/", "/ch/", "/g/", "/ñ/", "/y/", "/j/", "/s/"],
    "Líquidas y Trabantes": ["/r/", "/ua/", "/bl/", "/pl/", "/tl/", "/lt/", "/ls/", "/mp/", "/mb/", "/sm/", "/sp/", "/sk/", "/st/"],
    "Sínfones / Fonosucesiones": ["/fl/", "/kl/", "/gl/", "/nd/", "/nt/", "/ns/", "/tr/", "/br/", "/pr/", "/fr/", "/kr/", "/gr/", "/dr/", "/rm/", "/rd/", "/rb/", "/rt/", "/rk/", "/mbr/", "/mpr/", "/str/", "/skr/"]
}

# Inicializar estados en la sesión
todos_los_tokens = [f for lista in grupos_fonemas.values() for f in lista]

if "estados_colores" not in st.session_state:
    st.session_state.estados_colores = {token: "🟢" for token in todos_los_tokens}

# Datos generales
with st.container():
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1:
        nombre_paciente = st.text_input("Nombre del paciente o alumno:")
    with c2:
        edad = st.number_input("Edad:", min_value=1, max_value=18, value=5)
    with c3:
        evaluador = st.text_input("Terapeuta / Evaluador:")

st.markdown("---")

# Leyenda de estados superior
st.markdown("**Leyenda (Haz clic para alternar color):** 🟢 Logra | 🟡 No logra | 🟠 Omisión | 🔴 Distorsión")
st.markdown("---")

# Renderizado del tablero con colores de fondo completos
for categoria, tokens in grupos_fonemas.items():
    st.markdown(f"### {categoria}")
    
    elementos_por_fila = 8
    filas = [tokens[i:i + elementos_por_fila] for i in range(0, len(tokens), elementos_por_fila)]
    
    for fila in filas:
        cols = st.columns(elementos_por_fila)
        for idx, token in enumerate(fila):
            estado = st.session_state.estados_colores[token]
            
            # Definir colores de fondo y texto según el estado actual
            if estado == "🟢":
                bg_color = "#d4edda"  # Verde claro
                border_color = "#c3e6cb"
                text_color = "#155724"
            elif estado == "🟡":
                bg_color = "#fff3cd"  # Amarillo claro
                border_color = "#ffeeba"
                text_color = "#856404"
            elif estado == "🟠":
                bg_color = "#ffe8d6"  # Naranja claro
                border_color = "#ffd8b8"
                text_color = "#b85d00"
            else:
                bg_color = "#f8d7da"  # Rojo claro
                border_color = "#f5c6cb"
                text_color = "#721c24"

            # Inyectar estilo visual personalizado por cada botón para pintar todo el cuadro
            st.markdown(f"""
                <style>
                div.stButton > button[key*="btn_{token}"] {{
                    background-color: {bg_color} !important;
                    color: {text_color} !important;
                    border-color: {border_color} !important;
                }}
                </style>
            """, unsafe_allow_html=True)

            with cols[idx]:
                if st.button(f"{token}", key=f"btn_{token}"):
                    # Rotación cíclica de estados al hacer clic
                    if estado == "🟢":
                        st.session_state.estados_colores[token] = "🟡"
                    elif estado == "🟡":
                        st.session_state.estados_colores[token] = "🟠"
                    elif estado == "🟠":
                        st.session_state.estados_colores[token] = "🔴"
                    else:
                        st.session_state.estados_colores[token] = "🟢"
                    st.rerun()

st.markdown("---")

# Sección de guardado y reporte
st.subheader("📝 Observaciones Clínicas")
observaciones = st.text_area("Anota detalles relevantes de la evaluación:")

if st.button("💾 Guardar Evaluación", type="primary", use_container_width=True):
    if not nombre_paciente.strip():
        st.warning("⚠️ Por favor, ingresa el nombre del paciente.")
    else:
        st.success(f"¡Evaluación guardada exitosamente para **{nombre_paciente}**!")
        
        alteraciones = {t: e for t, e in st.session_state.estados_colores.items() if e != "🟢"}
        if alteraciones:
            st.warning(f"Se registraron **{len(alteraciones)}** fonemas con alteraciones:")
            for t, e in alteraciones.items():
                st.write(f"- **{t}**: {e}")
        else:
            st.balloons()
            st.success("🎉 ¡Excelente desempeño! Sin alteraciones detectadas.")
