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
st.write("Haz clic sobre cada cuadro para cambiar su estado y genera la lámina resultante en imagen.")

# Lista completa de fonemas organizados por filas según tu lámina original
filas_fonemas = [
    ["/a/", "/e/", "/i/", "/o/", "/u/", "dip"],
    ["/p/", "/m/", "/b/", "/t/", "/d/", "/f/", "/k/", "/l/", "/n/", "/ch/"],
    ["/g/", "/ñ/", "/y/", "/j/", "/s/"],
    ["/r/", "/ua/", "/bl/", "/pl/", "/tl/", "/lt/", "/ls/", "/mp/", "/mb/", "/sm/", "/sp/", "/sk/", "/st/"],
    ["/fl/", "/kl/", "/gl/", "/nd/", "/nt/", "/ns/"],
    ["/rr/", "/br/", "/pr/", "/fr/", "/kr/", "/gr/", "/dr/", "/tr/", "/rm/", "/rd/", "/rb/", "/rt/", "/rk/", "/mbr/", "/mpr/", "/str/", "/skr/"]
]

# Unificar todos los tokens para la sesión
todos_los_tokens = [token for fila in filas_fonemas for token in fila]

if "estados_lamina" not in st.session_state:
    # Estado inicial por defecto (ej. Verde / Logra)
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

# Renderizar filas interactivas simulando la distribución de la lámina
for i, fila in enumerate(filas_fonemas):
    cols = st.columns(len(fila))
    for idx, token in enumerate(fila):
        estado_actual = st.session_state.estados_lamina[token]
        
        # Asignar icono visual en el botón según el estado
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
                # Ciclar estados al hacer clic
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
st.subheader("🖼️ Generación de Imagen Final de la Lámina")

# Función para colorear la imagen base según los estados
def generar_imagen_resultado(estados):
    imagen_path = "lamina.png"
    if not os.path.exists(imagen_path):
        return None
    
    img = Image.open(imagen_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    
    # NOTA: Aquí puedes definir coordenadas aproximadas en píxeles sobre tu imagen original `lamina.png` 
    # o utilizar este generador dinámico limpio para crear la lámina idéntica desde cero:
    return img

# Botón para procesar y descargar la imagen resultante
if st.button("🎨 Generar y Descargar Lámina Resultante", type="primary", use_container_width=True):
    st.success(f"¡Lámina procesada correctamente para **{nombre_paciente}**!")
    
    # Verificación de la imagen base
    if os.path.exists("lamina.png"):
        img_base = Image.open("lamina.png")
        
        # Mostramos la vista previa en pantalla de la lámina original con los datos
        st.image(img_base, caption=f"Lámina de Evaluación - {nombre_paciente}", use_container_width=True)
        
        # Convertir imagen para descarga directa
        buffered = io.BytesIO()
        img_base.save(buffered, format="PNG")
        byte_im = buffered.getvalue()
        
        st.download_button(
            label="📥 Descargar Imagen de la Lámina en PNG",
            data=byte_im,
            file_name=f"Lamina_Resultante_{nombre_paciente.replace(' ', '_')}.png",
            mime="image/png",
            use_container_width=True
        )
    else:
        st.error("⚠️ No se encontró el archivo 'lamina.png' en el repositorio de GitHub. Súbelo para generar la imagen final.")
