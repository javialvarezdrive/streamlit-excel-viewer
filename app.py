import streamlit as st
import pandas as pd

# Configuración de la página para ocupar todo el ancho
st.set_page_config(layout="wide")

# Configuración básica de la aplicación
st.title('Visualización de Datos de Excel')
st.write('Sube tu archivo Excel para visualizar y filtrar los datos.')

# Subir archivo Excel
uploaded_file = st.file_uploader("Elige un archivo Excel", type=['xlsx', 'xls'])

if uploaded_file is not None:
    # Leer el archivo Excel
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Asegurarse de que la columna de tiempo esté en formato timedelta
        if 'Tiempo' in df.columns:
            # Convertir la columna de tiempo a timedelta
            df['Tiempo'] = pd.to_timedelta(df['Tiempo'].astype(str))

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

            # Filtro de rango de tiempo
            if 'Tiempo' in df.columns:
                min_time = df['Tiempo'].min()
                max_time = df['Tiempo'].max()
                time_range = st.slider(
                    'Selecciona el rango de tiempo',
                    min_value=min_time,
                    max_value=max_time,
                    value=(min_time, max_time),
                    format="hh:mm:ss"
                )

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
        if 'Tiempo' in df.columns:
            filtered_df = filtered_df[(filtered_df['Tiempo'] >= time_range[0]) & (filtered_df['Tiempo'] <= time_range[1])]

        # Selección de columnas a mostrar
        st.write("Selecciona las columnas que deseas ver:")
        columnas_seleccionadas = st.multiselect(
            "Selecciona las columnas",
            options=filtered_df.columns.tolist(),
            default=filtered_df.columns.tolist()  # Por defecto, mostrar todas las columnas
        )

        # Mostrar los datos filtrados con las columnas seleccionadas
        st.write("Datos:")
        st.dataframe(filtered_df[columnas_seleccionadas], use_container_width=True)

    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
