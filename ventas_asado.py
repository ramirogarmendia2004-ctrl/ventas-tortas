import streamlit as st
import pandas as pd
from datetime import datetime

# ─── Configuración de la página ───────────────────────────────────────────────
st.set_page_config(
    page_title="🥩 Carnicería Don Ramón",
    page_icon="🥩",
    layout="centered"
)

# ─── Estilos personalizados ────────────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lato:wght@400;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Lato', sans-serif;
            background-color: #0a0a0a;
            color: #f5e6d3;
        }
        h1, h2, h3 {
            font-family: 'Playfair Display', serif;
            color: #e53935;
        }
        .stNumberInput label, .stRadio label, .stTextInput label {
            color: #f5e6d3 !important;
            font-weight: 700;
        }
        .stButton > button {
            background-color: #e53935;
            color: white;
            font-size: 18px;
            font-weight: bold;
            border: none;
            border-radius: 10px;
            padding: 12px 30px;
            width: 100%;
            transition: background 0.3s;
        }
        .stButton > button:hover {
            background-color: #b71c1c;
        }
        .ticket {
            background: #1a1a1a;
            border: 2px dashed #e53935;
            border-radius: 15px;
            padding: 25px;
            margin-top: 20px;
        }
        .ticket h2 {
            text-align: center;
            font-size: 26px;
            margin-bottom: 10px;
            color: #e53935;
        }
        .ticket p {
            font-size: 16px;
            margin: 6px 0;
        }
        .total-line {
            font-size: 22px;
            font-weight: bold;
            color: #e53935;
            border-top: 1px solid #e53935;
            padding-top: 10px;
            margin-top: 10px;
        }
        .divider {
            border-top: 1px solid #e53935;
            margin: 20px 0;
        }
        .producto-card {
            background: #1a1a1a;
            border-radius: 12px;
            padding: 10px;
            text-align: center;
            margin-bottom: 10px;
        }
        @media print {
            .no-print { display: none !important; }
            .ticket { border: 2px dashed #000; color: #000; background: #fff; }
            body { background: #fff; color: #000; }
        }
    </style>
""", unsafe_allow_html=True)

# ─── Estado de sesión para historial ──────────────────────────────────────────
if "historial" not in st.session_state:
    st.session_state.historial = []

# ─── Encabezado ────────────────────────────────────────────────────────────────
st.markdown("<h1 style='text-align:center;'>🥩 Carnicería Don Ramón</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#e53935; font-size:18px;'>Sistema de Ventas</p>", unsafe_allow_html=True)

st.image(
    "https://images.unsplash.com/photo-1544025162-d76694265947?w=800&q=80",
    caption="El mejor asado 🥩🔥",
    use_container_width=True
)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Nombre del cliente ────────────────────────────────────────────────────────
st.markdown("## 🧑 Datos del cliente")
nombre_cliente = st.text_input("Nombre del cliente", placeholder="Ej: Juan García")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Productos ─────────────────────────────────────────────────────────────────
st.markdown("## 🛒 Seleccioná los productos")

PRODUCTOS = {
    "🥩 Matambre":   {"precio": 18500, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Matambre.jpg/320px-Matambre.jpg"},
    "🌭 Chorizo":    {"precio": 10000, "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Chorizos_argentinos.jpg/320px-Chorizos_argentinos.jpg"},
    "🍖 Chinchulin": {"precio": 9500,  "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Chinchulines.jpg/320px-Chinchulines.jpg"},
    "🖤 Morcilla":   {"precio": 6000,  "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Morcilla.jpg/320px-Morcilla.jpg"},
}

cantidades = {}
cols = st.columns(2)

for i, (nombre, datos) in enumerate(PRODUCTOS.items()):
    with cols[i % 2]:
        st.markdown("<div class='producto-card'>", unsafe_allow_html=True)
        st.image(datos["img"], use_container_width=True)
        st.markdown(f"**{nombre}**  \n💲 ${datos['precio']:,}/u")
        cantidades[nombre] = st.number_input("Cantidad", min_value=0, step=1, key=nombre)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Medio de pago ─────────────────────────────────────────────────────────────
st.markdown("## 💳 Medio de pago")

MEDIOS_DE_PAGO = {
    "💵 Efectivo":      {"recargo": 0,     "descripcion": "Sin recargo ni descuento"},
    "💳 Tarjeta":       {"recargo": 0.10,  "descripcion": "Recargo del 10%"},
    "🏦 Transferencia": {"recargo": -0.05, "descripcion": "¡5% de descuento!"},
    "📱 QR":            {"recargo": -0.05, "descripcion": "¡5% de descuento!"},
}

medio = st.radio("¿Cómo vas a pagar?", list(MEDIOS_DE_PAGO.keys()), horizontal=True)
info_pago = MEDIOS_DE_PAGO[medio]

if info_pago["recargo"] > 0:
    st.warning(f"⚠️ {info_pago['descripcion']}")
elif info_pago["recargo"] < 0:
    st.success(f"✅ {info_pago['descripcion']}")
else:
    st.info(f"ℹ️ {info_pago['descripcion']}")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Calcular ──────────────────────────────────────────────────────────────────
if st.button("🧾 Calcular total"):

    subtotal = sum(
        cantidades[nombre] * PRODUCTOS[nombre]["precio"]
        for nombre in PRODUCTOS
    )

    ajuste = subtotal * info_pago["recargo"]
    total = subtotal + ajuste

    if subtotal == 0:
        st.error("❌ Ingresá al menos un producto.")
    elif not nombre_cliente.strip():
        st.error("❌ Ingresá el nombre del cliente.")
    else:
        hora_venta = datetime.now().strftime("%H:%M:%S")
        fecha_venta = datetime.now().strftime("%d/%m/%Y")

        lineas_html = ""
        detalle_items = []
        for nombre, datos in PRODUCTOS.items():
            cant = cantidades[nombre]
            if cant > 0:
                subtot_item = cant * datos["precio"]
                lineas_html += f"<p>{nombre} x{cant} → <strong>${subtot_item:,.0f}</strong></p>"
                detalle_items.append(f"{nombre} x{cant}")

        signo = "+" if ajuste >= 0 else ""
        ajuste_label = (
            f"Recargo ({int(info_pago['recargo']*100)}%)"
            if ajuste > 0
            else f"Descuento ({int(abs(info_pago['recargo'])*100)}%)"
        )

        st.markdown(f"""
        <div class='ticket' id='ticket'>
            <h2>🧾 Carnicería Don Ramón</h2>
            <p>📅 Fecha: <strong>{fecha_venta}</strong> | 🕐 Hora: <strong>{hora_venta}</strong></p>
            <p>🧑 Cliente: <strong>{nombre_cliente}</strong></p>
            <hr style='border-color:#e53935;'>
            {lineas_html}
            <p>Subtotal: <strong>${subtotal:,.0f}</strong></p>
            <p>{ajuste_label}: <strong>{signo}${ajuste:,.0f}</strong></p>
            <p class='total-line'>TOTAL A PAGAR ({medio}): ${total:,.0f}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <br>
        <div class='no-print' style='text-align:center;'>
            <button onclick='window.print()' style='
                background:#e53935; color:white;
                font-size:16px; font-weight:bold;
                border:none; border-radius:10px;
                padding:10px 30px; cursor:pointer;'>
                🖨️ Imprimir ticket
            </button>
        </div>
        """, unsafe_allow_html=True)

        st.session_state.historial.append({
            "Hora": hora_venta,
            "Cliente": nombre_cliente,
            "Productos": ", ".join(detalle_items),
            "Subtotal": f"${subtotal:,.0f}",
            "Medio de pago": medio,
            "Total": f"${total:,.0f}",
        })

        st.balloons()

# ─── Historial del día ─────────────────────────────────────────────────────────
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
st.markdown("## 📊 Historial de ventas del día")

if st.session_state.historial:
    df = pd.DataFrame(st.session_state.historial)
    st.dataframe(df, use_container_width=True)

    totales_num = []
    for row in st.session_state.historial:
        val = row["Total"].replace("$", "").replace(",", "")
        try:
            totales_num.append(float(val))
        except:
            totales_num.append(0)

    total_dia = sum(totales_num)
    st.success(f"💰 Total recaudado hoy: **${total_dia:,.0f}**")

    if st.button("🗑️ Limpiar historial"):
        st.session_state.historial = []
        st.rerun()
else:
    st.info("Aún no hay ventas registradas hoy.")

# ─── Pie ───────────────────────────────────────────────────────────────────────
st.markdown("<br><p style='text-align:center; color:#888;'>🥩 Carnicería Don Ramón © 2026</p>", unsafe_allow_html=True)