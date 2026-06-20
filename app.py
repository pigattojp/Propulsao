import streamlit as st
import pandas as pd

from simulador import(
    dados_ex22,
    dados_ex72,
    simular_turbofan,
    simular_turbojato,
    simular_ramjet,
    simular_turbohelice
)

st.set_page_config(
    page_title="Simulador",
    layout="wide"
)

st.title("Simulador de motores aeronáuticos")

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
Ta = st.sidebar.number_input("Temperatura ambiente Ta em [K]", value=288.15)
Pa = st.sidebar.number_input("Pressão ambiente Pa em [kPa]", value=101.3)

if tipo_motor == "Turbo-hélice":
    dados = dados_ex72.copy()
else:
    dados = dados_ex22.copy()

dados["M"] = Mach
dados["Ta"] = Ta
dados["Pa"] = Pa

if tipo_motor == "Turbofan":
    resultado = simular_turbofan(
        dados,
        fora_de_projeto=fora_de_projeto,
        N2=N2
    )

elif tipo_motor == "Turbojato":
    resultado = simular_turbojato(
        dados,
        fora_de_projeto=fora_de_projeto,
        N2=N2
    )

elif tipo_motor == "Ramjet":
    resultado = simular_ramjet(
        dados,
        fora_de_projeto=fora_de_projeto,
        N2=N2
    )

elif tipo_motor == "Turbo-hélice":
    resultado = simular_turbohelice(
        dados,
        fora_de_projeto=fora_de_projeto,
        N2=N2
    )

st.write("## Entradas selecionadas")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Motor", tipo_motor)
col2.metric("N2", f"{N2:.2f}")
col3.metric("Mach", f"{Mach:.2f}")
col4.metric("Ta [K]", f"{Ta:.2f}")
col5.metric("Pa [kPa]", f"{Pa:.2f}")

st.write("## Resultados principais")

if tipo_motor in ["Turbofan", "Turbojato", "Ramjet"]:
    desempenho = resultado["DESEMPENHO GLOBAL"]

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Empuxo total [kN]",
        f"{desempenho['Empuxo Total [kN]']:.2f}"
    )

    col2.metric(
        "Empuxo específico [m/s]",
        f"{desempenho['Empuxo Específico [m/s]']:.2f}"
    )

    col3.metric(
        "TSFC [kg/(kN.s)]",
        f"{desempenho['Consumo Específico (TSFC) [kg/(kN.s)]']:.6f}"
    )

    col4.metric(
        "Combustível [kg/h]",
        f"{desempenho['Consumo total de combustível [kg/h]']:.2f}"
    )

else:
    helice = resultado["HÉLICE E CAIXA"]
    consumo = resultado["CONSUMO"]
    turbina = resultado["TURBINA LIVRE"]

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Potência turbina [kW]",
        f"{turbina['Potência da turbina [kW]']:.2f}"
    )

    col2.metric(
        "Potência útil hélice [kW]",
        f"{helice['Potência útil na hélice [kW]']:.2f}"
    )

    col3.metric(
        "Empuxo total [kN]",
        f"{helice['Empuxo total [kN]']:.2f}"
    )

    col4.metric(
        "BSFC [kg/(kW.s)]",
        f"{consumo['Consumo esp. no eixo BSFC [kg/(kW.s)]']:.8f}"
    )
    
    col5.metric(
        "TSFC [kg/(kN.s)]",
        f"{consumo['TSFC [kg/(kN.s)]']:.6f}"
    )

st.write("## Detalhamento da simulação")

linhas = []

for secao, dados_secao in resultado.items():
    for parametro, valor in dados_secao.items():
        linhas.append({
            "Seção": secao,
            "Parâmetro": parametro,
            "Valor": valor
        })

df_resultados = pd.DataFrame(linhas)

def formatar_valor(x):
    if isinstance(x, (int, float)):
        if abs(x) >= 100:
            return f"{x:.2f}"
        elif abs(x) >= 1:
            return f"{x:.4f}"
        else:
            return f"{x:.6f}"
    return x

df_resultados["Valor"] = df_resultados["Valor"].apply(formatar_valor)

st.dataframe(
    df_resultados,
    use_container_width=True,
    hide_index=True,
    height=500
)
