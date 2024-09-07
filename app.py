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
st.title('Visualización de Datos de Excel')
st.write('Sube tu archivo Excel para visualizar y filtrar los datos.')

# Subir archivo Excel
uploaded_file = st.file_uploader("Elige un archivo Excel", type=['xlsx', 'xls'])

# Estado de sesión para filtros
if 'filters' not in st.session_state:
    st.session_state.filters = {
        'Categoria': 'Todos',
        'Club': 'Todos',
        'Genero': 'Todos'
    }

def reset_filters():
    st.session_state.filters = {key: 'Todos' for key in st.session_state.filters}

if uploaded_file is not None:
    # Leer el archivo Excel
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Barra lateral para los filtros
        with st.sidebar.expander("Filtros", expanded=True):
            # Filtros dinámicos basados en los valores únicos de las columnas
            for col in ['Categoria', 'Club', 'Genero']:
                if col in df.columns:
                    options = ['Todos'] + sorted(df[col].dropna().unique().tolist())
                    st.session_state.filters[col] = st.selectbox(
                        f'Filtrar por {col}', 
                        options=options, 
                        index=options.index(st.session_state.filters[col])
                    )

            # Botón para limpiar filtros
            st.button('Limpiar Filtros', on_click=reset_filters)

        # Aplicar los filtros seleccionados
        filtered_df = df.copy()
        for col, selected in st.session_state.filters.items():
            if selected != 'Todos':
                filtered_df = filtered_df[filtered_df[col] == selected]

        # Selección de columnas a mostrar
        st.write("Selecciona las columnas que deseas ver:")
        columnas_seleccionadas = st.multiselect(
            "Selecciona las columnas",
            options=filtered_df.columns.tolist(),
            default=filtered_df.columns.tolist()  # Por defecto, mostrar todas las columnas
        )

        # Mostrar los datos filtrados con las columnas seleccionadas sin el índice
        st.write("Datos:")
        st.dataframe(filtered_df[columnas_seleccionadas].reset_index(drop=True), use_container_width=True)

    except ValueError as ve:
        st.error(f"Error en la lectura del archivo: {ve}. Verifique el formato y contenido del archivo.")
    except Exception as e:
        st.error(f"Error inesperado: {e}.")
