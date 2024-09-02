import streamlit as st
import pandas as pd

# Configuración de la página para ocupar todo el ancho
st.set_page_config(layout="wide")

# Ocultar el menú de configuración (tres puntos)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Configuración básica de la aplicación
st.title('Visualización de Datos')
st.write('Sube tu archivo para visualizar y filtrar los datos.')

# Subir archivo (Excel, CSV, o Texto delimitado)
uploaded_file = st.file_uploader("Elige un archivo", type=['xlsx', 'xls', 'csv', 'txt'])

if uploaded_file is not None:
    try:
        # Verificar la extensión del archivo y cargarlo adecuadamente
        if uploaded_file.name.endswith(('xlsx', 'xls')):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        elif uploaded_file.name.endswith('csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('txt'):
            delimiter = st.text_input('Delimitador para archivos de texto (e.g., ",", ";", "|"):', value=',')
            df = pd.read_csv(uploaded_file, delimiter=delimiter)
        else:
            st.error("Tipo de archivo no soportado.")

        # Convertir columnas a numéricas si es necesario
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convertir a numérico y manejar errores

        # Definir filtros por defecto
        filters = {
            'Categoria': 'Todos',
            'Club': 'Todos',
            'Genero': 'Todos'
        }

        # Barra lateral para los filtros
        with st.sidebar.expander("Filtros", expanded=True):
            if 'Categoria' in df.columns:
                filters['Categoria'] = st.selectbox('Filtrar por Categoria', options=['Todos'] + df['Categoria'].dropna().unique().tolist())
            if 'Club' in df.columns:
                filters['Club'] = st.selectbox('Filtrar por Club', options=['Todos'] + df['Club'].dropna().unique().tolist())
            if 'Genero' in df.columns:
                filters['Genero'] = st.selectbox('Filtrar por Genero', options=['Todos'] + df['Genero'].dropna().unique().tolist())

            # Botón para limpiar filtros
            if st.button('Limpiar Filtros'):
                filters = {key: 'Todos' for key in filters}

        # Aplicar los filtros seleccionados
        filtered_df = df.copy()
        if filters['Categoria'] != 'Todos':
            filtered_df = filtered_df[filtered_df['Categoria'] == filters['Categoria']]
        if filters['Club'] != 'Todos':
            filtered_df = filtered_df[filtered_df['Club'] == filters['Club']]
        if filters['Genero'] != 'Todos':
            filtered_df = filtered_df[filtered_df['Genero'] == filters['Genero']]

        # Selección de columnas a mostrar
        st.write("Selecciona las columnas que deseas ver:")
        columnas_seleccionadas = st.multiselect(
            "Selecciona las columnas",
            options=filtered_df.columns.tolist(),
            default=filtered_df.columns.tolist()
        )

        # Mostrar los datos filtrados con las columnas seleccionadas
        st.write("Datos:")
        st.dataframe(filtered_df[columnas_seleccionadas], use_container_width=True)

    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
