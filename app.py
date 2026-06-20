import streamlit as st

st.set_page_config(
    page_title="Simulador",
    layout="wide"
)

st.title("Simulador de motores aeronáuticos - Grupo 2")

st.sidebar.header("Entradas")

tipo_motor = st.sidebar.selectbox(
    "Tipo de motor",
    ["Turbofan", "Turbojato", "Ramjet", "Turbo-hélice"]
)

fora_de_projeto = st.sidebar.checkbox("Fora do ponto de projeto")

N2 = st.sidebar.slider(
    "Rotação normalizada N2",
    0.65, 1.00, 1.00, 0.01
)

Mach = st.sidebar.number_input("Mach", value=0.0, step=0.05)
Ta = st.sidebar.number_input("Temperatura ambiente Ta [K]", value=288.15)
Pa = st.sidebar.number_input("Pressão ambiente em [kPa]", value=101.3)

st.write("## Entradas selecionadas")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Motor", tipo_motor)
col2.metric("N2", f"{N2:.2f}")
col3.metric("Mach", f"{Mach:.2f}")
col4.metric("Ta [K]", f"{Ta:.2f}")

st.info("Próximo passo: conectar essas entradas às funções do simulador")
