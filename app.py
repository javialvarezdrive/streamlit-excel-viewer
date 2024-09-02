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

        # Convertir el DataFrame filtrado a HTML sin índice
        html_table = filtered_df[columnas_seleccionadas].to_html(index=False, justify='left', border=0, classes='responsive-table')

        # Estilos CSS para hacer la tabla responsive, con filas de la misma altura, y espaciado adecuado
        responsive_table_style = """
        <style>
        .responsive-table {
            width: 100%;
            overflow-x: auto;
            display: block;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .responsive-table th, .responsive-table td {
            padding: 10px; /* Aumentar el padding para mejorar la legibilidad */
            text-align: left;
            border: 1px solid #ddd;
            height: 40px;  /* Establecer una altura fija y uniforme para todas las filas */
            min-width: 100px;  /* Ancho mínimo para las celdas */
        }
        .responsive-table th {
            background-color: #f4f4f4; /* Color de fondo para la cabecera */
        }
        </style>
        """

        # Mostrar los datos filtrados con las columnas seleccionadas como HTML
        st.write("Datos:")
        st.markdown(responsive_table_style + f'{html_table}', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
