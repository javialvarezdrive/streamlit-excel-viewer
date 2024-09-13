import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Configuración de la página para ocupar todo el ancho
st.set_page_config(layout="wide")

# Ocultar el menú de configuración (tres puntos)
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Configuración básica de la aplicación
st.title('Visualización de Datos')
st.write('Sube tu archivo Excel o CSV para visualizar y filtrar los datos.')

# Subir archivo Excel o CSV
uploaded_file = st.file_uploader("Elige un archivo Excel o CSV", type=['xlsx', 'xls', 'csv'])

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
    # Leer el archivo Excel o CSV
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')

        # Barra lateral para los filtros
        with st.sidebar.expander("Filtros", expanded=True):
            # Filtros dinámicos basados en los valores únicos de las columnas
            for col in ['Categoria', 'Club', 'Genero']:
                if col in df.columns:
                    options = ['Todos'] + sorted(df[col].dropna().unique().tolist())
                    selected_option = st.session_state.filters.get(col, 'Todos')
                    if selected_option not in options:
                        selected_option = 'Todos'
                    st.session_state.filters[col] = st.selectbox(
                        f'Filtrar por {col}', 
                        options=options, 
                        index=options.index(selected_option)
                    )
                else:
                    st.warning(f"La columna '{col}' no s
