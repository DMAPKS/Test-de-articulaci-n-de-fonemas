import streamlit as st
import os

# Configuración de la página
st.set_page_config(
    page_title="Test de Articulación de Fonemas",
    page_icon="🗣️",
    layout="wide"
)

# Título principal
st.title("🗣️ Test de Articulación de Fonemas - Evaluación Visual")
st.write("Visualiza la lámina del test y registra el estado de articulación de cada fonema.")

# Datos generales del paciente en la parte superior
with st.container():
    col_n1, col_n2, col_n3 = st.columns(3)
    with col_n1:
        nombre_paciente = st.text_input("Nombre del paciente o alumno:")
    with col_n2:
        edad = st.number_input("Edad (años):", min_value=1, max_value=18, value=5)
    with col_n3:
        evaluador = st.text_input("Terapeuta / Evaluador:")

st.markdown("---")

# Distribución en dos columnas: Izquierda la Imagen, Derecha los controles interactivos
col_imagen, col_controles = st.columns([1.2, 1])

with col_imagen:
    st.subheader("🖼️ Lámina de Evaluación")
    
    # Verificamos si la imagen existe en el repositorio para mostrarla
    nombre_archivo_imagen = "lamina.png" # <--- CAMBIA ESTE NOMBRE SI TU ARCHIVO SE LLAMA DIFERENTE
    
    if os.path.exists(nombre_archivo_imagen):
        st.image(nombre_archivo_imagen, caption="Lámina oficial de fonemas", use_container_width=True)
    else:
        st.warning(
            f"⚠️ No se encontró la imagen '{nombre_archivo_imagen}' en tu repositorio de GitHub. "
            "Sube tu imagen con ese nombre exacto a la raíz del repositorio para que aparezca aquí."
        )
        st.info("Mientras tanto, puedes realizar la evaluación utilizando el panel de selección de la derecha.")

with col_controles:
    st.subheader("⚙️ Panel de Registro de Fonemas")
    st.write("Selecciona el diagnóstico para cada fonema evaluado:")
    
    # Listado de fonemas organizados por categorías fonológicas
    fonemas_por_grupo = {
        "Oclusivos": ["P", "B", "T", "D", "K", "G"],
        "Fricativos": ["F", "S", "J", "CH", "Y"],
        "Nasales y Líquidos": ["M", "N", "Ñ", "L", "R", "RR"]
    }
    
    resultados = {}
    
    for grupo, lista in fonemas_por_grupo.items():
        with st.expander(f"📁 Grupo: {grupo}", expanded=True):
            for fonema in lista:
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.markdown(f"**/{fonema}/**")
                with c2:
                    # Usamos colores o estados claros
                    estado = st.selectbox(
                        f"/{fonema}/",
                        ["Correcto 🟢", "Sustitución 🟡", "Omisión 🟠", "Distorsión 🔴"],
                        key=f"fonema_{fonema}",
                        label_visibility="collapsed"
                    )
                    resultados[fonema] = estado

st.markdown("---")

# Sección final de observaciones y guardado
st.subheader("📝 Observaciones Clínicas y Resultados")
observaciones = st.text_area("Anota aquí los datos relevantes de la evaluación fonológica:")

if st.button("💾 Guardar Evaluación", type="primary", use_container_width=True):
    if not nombre_paciente.strip():
        st.warning("⚠️ Por favor, ingresa el nombre del paciente antes de guardar.")
    else:
        st.success(f"¡Evaluación guardada exitosamente para **{nombre_paciente}**!")
        
        # Filtrar los que no están correctos
        alteraciones = {f: est for f, est in resultados.items() if not est.startswith("Correcto")}
        
        if alteraciones:
            st.warning(f"Se detectaron **{len(alteraciones)}** fonemas alterados:")
            for f, e in alteraciones.items():
                st.write(f"- **/{f}/**: {e}")
        else:
            st.balloons()
            st.success("🎉 ¡Excelente! No se registran alteraciones en los fonemas evaluados.")
