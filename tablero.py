import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título del tablero
st.set_page_config(layout="wide")
st.title("🚍 Tablero Interactivo - Causas de Inmovilización de Buses")

# Carga de datos
@st.cache_data
def cargar_datos():
    return pd.read_excel("VARIABLES LIMPIAS.xlsx")

df = cargar_datos()

# Agrupar categorías (puedes reemplazar esta función por la tuya si la tienes definida)
def agrupar_categorias(causa):
    if "pico y placa" in str(causa).lower():
        return "Restricción de circulación"
    elif "documentación" in str(causa).lower():
        return "Documentación"
    elif "técnica" in str(causa).lower():
        return "Condición técnica"
    else:
        return "Otras"

# Aplicar agrupación
df["categoria_agrupada"] = df["Causa de la inmovilización"].apply(agrupar_categorias)

# Filtro por columna
columna = st.selectbox("Selecciona una columna para filtrar:", df.columns)
valor = st.selectbox(f"Selecciona un valor de '{columna}':", df[columna].dropna().unique())
df_filtrado = df[df[columna] == valor]

st.metric("Registros filtrados", len(df_filtrado))
st.dataframe(df_filtrado)

# Diagrama de Pareto
st.subheader("📊 Diagrama de Pareto - Causas Agrupadas")
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

# ------------------------------
# NUEVA SECCIÓN: Predicciones
# ------------------------------
if "prediccion_modelo" in df.columns:
    st.subheader("🤖 Análisis de Predicciones del Modelo")
    
    conteo_pred = df["prediccion_modelo"].value_counts()
    st.bar_chart(conteo_pred)

    st.dataframe(df[["Causa de la inmovilización", "categoria_agrupada", "prediccion_modelo"]].head(10))
else:
    st.warning("No se encontró la columna 'prediccion_modelo' en los datos.")