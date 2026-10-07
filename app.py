import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io

# Configuración de la página
st.set_page_config(
    page_title="Configuración de Evaluación Fonológica",
    page_icon="🗣️",
    layout="wide"
)

st.title("Matriz Fonológica - Análisis y Niveles del Lenguaje")
st.write("Haz clic sobre cada fonema para cambiar su estado y generar el gráfico final.")

# Filas de fonemas estructuradas exactamente como en tu lámina
filas_fonemas = [
    ["/a/", "/e/", "/i/", "/o/", "/u/", "dip"],
    ["/p/", "/m/", "/b/", "/t/", "/d/", "/f/", "/k/", "/l/", "/n/", "/ch/"],
    ["/g/", "/ñ/", "/y/", "/j/", "/s/"],
    ["/r/", "/ua/", "/bl/", "/pl/", "/tl/", "/lt/", "/ls/", "/mp/", "/mb/", "/sm/", "/sp/", "/sk/", "/st/"],
    ["/fl/", "/kl/", "/gl/", "/nd/", "/nt/", "/ns/"],
    ["/rr/", "/br/", "/pr/", "/fr/", "/kr/", "/gr/", "/dr/", "/tr/", "/rm/", "/rd/", "/rb/", "/rt/", "/rk/", "/mbr/", "/mpr/", "/str/", "/skr/"]
]

todos_los_tokens = [token for fila in filas_fonemas for token in fila]

if "estados_matriz" not in st.session_state:
    st.session_state.estados_matriz = {token: "Logra" for token in todos_los_tokens}

# Leyenda de estados superior idéntica a tu video
st.markdown("### Leyenda de Estados")
cols_leyenda = st.columns(4)
with cols_leyenda[0]:
    st.markdown("🟢 **Logra**")
with cols_leyenda[1]:
    st.markdown("🔴 **No logra**")
with cols_leyenda[2]:
    st.markdown("⚪ **No valorado**")
with cols_leyenda[3]:
    st.markdown("🔵 **No esperado para su edad**")

st.markdown("---")

# Diccionario de colores para los estados
colores_map = {
    "Logra": {"bg": "#d4edda", "border": "#c3e6cb", "text": "#155724"},
    "No logra": {"bg": "#f8d7da", "border": "#f5c6cb", "text": "#721c24"},
    "No valorado": {"bg": "#e2e3e5", "border": "#d6d8db", "text": "#383d41"},
    "No esperado": {"bg": "#cce5ff", "border": "#b8daff", "text": "#004085"}
}

# Generar estilos CSS dinámicos para que cada botón tome el color exacto de su estado y se adapte en tablets
css_botones = """
<style>
/* Estilo base para todos los botones de la matriz */
.stButton button {
    width: 100% !important;
    border-radius: 6px !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    padding: 6px 2px !important;
    min-height: 48px !important;
    line-height: 1.2 !important;
    white-space: normal !important;
    word-break: break-word !important;
}
"""

# Inyectar clases CSS personalizadas por estado para colorear los botones por completo
for token in todos_los_tokens:
    est = st.session_state.estados_matriz[token]
    c_info = colores_map[est]
    # Limpiar caracteres especiales del token para usarlos en el selector CSS de Streamlit
    safe_key = token.replace("/", "").replace("...", "").replace(" ", "_")
    css_botones += f"""
    button[key*="{safe_key}"] {{
        background-color: {c_info["bg"]} !important;
        color: {c_info["text"]} !important;
        border: 1px solid {c_info["border"]} !important;
    }}
    button[key*="{safe_key}"]:hover {{
        background-color: {c_info["border"]} !important;
        color: {c_info["text"]} !important;
        border: 1px solid {c_info["text"]} !important;
    }}
    """

css_botones += "</style>"
st.markdown(css_botones, unsafe_allow_html=True)

# Renderizado del tablero interactivo por filas adaptado a tablets
for i, fila in enumerate(filas_fonemas):
    cols = st.columns(len(fila))
    for idx, token in enumerate(fila):
        estado = st.session_state.estados_matriz[token]
        
        if estado == "Logra":
            ico = "🟢"
        elif estado == "No logra":
            ico = "🔴"
        elif estado == "No valorado":
            ico = "⚪"
        else:
            ico = "🔵"
            
        with cols[idx]:
            if st.button(f"{token}\n{ico}", key=f"mat_{i}_{idx}_{token}", use_container_width=True):
                if estado == "Logra":
                    st.session_state.estados_matriz[token] = "No logra"
                elif estado == "No logra":
                    st.session_state.estados_matriz[token] = "No valorado"
                elif estado == "No valorado":
                    st.session_state.estados_matriz[token] = "No esperado"
                else:
                    st.session_state.estados_matriz[token] = "Logra"
                st.rerun()

st.markdown("---")

# Función para generar la imagen PNG con separación real entre cajitas
def generar_grafico_matriz(estados):
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.set_xlim(0, 18.5)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Dibujar Leyenda superior en el gráfico de forma balanceada
    leyendas = [
        ("Logra", "#d4edda", "#155724", 0.6),
        ("No logra", "#f8d7da", "#721c24", 4.8),
        ("No valorado", "#e2e3e5", "#383d41", 9.0),
        ("No esperado para su edad", "#cce5ff", "#004085", 13.2)
    ]
    for lbl, bg_l, tx_l, x_pos in leyendas:
        ax.add_patch(patches.Circle((x_pos, 7.3), 0.15, facecolor=bg_l, edgecolor=tx_l, linewidth=1.5))
        ax.text(x_pos + 0.3, 7.3, lbl, fontsize=10, va='center', fontweight='bold', color='#333333')

    # Dibujar filas de fonemas con separación real y visible
    y_start = 6.0
    row_height = 0.9
    
    box_width = 0.72   
    box_height = 0.6   
    step_x = 0.86      
    
    for i, fila in enumerate(filas_fonemas):
        x_start = 0.6
        y_pos = y_start - (i * row_height)
        for token in fila:
            est = estados[token]
            c_info = colores_map[est]
            
            # Mapeo clave interna para el reporte gráfico
            bg_col = c_info["bg"]
            ed_col = c_info["border"]
            tx_col = c_info["text"]
            
            rect = patches.FancyBboxPatch(
                (x_start, y_pos), box_width, box_height,
                boxstyle="round,pad=0.02,rounding_size=0.1",
                facecolor=bg_col,
                edgecolor=ed_col,
                linewidth=1.5
            )
            ax.add_patch(rect)
            
            ax.text(x_start + (box_width / 2.0), y_pos + (box_height / 2.0), token, color=tx_col, 
                    fontsize=9.5, fontweight='bold', ha='center', va='center')
            
            x_start += step_x

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight', dpi=300)
    buf.seek(0)
    plt.close(fig)
    return buf.getvalue()

# Botón central inferior idéntico al de tu video ("GENERAR GRÁFICO (PNG)")
col_cent = st.columns([1, 2, 1])
with col_cent[1]:
    if st.button("GENERAR GRÁFICO (PNG)", type="primary", use_container_width=True):
        img_bytes = generar_grafico_matriz(st.session_state.estados_matriz)
        
        st.success("¡Gráfico generado exitosamente!")
        st.image(img_bytes, caption="Matriz Fonológica Resultante", use_container_width=True)
        
        st.download_button(
            label="📥 Descargar Imagen PNG",
            data=img_bytes,
            file_name="Matriz_Fonologica_Resultado.png",
            mime="image/png",
            use_container_width=True
        )
