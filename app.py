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

# Estilos CSS personalizados para los botones de la matriz
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        border-radius: 6px;
        font-weight: 600;
        font-size: 13px;
        padding: 5px 2px;
    }
    </style>
""", unsafe_allow_html=True)

# Renderizado del tablero interactivo por filas
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

# Función para generar la imagen PNG exacta utilizando Matplotlib
def generar_grafico_matriz(estados):
    # Ampliamos el límite del eje X de 16 a 17.5 para que quepa toda la fila larga sin cortes
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.set_xlim(0, 17.5)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Colores exactos en formato HEX
    colores_map = {
        "Logra": {"bg": "#d4edda", "edge": "#c3e6cb", "text": "#155724"},
        "No logra": {"bg": "#f8d7da", "edge": "#f5c6cb", "text": "#721c24"},
        "No valorado": {"bg": "#e2e3e5", "edge": "#d6d8db", "text": "#383d41"},
        "No esperado": {"bg": "#cce5ff", "edge": "#b8daff", "text": "#004085"}
    }
    
    # Dibujar Leyenda superior en el gráfico ajustada simétricamente
    leyendas = [
        ("Logra", "#d4edda", "#155724", 0.5),
        ("No logra", "#f8d7da", "#721c24", 4.5),
        ("No valorado", "#e2e3e5", "#383d41", 8.5),
        ("No esperado para su edad", "#cce5ff", "#004085", 12.5)
    ]
    for lbl, bg_l, tx_l, x_pos in leyendas:
        ax.add_patch(patches.Circle((x_pos, 7.3), 0.15, facecolor=bg_l, edgecolor=tx_l, linewidth=1.5))
        ax.text(x_pos + 0.3, 7.3, lbl, fontsize=10, va='center', fontweight='bold', color='#333333')

    # Dibujar filas de fonemas con sus respectivos colores según estado
    y_start = 6.0
    row_height = 0.9
    
    for i, fila in enumerate(filas_fonemas):
        x_start = 0.5
        y_pos = y_start - (i * row_height)
        for token in fila:
            est = estados[token]
            c_info = colores_map[est]
            
            # Dibujar cajita redondeada del fonema
            rect = patches.FancyBboxPatch(
                (x_start, y_pos), 0.8, 0.6,
                boxstyle="round,pad=0.1",
                facecolor=c_info["bg"],
                edgecolor=c_info["edge"],
                linewidth=1.5
            )
            ax.add_patch(rect)
            
            # Texto del fonema centrado en la caja
            ax.text(x_start + 0.4, y_pos + 0.3, token, color=c_info["text"], 
                    fontsize=10, fontweight='bold', ha='center', va='center')
            
            x_start += 0.95

    # Guardar en buffer de memoria
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
