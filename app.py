import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Venta de Tortas y Bizcochos", page_icon="🎂")

st.title("🎂 Sistema de Ventas - Tortas y Bizcochos")

# --- PRECIOS ---
precio_torta = 5000
precio_bizcocho = 2500

st.sidebar.header("💰 Precios")
st.sidebar.write(f"Torta: ${precio_torta}")
st.sidebar.write(f"Bizcocho: ${precio_bizcocho}")

# --- INGRESO DE DATOS ---
st.header("📋 Registrar Venta")
torta = st.number_input("Cantidad de tortas vendidas:", min_value=0, value=0)
bizcocho = st.number_input("Cantidad de bizcochos vendidos:", min_value=0, value=0)

# --- CÁLCULOS ---
total_torta = torta * precio_torta
total_bizcocho = bizcocho * precio_bizcocho
total_general = total_torta + total_bizcocho
cantidad_total = torta + bizcocho

# --- RESULTADOS ---
st.header("📊 Resumen de Ventas")
col1, col2, col3 = st.columns(3)
col1.metric("Total Tortas", f"${total_torta}")
col2.metric("Total Bizcochos", f"${total_bizcocho}")
col3.metric("Total General", f"${total_general}")

# --- ANÁLISIS ---
if cantidad_total > 0:
    st.header("📈 Análisis")

    if torta > bizcocho:
        st.success("🏆 Producto más vendido: Torta")
    elif bizcocho > torta:
        st.success("🏆 Producto más vendido: Bizcocho")
    else:
        st.info("Ambos productos se vendieron igual")

    datos = pd.DataFrame({
        "Producto": ["Torta", "Bizcocho"],
        "Unidades": [torta, bizcocho],
        "Total $": [total_torta, total_bizcocho]
    })
    st.bar_chart(datos.set_index("Producto")["Unidades"])
    st.dataframe(datos)
else:
    st.warning("Ingresá las cantidades vendidas para ver el análisis.")
    