import streamlit as st
import pandas as pd
import plotly.express as px

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
st.title('Visualización de Datos de Excel')
st.write('Sube tu archivo Excel para visualizar y filtrar los datos.')

# Subir archivo Excel
uploaded_file = st.file_uploader("Elige un archivo Excel", type=['xlsx', 'xls'])

if uploaded_file is not None:
    # Leer el archivo Excel
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Convertir la columna de tiempo a timedelta si existe
        if 'Tiempo' in df.columns:
            df['Tiempo'] = pd.to_timedelta(df['Tiempo'].astype(str), errors='coerce')

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

        # Mostrar los datos filtrados con las columnas seleccionadas
        st.write("Datos:")
        st.dataframe(filtered_df[columnas_seleccionadas], use_container_width=True)

        # Mostrar el gráfico de tiempos medios por categoría
        if 'Tiempo' in filtered_df.columns and 'Categoria' in filtered_df.columns:
            st.write("Gráfico de Tiempos Medios por Categoría")

            # Calcular tiempos medios por categoría
            mean_times = filtered_df.groupby('Categoria')['Tiempo'].mean().reset_index()

            # Convertir el tiempo medio a segundos para el gráfico
            mean_times['Tiempo'] = mean_times['Tiempo'].dt.total_seconds()

            # Crear gráfico de barras
            fig = px.bar(mean_times, x='Categoria', y='Tiempo', labels={'Tiempo': 'Tiempo Medio (segundos)'}, title='Tiempos Medios por Categoría')
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
