import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
st.title('Visualización de Datos de Excel')
st.write('Sube tu archivo Excel para visualizar y filtrar los datos.')

# Subir archivo Excel
uploaded_file = st.file_uploader("Elige un archivo Excel", type=['xlsx', 'xls'])

# Estado de sesión para filtros
if 'filters' not in st.session_state:
    st.session_state.filters = {}

def reset_filters():
    st.session_state.filters = {}
    st.experimental_rerun()

if uploaded_file is not None:
    # Leer el archivo Excel
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
        st.stop()

    # Validar columnas requeridas
    required_columns = ['Categoria', 'Club', 'Genero']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Las siguientes columnas faltan en el archivo: {', '.join(missing_columns)}")
        st.stop()

    # Barra lateral para los filtros
    with st.sidebar.expander("Filtros", expanded=True):
        for col in required_columns:
            options = ['Todos'] + sorted(df[col].dropna().unique().tolist())
            selected = st.selectbox(f'Filtrar por {col}', options, key=col)
            if selected != 'Todos':
                st.session_state.filters[col] = selected
            else:
                st.session_state.filters.pop(col, None)

        # Botón para limpiar filtros
        st.button('Limpiar Filtros', on_click=reset_filters)

    # Aplicar los filtros seleccionados
    filtered_df = df.copy()
    for col, selected in st.session_state.filters.items():
        filtered_df = filtered_df[filtered_df[col] == selected]

    # Resetea el índice y elimina la columna de índice
    filtered_df.reset_index(drop=True, inplace=True)

    # Limitar a las primeras 1000 filas
    max_rows = 1000
    if len(filtered_df) > max_rows:
        st.warning(f"Mostrando las primeras {max_rows} filas de {len(filtered_df)} filas totales.")
        filtered_df = filtered_df.head(max_rows)

    # Selección de columnas a mostrar
    st.write("Selecciona las columnas que deseas ver:")
    all_columns = filtered_df.columns.tolist()
    columnas_seleccionadas = st.multiselect(
        "Selecciona las columnas",
        options=all_columns,
        default=all_columns
    )

    # Crear la tabla con Plotly
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[f'<b>{col}</b>' for col in columnas_seleccionadas],
            fill_color='#1f77b4',
            font=dict(color='white', size=12),
            align='center',
            line_color='darkslategray',
            height=30,
        ),
        cells=dict(
            values=[filtered_df[col].tolist() for col in columnas_seleccionadas],
            fill_color='lavender',
            align='center',
            line_color='darkslategray',
            height=30,
        )
    )])

    # Ajustar el layout
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
    )

    # Mostrar la tabla
    st.write("Datos:")
    st.plotly_chart(fig, use_container_width=True)
