import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de página
st.set_page_config(layout="wide")
st.title("🚍 Tablero Interactivo - Causas de Inmovilización de Buses")

# Cargar los datos desde el archivo Excel
@st.cache_data
def cargar_datos():
    return pd.read_excel("VARIABLES_PREDICCION.xlsx")

df = cargar_datos()

# Mostrar el DataFrame completo (puedes ocultarlo si deseas)
st.subheader("📋 Datos completos")
st.dataframe(df)

# Filtro por columna
st.subheader("🔍 Filtrado de datos")
columna = st.selectbox("Selecciona una columna para filtrar:", df.columns)
valor = st.selectbox(f"Selecciona un valor de '{columna}':", df[columna].dropna().unique())
df_filtrado = df[df[columna] == valor]

st.metric("Registros filtrados", len(df_filtrado))
st.dataframe(df_filtrado)

# Diagrama de Pareto para la columna 'categoria_agrupada'
st.subheader("📊 Diagrama de Pareto - Categorías Agrupadas")

if "categoria_agrupada" in df.columns:
    conteo = df["categoria_agrupada"].value_counts()
    porcentaje = (conteo / conteo.sum()) * 100
    pareto_df = pd.DataFrame({"Frecuencia": conteo, "Porcentaje": porcentaje})
    pareto_df["Acumulado"] = pareto_df["Porcentaje"].cumsum()

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(pareto_df.index, pareto_df["Frecuencia"], color='skyblue')
    ax2 = ax1.twinx()
    ax2.plot(pareto_df.index, pareto_df["Acumulado"], color='red', marker='o')

    ax1.set_ylabel("Frecuencia")
    ax2.set_ylabel("Porcentaje Acumulado")
    plt.title("Diagrama de Pareto de Categorías Agrupadas")
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.warning("No se encontró la columna 'categoria_agrupada'.")

# Nueva sección: Visualización de predicciones
st.subheader("🤖 Predicciones del Modelo")

if "prediccion_modelo" in df.columns:
    conteo_pred = df["prediccion_modelo"].value_counts()
    st.bar_chart(conteo_pred)

    st.dataframe(df[["Causa de la inmovilización", "categoria_agrupada", "prediccion_modelo"]].head(10))
else:
    st.info("No se encontró la columna 'prediccion_modelo'. Asegúrate de exportarla desde el modelo.")
