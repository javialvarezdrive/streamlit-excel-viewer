import streamlit as st
import pandas as pd

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
                    st.warning(f"La columna '{col}' no se encontró en el archivo.")

            # Botón para limpiar filtros
            st.button('Limpiar Filtros', on_click=reset_filters)

        # Aplicar los filtros seleccionados
        filtered_df = df.copy()
        for col, selected in st.session_state.filters.items():
            if selected != 'Todos' and col in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[col] == selected]

        # Resetea el índice y elimina la columna de índice
        filtered_df.reset_index(drop=True, inplace=True)

        # Selección de columnas a mostrar
        st.write("Selecciona las columnas que deseas ver:")
        columnas_seleccionadas = st.multiselect(
            "Selecciona las columnas",
            options=filtered_df.columns.tolist(),
            default=filtered_df.columns.tolist()  # Por defecto, mostrar todas las columnas
        )

        # Mostrar el número de registros
        st.write(f"Datos (Total de registros: {len(filtered_df)}):")

        # Eliminar la columna de índice del DataFrame antes de mostrarlo
        df_to_display = filtered_df[columnas_seleccionadas].copy()
        df_to_display.index = [''] * len(df_to_display)

        # Mostrar la tabla sin la columna de índice
        st.table(df_to_display)

    except ValueError as ve:
        st.error(f"Error en la lectura del archivo: {ve}. Verifique el formato y contenido del archivo.")
    except Exception as e:
        st.error(f"Error inesperado: {e}.")
