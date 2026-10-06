import streamlit as st

# Configuración de la página en ancho completo
st.set_page_config(
    page_title="Test de Articulación de Fonemas - Tablero Visual",
    page_icon="🗣️",
    layout="wide"
)

st.title("🗣️ Tablero Visual de Articulación de Fonemas")
st.write("Haz clic directamente sobre cualquier tarjeta de fonema para cambiar su estado de evaluación.")

# Definición de todos los grupos y fonemas según la lámina de referencia
grupos_fonemas = {
    "Vocales y Diptongo": ["/a/", "/e/", "/i/", "/o/", "/u/", "dip"],
    "Consonantes Principales": ["/p/", "/m/", "/b/", "/t/", "/d/", "/f/", "/k/", "/l/", "/n/", "/ch/", "/g/", "/ñ/", "/y/", "/j/", "/s/"],
    "Líquidas y Trabantes": ["/r/", "/ua/", "/bl/", "/pl/", "/tl/", "/lt/", "/ls/", "/mp/", "/mb/", "/sm/", "/sp/", "/sk/", "/st/"],
    "Fonosucesiones / Sínfones (L y R)": ["/fl/", "/kl/", "/gl/", "/nd/", "/nt/", "/ns/", "/tr/", "/br/", "/pr/", "/fr/", "/kr/", "/gr/", "/dr/", "/rm/", "/rd/", "/rb/", "/rt/", "/rk/", "/mbr/", "/mpr/", "/str/", "/skr/"]
}

# Inicializar los estados de todos los fonemas en la memoria de la sesión
todos_los_tokens = [f for lista in grupos_fonemas.values() for f in lista]

if "estados_tablero" not in st.session_state:
    st.session_state.estados_tablero = {token: "Logra 🟢" for token in todos_los_tokens}

# Barra superior para datos generales
with st.container():
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1:
        nombre_paciente = st.text_input("Nombre del paciente o alumno:")
    with c2:
        edad = st.number_input("Edad:", min_value=1, max_value=18, value=5)
    with c3:
        evaluador = st.text_input("Terapeuta / Evaluador:")

st.markdown("---")

# Leyenda visual de estados
st.markdown("### 📊 Leyenda de Estados (Haz clic para alternar)")
st.caption("🟢 **Logra / Correcto** ➔ 🟡 **No logra / Sustitución** ➔ 🟠 **Omisión** ➔ 🔴 **Distorsión**")

# Renderizado del tablero gráfico interactivo organizado por categorías
for categoria, tokens in grupos_fonemas.items():
    st.subheader(f"📌 {categoria}")
    
    # Creamos filas dinámicas de 6 elementos por cada fila visual
    num_columnas = 6
    filas = [tokens[i:i + num_columnas] for i in range(0, len(tokens), num_columnas)]
    
    for fila in filas:
        cols = st.columns(len(fila))
        for idx, token in enumerate(fila):
            estado_actual = st.session_state.estados_tablero[token]
            
            # Asignar un color visual o emoji representativo según el estado
            with cols[idx]:
                if st.button(f"{token}\n{estado_actual}", key=f"token_{token}", use_container_width=True):
                    # Ciclar estados al hacer clic
                    if "Logra" in estado_actual:
                        st.session_state.estados_tablero[token] = "No logra 🟡"
                    elif "No logra" in estado_actual:
                        st.session_state.estados_tablero[token] = "Omisión 🟠"
                    elif "Omisión" in estado_actual:
                        st.session_state.estados_tablero[token] = "Distorsión 🔴"
                    else:
                        st.session_state.estados_tablero[token] = "Logra 🟢"
                    st.rerun()

st.markdown("---")

# Observaciones y Botón de Guardado Final
st.subheader("📝 Observaciones Clínicas y Cierre")
observaciones = st.text_area("Anota aquí comentarios o patrones fonológicos observados:")

if st.button("💾 Guardar y Procesar Resultados", type="primary", use_container_width=True):
    if not nombre_paciente.strip():
        st.warning("⚠️ Por favor, ingresa el nombre del paciente antes de guardar.")
    else:
        st.success(f"¡Evaluación registrada correctamente para **{nombre_paciente}**!")
        
        # Filtrar alteraciones (todo lo que no sea Logra)
        alteraciones = {t: e for t, e in st.session_state.estados_tablero.items() if "Logra" not in e}
        
        if alteraciones:
            st.warning(f"Se detectaron **{len(alteraciones)}** elementos con alteraciones:")
            for token, estado in alteraciones.items():
                st.write(f"- **{token}**: {estado}")
        else:
            st.balloons()
            st.success("🎉 ¡Excelente desempeño! No se registran alteraciones fonológicas en el tablero.")
