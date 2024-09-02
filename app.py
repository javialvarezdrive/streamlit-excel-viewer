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
    # Intentar leer el archivo según su tipo
    try:
        # Verificar la extensión del archivo y cargarlo adecuadamente
        if uploaded_file.name.endswith(('xlsx', 'xls')):
            df = pd.read_excel(uploaded_file, engine='openpyxl')
        elif uploaded_file.name.endswith('csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('txt'):
            # Asumir un delimitador común como la coma, permitir ajuste si es necesario
            delimiter = st.text_input('Delimitador para archivos de texto (e.g., ",", ";", "|"):', value=',')
            df = pd.read_csv(uploaded_file, delimiter=delimiter)
        else:
            st.error("Tipo de archivo no soportado.")
            st.stop()  # Detener la ejecución si el archivo no es soportado.

        # Restablecer el índice para eliminar la columna de índice
        df = df.reset_index(drop=True)

        # Definir filtros por defecto
        filters = {
            'Categoria': 'Todos',
            'Club': 'Todos',
            'Genero': 'Todos'
        }

        # Barra lateral para los filtros
        with st.sidebar.expander("Filtros", expanded=True):
            # Filtros dinámicos basados en los valores únicos de las columnas
            if 'Categoria' in df.columns:
                filters['Categoria'] = st.selectbox('Filtrar por Categoria', options=['Todos'] + df['Categoria'].unique().tolist())
            if 'Club' in df.columns:
                filters['Club'] = st.selectbox('Filtrar por Club', options=['Todos'] + df['Club'].unique().tolist())
            if 'Genero' in df.columns:
                filters['Genero'] = st.selectbox('Filtrar por Genero', options=['Todos'] + df['Genero'].unique().tolist())

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
            default=filtered_df.columns.tolist()  # Por defecto, mostrar todas las columnas
        )

        # Mostrar los datos filtrados con las columnas seleccionadas utilizando st.dataframe
        st.write("Datos:")
        st.dataframe(filtered_df[columnas_seleccionadas], use_container_width=True)

        # Botón para exportar los datos filtrados a un archivo CSV sin índices
        st.write("Exportar datos:")
        if st.button('Exportar a CSV'):
            filtered_df[columnas_seleccionadas].to_csv('datos_filtrados.csv', index=False)
            st.success('Archivo CSV exportado sin índices.')

    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
