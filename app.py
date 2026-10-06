import streamlit as st
import os

# Configuración de la página
st.set_page_config(
    page_title="Test de Articulación de Fonemas",
    page_icon="🗣️",
    layout="wide"
)

st.title("🗣️ Panel Visual Interactivo de Fonemas")
st.write("Visualiza tu lámina de referencia y haz clic directamente en los botones de los fonemas para cambiar su estado de evaluación.")

# Inicializar los estados de los fonemas en la memoria de la app
fonemas_lista = ["P", "B", "T", "D", "K", "G", "F", "S", "J", "CH", "Y", "M", "N", "Ñ", "L", "R", "RR"]

if "estados_fonemas" not in st.session_state:
    st.session_state.estados_fonemas = {f: "Correcto 🟢" for f in fonemas_lista}

# Datos generales
col_p1, col_p2 = st.columns(2)
with col_p1:
    nombre_paciente = st.text_input("Nombre del paciente o alumno:")
with col_p2:
    evaluador = st.text_input("Terapeuta / Evaluador:")

st.markdown("---")

# Distribución: Imagen a la izquierda, Panel visual interactivo a la derecha
col_imagen, col_panel = st.columns([1.2, 1])

with col_imagen:
    st.subheader("🖼️ Lámina de Referencia")
    nombre_archivo_imagen = "lamina.png"  # Asegúrate de subir tu imagen con este nombre a GitHub
    
    if os.path.exists(nombre_archivo_imagen):
        st.image(nombre_archivo_imagen, caption="Lámina oficial", use_container_width=True)
    else:
        st.warning(
            f"⚠️ No se encontró la imagen '{nombre_archivo_imagen}' en el repositorio. "
            "Sube tu archivo de imagen a la raíz de GitHub para visualizarlo aquí."
        )

with col_panel:
    st.subheader("🎛️ Panel Visual de Control")
    st.write("Haz clic sobre cualquier fonema para cambiar su estado cíclicamente:")
    
    # Leyenda rápida
    st.caption("🟢 Correcto | 🟡 Sustitución | 🟠 Omisión | 🔴 Distorsión")
    
    # Crear una cuadrícula de botones interactivos
    cols = st.columns(3)
    for i, fonema in enumerate(fonemas_lista):
        col_idx = i % 3
        estado_actual = st.session_state.estados_fonemas[fonema]
        
        # Texto del botón con su estado actual
        boton_label = f"/{fonema}/\n{estado_actual}"
        
        with cols[col_idx]:
            if st.button(boton_label, key=f"btn_{fonema}", use_container_width=True):
                # Ciclar al hacer clic: Correcto -> Sustitución -> Omisión -> Distorsión -> Correcto
                if "Correcto" in estado_actual:
                    st.session_state.estados_fonemas[fonema] = "Sustitución 🟡"
                elif "Sustitución" in estado_actual:
                    st.session_state.estados_fonemas[fonema] = "Omisión 🟠"
                elif "Omisión" in estado_actual:
                    st.session_state.estados_fonemas[fonema] = "Distorsión 🔴"
                else:
                    st.session_state.estados_fonemas[fonema] = "Correcto 🟢"
                st.rerun()  # Recarga la pantalla al instante para reflejar el cambio

st.markdown("---")

# Sección de resultados y guardado
st.subheader("📋 Resumen de la Evaluación")
observaciones = st.text_area("Notas u observaciones clínicas:")

if st.button("💾 Guardar y Finalizar Evaluación", type="primary", use_container_width=True):
    if not nombre_paciente.strip():
        st.warning("⚠️ Ingresa el nombre del paciente antes de guardar.")
    else:
        st.success(f"¡Evaluación registrada para **{nombre_paciente}**!")
        
        # Filtrar alteraciones
        alteraciones = {f: est for f, est in st.session_state.estados_fonemas.items() if "Correcto" not in est}
        
        if alteraciones:
            st.warning(f"Se registraron **{len(alteraciones)}** alteraciones:")
            for f, e in alteraciones.items():
                st.write(f"- **/{f}/**: {e}")
        else:
            st.balloons()
            st.success("🎉 ¡Excelente desempeño! Sin alteraciones fonológicas detectadas.")
