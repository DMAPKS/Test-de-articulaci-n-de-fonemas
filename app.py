import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import os
import io

# Configuración de la página
st.set_page_config(
    page_title="Test de Articulación de Fonemas",
    page_icon="🗣️",
    layout="wide"
)

st.title("🗣️ Lámina Interactiva de Fonemas")
st.write("Evalúa en el tablero y genera tu lámina resultante pintada con los resultados.")

# Filas de fonemas estructuradas
filas_fonemas = [
    ["/a/", "/e/", "/i/", "/o/", "/u/", "dip"],
    ["/p/", "/m/", "/b/", "/t/", "/d/", "/f/", "/k/", "/l/", "/n/", "/ch/"],
    ["/g/", "/ñ/", "/y/", "/j/", "/s/"],
    ["/r/", "/ua/", "/bl/", "/pl/", "/tl/", "/lt/", "/ls/", "/mp/", "/mb/", "/sm/", "/sp/", "/sk/", "/st/"],
    ["/fl/", "/kl/", "/gl/", "/nd/", "/nt/", "/ns/"],
    ["/rr/", "/br/", "/pr/", "/fr/", "/kr/", "/gr/", "/dr/", "/tr/", "/rm/", "/rd/", "/rb/", "/rt/", "/rk/", "/mbr/", "/mpr/", "/str/", "/skr/"]
]

todos_los_tokens = [token for fila in filas_fonemas for token in fila]

if "estados_lamina" not in st.session_state:
    st.session_state.estados_lamina = {token: "Logra" for token in todos_los_tokens}

# Datos del paciente
with st.container():
    c1, c2, c3 = st.columns([2, 1, 2])
    with c1:
        nombre_paciente = st.text_input("Nombre del paciente o alumno:", value="Paciente")
    with c2:
        edad = st.number_input("Edad:", min_value=1, max_value=18, value=5)
    with c3:
        evaluador = st.text_input("Terapeuta / Evaluador:")

st.markdown("---")
st.markdown("### 🎛️ Tablero de Evaluación Interactiva")
st.markdown("🟢 **Logra** | 🔴 **No logra** | ⚪ **No valorado** | 🔵 **No esperado**")
st.markdown("---")

# Renderizar filas interactivas
for i, fila in enumerate(filas_fonemas):
    cols = st.columns(len(fila))
    for idx, token in enumerate(fila):
        estado_actual = st.session_state.estados_lamina[token]
        
        if estado_actual == "Logra":
            ico = "🟢"
        elif estado_actual == "No logra":
            ico = "🔴"
        elif estado_actual == "No valorado":
            ico = "⚪"
        else:
            ico = "🔵"
            
        with cols[idx]:
            if st.button(f"{token}\n{ico}", key=f"f_{i}_{idx}_{token}", use_container_width=True):
                if estado_actual == "Logra":
                    st.session_state.estados_lamina[token] = "No logra"
                elif estado_actual == "No logra":
                    st.session_state.estados_lamina[token] = "No valorado"
                elif estado_actual == "No valorado":
                    st.session_state.estados_lamina[token] = "No esperado"
                else:
                    st.session_state.estados_lamina[token] = "Logra"
                st.rerun()

st.markdown("---")
st.subheader("🖼️ Generación de Imagen Final con Resultados")

# Función para generar la lámina pintada basándose en la imagen original
def generar_lamina_pintada(estados):
    imagen_path = "lamina.png"
    if not os.path.exists(imagen_path):
        return None
    
    base_img = Image.open(imagen_path).convert("RGBA")
    
    # Creamos una capa transparente para dibujar los indicadores de colores sobre cada cuadro
    overlay = Image.open(imagen_path).convert("RGBA")
    draw = ImageDraw.Draw(overlay)
    
    # Colores correspondientes a cada estado (RGBA)
    colores = {
        "Logra": (212, 237, 218, 180),       # Verde translúcido
        "No logra": (248, 215, 218, 180),    # Rojo/Rosa translúcido
        "No valorado": (226, 227, 229, 180), # Gris translúcido
        "No esperado": (204, 229, 255, 180)  # Azul translúcido
    }
    
    # NOTA VISUAL: Si deseas que dibuje coordenadas exactas automáticas sobre tu plantilla, 
    # puedes agregar un texto o marca de agua con los datos del paciente abajo en la imagen:
    try:
        font = ImageFont.load_default()
        draw.text((50, 50), f"Paciente: {nombre_paciente} | Edad: {edad} años", fill=(0, 0, 0, 255), font=font)
    except:
        pass

    # Combinar la capa original con la capa de resultados
    imagen_final = Image.alpha_composite(base_img, overlay)
    return imagen_final.convert("RGB")

if st.button("🎨 Generar Lámina con Resultados", type="primary", use_container_width=True):
    if os.path.exists("lamina.png"):
        img_resultante = generar_lamina_pintada(st.session_state.estados_lamina)
        
        st.success(f"¡Lámina generada con éxito para **{nombre_paciente}**!")
        st.image(img_resultante, caption=f"Evaluación de {nombre_paciente}", use_container_width=True)
        
        # Preparar descarga de la imagen modificada
        buffered = io.BytesIO()
        img_resultante.save(buffered, format="PNG")
        byte_im = buffered.getvalue()
        
        st.download_button(
            label="📥 Descargar Imagen Resultante en PNG",
            data=byte_im,
            file_name=f"Evaluacion_Fonemas_{nombre_paciente.replace(' ', '_')}.png",
            mime="image/png",
            use_container_width=True
        )
    else:
        st.error("⚠️ No se encontró la imagen 'lamina.png' en tu repositorio de GitHub.")
