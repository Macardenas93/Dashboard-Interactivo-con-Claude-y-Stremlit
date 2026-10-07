import streamlit as st
import pandas as pd

# Configuración de la página (siempre debe ser el primer comando de Streamlit)
st.set_page_config(
    page_title="Dashboard de ventas",
    page_icon="📊",
    layout="wide",
)

# Cargar el archivo CSV (debe estar en la misma carpeta que app.py)
df = pd.read_csv("datos.csv")

# Convertir la columna fecha a tipo fecha
df["fecha"] = pd.to_datetime(df["fecha"])

# ---------- BARRA LATERAL: FILTROS ----------
st.sidebar.header("Filtros")

# Filtro de rango de fechas
fecha_min = df["fecha"].min().date()
fecha_max = df["fecha"].max().date()

rango = st.sidebar.date_input(
    "Rango de fechas",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max,
)

# Filtro de categorías (una o varias)
todas_categorias = sorted(df["categoria"].unique())

categorias = st.sidebar.multiselect(
    "Categorías",
    options=todas_categorias,
    default=todas_categorias,
)

# ---------- ENCABEZADO ----------
st.title("📊 Dashboard de ventas")
st.caption("Resumen de las ventas de la tienda. Usa los filtros de la barra lateral para explorar los datos.")

# ---------- APLICAR LOS FILTROS ----------
# Mientras el usuario elige el rango puede haber solo una fecha;
# en ese caso esperamos a que elija las dos.
if len(rango) != 2:
    st.info("Selecciona la fecha de inicio y la fecha de fin en la barra lateral.")
    st.stop()

fecha_inicio, fecha_fin = rango

df_filtrado = df[
    (df["fecha"].dt.date >= fecha_inicio)
    & (df["fecha"].dt.date <= fecha_fin)
    & (df["categoria"].isin(categorias))
]

# Si no hay datos con esos filtros, avisamos y paramos
if df_filtrado.empty:
    st.warning("No hay datos con los filtros seleccionados. Prueba con otro rango o categoría.")
    st.stop()

# ---------- SECCIÓN 1: INDICADORES CLAVE (KPIs) ----------
st.header("Indicadores clave")

total_ventas = df_filtrado["total"].sum()
operaciones = len(df_filtrado)
ticket_promedio = total_ventas / operaciones
unidades = df_filtrado["cantidad"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.metric("Total de ventas", f"{total_ventas:,.2f}")

with col2:
    with st.container(border=True):
        st.metric("Operaciones", f"{operaciones:,}")

with col3:
    with st.container(border=True):
        st.metric("Ticket promedio", f"{ticket_promedio:,.2f}")

with col4:
    with st.container(border=True):
        st.metric("Unidades vendidas", f"{unidades:,}")

# ---------- SECCIÓN 2: ANÁLISIS VISUAL ----------
st.header("Análisis visual")

graf1, graf2 = st.columns(2)

with graf1:
    st.subheader("Ventas por categoría")
    ventas_categoria = df_filtrado.groupby("categoria")["total"].sum()
    st.bar_chart(ventas_categoria)

with graf2:
    st.subheader("Evolución de las ventas")
    ventas_fecha = df_filtrado.groupby("fecha")["total"].sum()
    st.line_chart(ventas_fecha)

# ---------- SECCIÓN 3: DETALLE DE LOS DATOS ----------
st.header("Detalle de los datos")
st.write(f"Mostrando **{len(df_filtrado)}** de **{len(df)}** filas.")
st.dataframe(df_filtrado, use_container_width=True)