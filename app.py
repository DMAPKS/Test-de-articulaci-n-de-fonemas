import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Test de Articulación de Fonemas",
    page_icon="🗣️️",
    layout="wide"
)

# Título principal
st.title("🗣️ Test de Articulación de Fonemas - Panel Interactivo")
st.write("Selecciona o evalúa cada fonema haciendo clic en las opciones correspondientes.")

# Datos generales en una barra superior dividida
col_1, col_2, col_3 = st.columns(3)
with col_1:
    nombre_paciente = st.text_input("Nombre del paciente o alumno:")
with col_2:
    edad = st.number_input("Edad (años):", min_value=1, max_value=18, value=5)
with col_3:
    evaluador = st.text_input("Nombre del evaluador:")

st.markdown("---")

# Estructura principal en dos columnas (Simulando panel visual y controles)
col_izq, col_der = st.columns([1, 1.2])

with col_izq:
    st.subheader("🖼️ Referencia Visual")
    # Aquí puedes mostrar la imagen de los fonemas si la subiste al repositorio
    # Ejemplo: st.image("tu_imagen_fonemas.png", caption="Lámina de Articulación")
    
    # Como alternativa visual integrada si no hay imagen física cargada aún:
    st.info(
        "💡 **Nota:** Si tienes una lámina o imagen oficial del test, "
        "puedes colocarla en tu repositorio de GitHub e incluirla aquí usando "
        "`st.image('nombre_de_tu_imagen.png')` para verla de manera simultánea."
    )
    
    st.markdown("### 📊 Leyenda de Estados")
    st.markdown("🟢 **Correcto:** Articulación adecuada.")
    st.markdown("🟡 **Sustitución:** Cambia un fonema por otro.")
    st.markdown("🟠 **Omisión:** Omite el fonema.")
    st.markdown("🔴 **Distorsión:** Sonido alterado o deformado.")

with col_der:
    st.subheader("📝 Registro de Fonemas por Grupos")
    
    # Definición de grupos de fonemas
    grupos_fonemas = {
        "Oclusivos": ["P", "B", "T", "D", "K", "G"],
        "Fricativos": ["F", "S", "J", "CH", "Y"],
        "Nasales y Líquidos": ["M", "N", "Ñ", "L", "R", "RR"]
    }
    
    resultados = {}
    
    for grupo, lista in grupos_fonemas.items():
        with st.expander(f"📌 Grupo: {grupo}", expanded=True):
            for fonema in lista:
                # Creamos filas interactivas para cada fonema
                c_fonema, c_opcion = st.columns([1, 2])
                with c_fonema:
                    st.markdown(f"### `/{fonema}/`")
                with c_opcion:
                    estado = st.selectbox(
                        f"Estado /{fonema}/",
                        ["Correcto", "Sustitución", "Omisión", "Distorsión"],
                        key=f"fonema_{fonema}",
                        label_visibility="collapsed"
                    )
                    resultados[fonema] = estado

st.markdown("---")

# Observaciones y Botón de Guardado
st.subheader("📋 Observaciones Clínicas y Cierre")
observaciones = st.text_area("Escribe aquí notas adicionales sobre la evaluación:")

if st.button("💾 Guardar y Evaluar Resultados", type="primary", use_container_width=True):
    if not nombre_paciente.strip():
        st.warning("⚠️ Por favor, ingresa el nombre del paciente antes de continuar.")
    else:
        st.success(f"¡Evaluación registrada correctamente para **{nombre_paciente}**!")
        
        # Filtrar alteraciones
        alterados = {f: est for f, est in resultados.items() if est != "Correcto"}
        
        if alterados:
            st.warning(f"Se encontraron **{len(alterados)} fonema(s)** con alteraciones:")
            for f, e in alterados.items():
                st.write(f"- **/{f}/**: {e}")
        else:
            st.balloons()
            st.success("🎉 ¡Excelente desempeño! No se registraron alteraciones fonológicas.")
