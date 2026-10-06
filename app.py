import streamlit as st
from datetime import datetime

# Configuración de la página
st.set_page_config(
    page_title="Test de Articulación de Fonemas",
    page_icon="🗣️",
    layout="wide"
)

# Estilos CSS para simular exactamente el diseño de tarjetas de la lámina
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
        padding: 6px 2px;
    }
    .card-logra { background-color: #d4edda !important; color: #155724 !important; border: 1px solid #c3e6cb !important; }
    .card-nologra { background-color: #f8d7da !important; color: #721c24 !important; border: 1px solid #f5c6cb !important; }
    .card-valorado { background-color: #e2e3e5 !important; color: #383d41 !important; border: 1px solid #d6d8db !important; }
    .card-esperado { background-color: #cce5ff !important; color: #004085 !important; border: 1px solid #b8daff !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🗣️️ Lámina Interactiva de Articulación de Fonemas")
st.write("Haz clic en cada fonema para alternar su estado de evaluación.")

# Filas de fonemas estructuradas exactamente igual que tu lámina
filas_fonemas = [
    ["/a/", "/e/", "/i/", "/o/", "/u/", "dip"],
    ["/p/", "/m/", "/b/", "/t/", "/d/", "/f/", "/k/", "/l/", "/n/", "/ch/"],
    ["/g/", "/ñ/", "/y/", "/j/", "/s/"],
    ["/r/", "/ua/", "/bl/", "/pl/", "/tl/", "/lt/", "/ls/", "/mp/", "/mb/", "/sm/", "/sp/", "/sk/", "/st/"],
    ["/fl/", "/kl/", "/gl/", "/nd/", "/nt/", "/ns/"],
    ["/rr/", "/br/", "/pr/", "/fr/", "/kr/", "/gr/", "/dr/", "/tr/", "/rm/", "/rd/", "/rb/", "/rt/", "/rk/", "/mbr/", "/mpr/", "/str/", "/skr/"]
]

todos_los_tokens = [token for fila in filas_fonemas for token in fila]

if "estados_tablero" not in st.session_state:
    st.session_state.estados_tablero = {token: "Logra" for token in todos_los_tokens}

# Datos del paciente
with st.container():
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1:
        nombre_paciente = st.text_input("Nombre del paciente o alumno:", value="")
    with c2:
        edad = st.number_input("Edad:", min_value=1, max_value=18, value=5)
    with c3:
        evaluador = st.text_input("Terapeuta / Evaluador:", value="")

st.markdown("---")

# Leyenda visual idéntica a la parte superior de tu imagen
st.markdown("### 📋 Leyenda de Estados")
st.markdown("🟢 **Logra** &nbsp;&nbsp;|&nbsp;&nbsp; 🔴 **No logra** &nbsp;&nbsp;|&nbsp;&nbsp; ⚪ **No valorado** &nbsp;&nbsp;|&nbsp;&nbsp; 🔵 **No esperado para su edad**")
st.markdown("---")

# Renderizar filas interactivas del tablero
st.markdown("### 🎛️ Tablero de Evaluación")

for i, fila in enumerate(filas_fonemas):
    cols = st.columns(len(fila))
    for idx, token in enumerate(fila):
        estado_actual = st.session_state.estados_tablero[token]
        
        # Asignar etiqueta e icono
        if estado_actual == "Logra":
            ico = "🟢 Logra"
        elif estado_actual == "No logra":
            ico = "🔴 No logra"
        elif estado_actual == "No valorado":
            ico = "⚪ No valorado"
        else:
            ico = "🔵 No esperado"
            
        with cols[idx]:
            if st.button(f"{token}\n{ico}", key=f"token_{i}_{idx}_{token}", use_container_width=True):
                # Ciclo de estados al hacer clic
                if estado_actual == "Logra":
                    st.session_state.estados_tablero[token] = "No logra"
                elif estado_actual == "No logra":
                    st.session_state.estados_tablero[token] = "No valorado"
                elif estado_actual == "No valorado":
                    st.session_state.estados_tablero[token] = "No esperado"
                else:
                    st.session_state.estados_tablero[token] = "Logra"
                st.rerun()

st.markdown("---")

# Sección de resultados y vista de impresión para obtener la lámina final
st.subheader("🖼️ Vista de la Lámina Resultante y Reporte")

if not nombre_paciente.strip():
    st.warning("⚠️ Ingresa el nombre del paciente para generar la lámina y el reporte final.")
else:
    st.success(f"Lámina lista para el paciente: **{nombre_paciente}**")
    
    # Contenedor visual tipo lámina final para captura o impresión
    st.markdown("### 📄 Formato de Lámina Evaluada")
    
    html_lamina = f"""
    <div style="border: 2px solid #ccc; padding: 20px; border-radius: 10px; background-color: #fafafa; color: #333;">
        <h3>Test de Articulación de Fonemas - Resultados</h3>
        <p><b>Paciente:</b> {nombre_paciente} | <b>Edad:</b> {edad} años | <b>Evaluador:</b> {evaluador if evaluador else 'N/A'}</p>
        <hr>
    """
    
    for fila in filas_fonemas:
        html_lamina += "<div style='display: flex; gap: 8px; margin-bottom: 8px; flex-wrap: wrap;'>"
        for token in fila:
            est = st.session_state.estados_tablero[token]
            # Colores de fondo equivalentes
            bg = "#d4edda" if est == "Logra" else "#f8d7da" if est == "No logra" else "#e2e3e5" if est == "No valorado" else "#cce5ff"
            col = "#155724" if est == "Logra" else "#721c24" if est == "No logra" else "#383d41" if est == "No valorado" else "#004085"
            
            html_lamina += f"""
            <div style="background-color: {bg}; color: {col}; border: 1px solid #ccc; padding: 6px 10px; border-radius: 6px; text-align: center; font-weight: bold; min-width: 60px;">
                {token}<br><span style="font-size: 10px;">{est}</span>
            </div>
            """
        html_lamina += "</div>"
        
    html_lamina += "</div>"
    
    st.markdown(html_lamina, unsafe_allow_html=True)
    st.info("💡 **Tip para guardar como imagen o PDF:** Puedes presionar las teclas `Ctrl + P` (o `Cmd + P` en Mac) en tu navegador y seleccionar **'Guardar como PDF'** o hacer una captura de pantalla de este recuadro para conservar tu lámina evaluada con el formato gráfico exacto.")
