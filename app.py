import streamlit as st

st.title("Simulador de motores aeronáuticos - Grupo 2")
st.write("Streamlit funcionando!")

N2 = st.slider("Rotação normalizada N2", 0.65, 1.00, 1.00, 0.01)

st.write(f"Rotação selecionada: {N2:.2f}")
