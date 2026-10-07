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

# Dividimos la última fila larga en dos partes para que respire perfectamente y no se corte ningún texto
fila_final_1 = ["/rr/", "/br/", "/pr/", "/fr/", "/kr/", "/gr/", "/dr/", "/tr/", "/rm/"]
fila_final_2 = ["/rd/", "/rb/", "/rt/", "/rk/", "/mbr/", "/mpr/", "/str/", "/skr/"]

# Filas de fonemas estructuradas
filas_fonemas = [
    ["/a/", "/e/", "/i/", "/o/", "/u/", "dip"],
    ["/p/", "/m/", "/b/", "/t/", "/d/", "/f/", "/k/", "/l/", "/n/", "/ch/"],
    ["/g/", "/ñ/", "/y/", "/j/", "/s/"],
    ["/r/", "/ua/", "/bl/", "/pl/", "/tl/", "/lt/", "/ls/", "/mp/", "/mb/", "/sm/", "/sp/", "/sk/", "/st/"],
    ["/fl/", "/kl/", "/gl/", "/nd/", "/nt/", "/ns/"],
    fila_final_1,
    fila_final_2
]

todos_los_tokens = [token for fila in filas_fonemas for token in fila]

if "estados_matriz" not in st.session_state:
    st.session_state.estados_matriz = {token: "Logra" for token in todos_los_tokens}

# Leyenda de estados superior
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

# Mapeo exacto de colores de fondo, texto y bordes para cada estado
colores_map = {
    "Logra": {"bg": "#d4edda", "text": "#155724", "border": "#c3e6cb", "ico": "🟢"},
    "No logra": {"bg": "#f8d7da", "text": "#721c24", "border": "#f5c6cb", "ico": "🔴"},
    "No valorado": {"bg": "#e2e3e5", "text": "#383d41", "border": "#d6d8db", "ico": "⚪"},
    "No esperado": {"bg": "#cce5ff", "text": "#004085", "border": "#b8daff", "ico": "🔵"}
}

# CSS global para forzar que los botones de Streamlit adopten el color correspondiente según la clase asignada
st.markdown("""
    <style>
    /* Forzar diseño limpio y adaptable */
    .stButton button {
        width: 100% !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 12px !important;
        min-height: 48px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Generación dinámica de estilos CSS específicos por cada fonema según su estado actual
css_dinamico = "<style>\n"
for token in todos_los_tokens:
    estado = st.session_state.estados_matriz[token]
    c = colores_map[estado]
    # Limpiamos el token para usarlo de selector seguro en CSS
    token_id = token.replace("/", "").replace(" ", "_")
    css_dinamico += f"""
    button[key*="{token_id}"] {{
        background-color: {c["bg"]} !important;
        color: {c["text"]} !important;
        border: 1px solid {c["border"]} !important;
    }}
    button[key*="{token_id}"]:hover {{
        background-color: {c["border"]} !important;
        color: {c["text"]} !important;
    }}
    """
css_dinamico += "</style>"
st.markdown(css_dinamico, unsafe_allow_html=True)

# Renderizado del tablero interactivo por filas
for i, fila in enumerate(filas_fonemas):
    cols = st.columns(len(fila))
    for idx, token in enumerate(fila):
        estado = st.session_state.estados_matriz[token]
        c_info = colores_map[estado]
        
        with cols[idx]:
            token_id = token.replace("/", "").replace(" ", "_")
            btn_key = f"mat_{i}_{idx}_{token_id}"
            
            # Etiqueta limpia del botón
            label_btn = f"{token}\n{c_info['ico']}"
            
            if st.button(label_btn, key=btn_key, use_container_width=True):
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

# Función para generar la imagen PNG del reporte gráfico final agrupando la última fila de vuelta en su formato original
def generar_grafico_matriz(estados):
    fig, ax = plt.subplots(figsize=(13, 7.5))
    ax.set_xlim(0, 18.5)
    ax.set_ylim(0, 8.5)
    ax.axis('off')
    
    # Leyenda superior del gráfico
    leyendas = [
        ("Logra", "#d4edda", "#155724", 0.6),
        ("No logra", "#f8d7da", "#721c24", 4.8),
        ("No valorado", "#e2e3e5", "#383d41", 9.0),
        ("No esperado para su edad", "#cce5ff", "#004085", 13.2)
    ]
    for lbl, bg_l, tx_l, x_pos in leyendas:
        ax.add_patch(patches.Circle((x_pos, 7.8), 0.15, facecolor=bg_l, edgecolor=tx_l, linewidth=1.5))
        ax.text(x_pos + 0.3, 7.8, lbl, fontsize=10, va='center', fontweight='bold', color='#333333')

    # Reconstruimos las filas originales para que el reporte gráfico conserve el orden exacto de tu lámina
    filas_originales = [
        ["/a/", "/e/", "/i/", "/o/", "/u/", "dip"],
        ["/p/", "/m/", "/b/", "/t/", "/d/", "/f/", "/k/", "/l/", "/n/", "/ch/"],
        ["/g/", "/ñ/", "/y/", "/j/", "/s/"],
        ["/r/", "/ua/", "/bl/", "/pl/", "/tl/", "/lt/", "/ls/", "/mp/", "/mb/", "/sm/", "/sp/", "/sk/", "/st/"],
        ["/fl/", "/kl/", "/gl/", "/nd/", "/nt/", "/ns/"],
        ["/rr/", "/br/", "/pr/", "/fr/", "/kr/", "/gr/", "/dr/", "/tr/", "/rm/", "/rd/", "/rb/", "/rt/", "/rk/", "/mbr/", "/mpr/", "/str/", "/skr/"]
    ]

    y_start = 6.4
    row_height = 0.9
    box_width = 0.72   
    box_height = 0.6   
    step_x = 0.86      
    
    for i, fila in enumerate(filas_originales):
        x_start = 0.6
        y_pos = y_start - (i * row_height)
        for token in fila:
            est = estados[token]
            c_info = colores_map[est if est in colores_map else "Logra"]
            
            rect = patches.FancyBboxPatch(
                (x_start, y_pos), box_width, box_height,
                boxstyle="round,pad=0.02,rounding_size=0.1",
                facecolor=c_info["bg"],
                edgecolor=c_info["border"],
                linewidth=1.5
            )
            ax.add_patch(rect)
            
            ax.text(x_start + (box_width / 2.0), y_pos + (box_height / 2.0), token, color=c_info["text"], 
                    fontsize=9.5, fontweight='bold', ha='center', va='center')
            
            x_start += step_x

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight', dpi=300)
    buf.seek(0)
    plt.close(fig)
    return buf.getvalue()

# Botón central inferior para generar el reporte gráfico en PNG
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
