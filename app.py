import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Test de Articulación de Fonemas",
    page_icon="🗣️",
    layout="centered"
)

# Título principal de la aplicación
st.title("🗣️ Test de Articulación de Fonemas")
st.write("Evaluación fonológica interactiva para el registro y análisis del habla.")

# Sección de datos del paciente
st.header("1. Datos Generales")
nombre_paciente = st.text_input("Nombre del paciente o alumno:")
edad = st.number_input("Edad (años):", min_value=1, max_value=18, value=5)
evaluador = st.text_input("Nombre del evaluador / terapeuta:")

st.markdown("---")

# Sección de evaluación de fonemas
st.header("2. Registro de Articulación")
st.write("Selecciona el estado de articulación para cada fonema evaluado:")

# Lista de fonemas organizados por grupos comunes
fonemas = {
    "Consonantes Oclusivas": ["P", "B", "T", "D", "K", "G"],
    "Consonantes Fricativas": ["F", "S", "J", "CH", "Y"],
    "Consonantes Nasales y Líquidas": ["M", "N", "Ñ", "L", "R", "RR"]
}

resultados = {}

for categoria, lista_fonemas in fonemas.items():
    st.subheader(categoria)
    cols = st.columns(3)
    for i, fonema in enumerate(lista_fonemas):
        col_idx = i % 3
        with cols[col_idx]:
            estado = st.selectbox(
                f"Fonema /{fonema}/",
                ["Correcto", "Sustitución", "Omisión", "Distorsión"],
                key=f"fonema_{fonema}"
            )
            resultados[fonema] = estado

st.markdown("---")

# Observaciones y comentarios
st.header("3. Observaciones Clínicas")
observaciones = st.text_area("Notas adicionales, conducta o patrón fonológico observado:")

# Botón para procesar y guardar resultados
if st.button("💾 Guardar y Generar Reporte", type="primary"):
    if not nombre_paciente.strip():
        st.warning("Por favor, ingresa el nombre del paciente antes de guardar.")
    else:
        st.success(f"¡Evaluación guardada con éxito para **{nombre_paciente}**!")
        
        # Resumen de resultados
        st.subheader("📋 Resumen de la Evaluación")
        st.write(f"**Edad:** {edad} años")
        st.write(f"**Evaluador:** {evaluador if evaluador else 'No especificado'}")
        
        # Mostrar errores o fonemas alterados
        alterados = {f: est for f, est in resultados.items() if est != "Correcto"}
        
        if alterados:
            st.write("**Fonemas que requieren atención:**")
            for fonema, estado in alterados.items():
                st.write(f"- **/{fonema}/**: {estado}")
        else:
            st.balloons()
            st.success("¡Excelente! Todos los fonemas evaluados se encuentran correctos.")
