import streamlit as st
import pandas as pd

# Configuración básica de la aplicación
st.title('Visualización de Datos de Excel')
st.write('Sube tu archivo Excel para visualizar y filtrar los datos.')

# Subir archivo Excel
uploaded_file = st.file_uploader("Elige un archivo Excel", type=['xlsx', 'xls'])

if uploaded_file is not None:
    # Leer el archivo Excel
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Mostrar los datos cargados
        st.write("Datos cargados:")
        st.dataframe(df)

        # Barra lateral para los filtros
        with st.sidebar.expander("Filtros", expanded=True):
            # Filtros dinámicos basados en los valores únicos de las columnas
            if 'Categoria' in df.columns:
                categoria = st.selectbox('Filtrar por Categoria', options=['Todos'] + df['Categoria'].unique().tolist())
            else:
                categoria = 'Todos'

            if 'Club' in df.columns:
                club = st.selectbox('Filtrar por Club', options=['Todos'] + df['Club'].unique().tolist())
            else:
                club = 'Todos'

            if 'Genero' in df.columns:
                genero = st.selectbox('Filtrar por Genero', options=['Todos'] + df['Genero'].unique().tolist())
            else:
                genero = 'Todos'

        # Aplicar los filtros seleccionados
        filtered_df = df.copy()
        if categoria != 'Todos':
            filtered_df = filtered_df[filtered_df['Categoria'] == categoria]
        if club != 'Todos':
            filtered_df = filtered_df[filtered_df['Club'] == club]
        if genero != 'Todos':
            filtered_df = filtered_df[filtered_df['Genero'] == genero]

        # Mostrar los datos filtrados
        st.write("Datos filtrados:")
        st.dataframe(filtered_df)

    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
