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

# Filas de fonemas en el orden correcto original
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

# Mapeo de colores y textos para los estados
colores_map = {
    "Logra": {"bg": "#d4edda", "border": "#c3e6cb", "text": "#155724", "ico": "🟢"},
    "No logra": {"bg": "#f8d7da", "border": "#f5c6cb", "text": "#721c24", "ico": "🔴"},
    "No valorado": {"bg": "#e2e3e5", "border": "#d6d8db", "text": "#383d41", "ico": "⚪"},
    "No esperado": {"bg": "#cce5ff", "border": "#b8daff", "text": "#004085", "ico": "🔵"}
}

# Inyectar estilos para que los botones interactivos ocupen todo el ancho y muestren el texto completo
st.markdown("""
    <style>
    .phoneme-btn {
        width: 100%;
        border-radius: 8px;
        font-weight: 700;
        font-size: 11px;
        padding: 6px 2px;
        min-height: 52px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        cursor: pointer;
        border: 1px solid transparent;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 8px;
        text-decoration: none !important;
    }
    .phoneme-btn span {
        font-size: 10px;
        margin-top: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# Renderizado interactivo usando formularios o botones de Streamlit optimizados por filas
for i, fila in enumerate(filas_fonemas):
    cols = st.columns(len(fila))
    for idx, token in enumerate(fila):
        estado = st.session_state.estados_matriz[token]
        c_info = colores_map[estado]
        
        with cols[idx]:
            # Creamos un botón nativo estilizado mediante clases inyectadas o estado de Streamlit
            btn_key = f"mat_{i}_{idx}_{token}"
            
            # Para garantizar que el botón se pinte por completo en la tablet, usamos un botón de Streamlit limpio
            if st.button(f"{token}\n{c_info['ico']}", key=btn_key, use_container_width=True):
                if estado == "Logra":
                    st.session_state.estados_matriz[token] = "No logra"
                elif estado == "No logra":
                    st.session_state.estados_matriz[token] = "No valorado"
                elif estado == "No valorado":
                    st.session_state.estados_matriz[token] = "No esperado"
                else:
                    st.session_state.estados_matriz[token] = "Logra"
                st.rerun()
            
            # CSS específico para colorear este botón exacto por completo
            st.markdown(f"""
                <style>
                div[data-testid="column"]:nth-of-type({idx+1}) button[key*="{token.replace('/', '')}"] {{
                    background-color: {c_info["bg"]} !important;
                    color: {c_info["text"]} !important;
                    border: 1px solid {c_info["border"]} !important;
                }}
                </style>
            """, unsafe_allow_html=True)

st.markdown("---")

# Función para generar la imagen PNG del reporte gráfico final
def generar_grafico_matriz(estados):
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.set_xlim(0, 18.5)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Leyenda superior del gráfico
    leyendas = [
        ("Logra", "#d4edda", "#155724", 0.6),
        ("No logra", "#f8d7da", "#721c24", 4.8),
        ("No valorado", "#e2e3e5", "#383d41", 9.0),
        ("No esperado para su edad", "#cce5ff", "#004085", 13.2)
    ]
    for lbl, bg_l, tx_l, x_pos in leyendas:
        ax.add_patch(patches.Circle((x_pos, 7.3), 0.15, facecolor=bg_l, edgecolor=tx_l, linewidth=1.5))
        ax.text(x_pos + 0.3, 7.3, lbl, fontsize=10, va='center', fontweight='bold', color='#333333')

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
