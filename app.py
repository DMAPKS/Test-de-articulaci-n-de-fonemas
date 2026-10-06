import streamlit as st

# Configuración de la página en ancho completo
st.set_page_config(
    page_title="Test de Articulación de Fonemas",
    page_icon="🗣️",
    layout="wide"
)

st.title("🗣️ Lámina Interactiva de Fonemas")
st.write("Haz clic sobre cada cuadro de fonema para alternar su estado de evaluación.")

# Definición de los grupos de fonemas
grupos_fonemas = {
    "Vocales y Diptongo": ["/a/", "/e/", "/i/", "/o/", "/u/", "dip"],
    "Consonantes": ["/p/", "/m/", "/b/", "/t/", "/d/", "/f/", "/k/", "/l/", "/n/", "/ch/", "/g/", "/ñ/", "/y/", "/j/", "/s/"],
    "Líquidas y Trabantes": ["/r/", "/ua/", "/bl/", "/pl/", "/tl/", "/lt/", "/ls/", "/mp/", "/mb/", "/sm/", "/sp/", "/sk/", "/st/"],
    "Sínfones / Fonosucesiones": ["/fl/", "/kl/", "/gl/", "/nd/", "/nt/", "/ns/", "/tr/", "/br/", "/pr/", "/fr/", "/kr/", "/gr/", "/dr/", "/rm/", "/rd/", "/rb/", "/rt/", "/rk/", "/mbr/", "/mpr/", "/str/", "/skr/"]
}

# Inicializar estados en la sesión
todos_los_tokens = [f for lista in grupos_fonemas.values() for f in lista]

if "estados_interactivos" not in st.session_state:
    st.session_state.estados_interactivos = {token: "🟢 Logra" for token in todos_los_tokens}

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
st.markdown("### 📋 Leyenda de Estados")
st.markdown("🟢 **Logra** | 🟡 **No logra** | 🟠 **Omisión** | 🔴 **Distorsión**")
st.markdown("---")

# Renderizado del tablero interactivo
for categoria, tokens in grupos_fonemas.items():
    st.markdown(f"### {categoria}")
    
    elementos_por_fila = 8
    filas = [tokens[i:i + elementos_por_fila] for i in range(0, len(tokens), elementos_por_fila)]
    
    for fila in filas:
        cols = st.columns(elementos_por_fila)
        for idx, token in enumerate(fila):
            estado_actual = st.session_state.estados_interactivos[token]
            
            # Etiqueta que muestra el fonema y su estado actual claramente en el botón
            label_boton = f"{token}\n{estado_actual}"
            
            with cols[idx]:
                if st.button(label_boton, key=f"btn_fonema_{token}", use_container_width=True):
                    # Rotación cíclica de estados al hacer clic
                    if estado_actual == "🟢 Logra":
                        st.session_state.estados_interactivos[token] = "🟡 No logra"
                    elif estado_actual == "🟡 No logra":
                        st.session_state.estados_interactivos[token] = "🟠 Omisión"
                    elif estado_actual == "🟠 Omisión":
                        st.session_state.estados_interactivos[token] = "🔴 Distorsión"
                    else:
                        st.session_state.estados_interactivos[token] = "🟢 Logra"
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
        
        alteraciones = {t: e for t, e in st.session_state.estados_interactivos.items() if "Logra" not in e}
        if alteraciones:
            st.warning(f"Se registraron **{len(alteraciones)}** fonemas con alteraciones:")
            for t, e in alteraciones.items():
                st.write(f"- **{t}**: {e}")
        else:
            st.balloons()
            st.success("🎉 ¡Excelente desempeño! Sin alteraciones detectadas.")
