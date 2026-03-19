import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

# Título do aplicativo
st.title("Universo Áurea - Tudo em Um")

# Sidebar para inputs do usuário
st.sidebar.header("Parâmetros de Entrada")
massa = st.sidebar.slider("Massa (kg)", 1e-30, 1e50, 5.972e24)  # Escala variável
distancia = st.sidebar.slider("Distância (metros)", 1e-12, 1e25, 1e6)  # Escala variável
probabilidade = st.sidebar.slider("Probabilidade", 0.0, 1.0, 0.5)
investimento_total = st.sidebar.number_input("Investimento Total", value=1000.0)

# Funções dos módulos
def calcular_gravidade(massa, distancia):
    G = 6.67430e-11  # Constante gravitacional
    return G * massa / distancia**2

def calcular_frequencia(massa, distancia):
    G = 6.67430e-11
    return np.sqrt(G * massa / distancia**3) / (2 * np.pi)

def calcular_energia(massa):
    c = 299792458  # Velocidade da luz
    return massa * c**2

def calcular_odds(probabilidade):
    return 1 / probabilidade

def redistribuir_apostas(odds, investimento_total):
    return investimento_total / odds

def calcular_singularidade(massa, distancia):
    phi = (1 + np.sqrt(5)) / 2  # Proporção áurea
    return (massa * distancia) / phi

def calcular_funcao_onda(distancia, massa):
    h = 6.62607015e-34  # Constante de Planck
    return np.sin((2 * np.pi * massa * distancia) / h)

# Função da Bobina Áurea
def bobina_aurea(valor):
    phi = (1 + np.sqrt(5)) / 2  # Proporção áurea
    valor_ajustado = valor / phi  # Ajusta o valor para a proporção áurea
    return valor_ajustado

# Abas para cada módulo
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Gravidade e Buracos Negros", 
    "Frequências e Ressonância", 
    "Territórios e Zonas de Calor", 
    "Desequilíbrios e Energia", 
    "Valores Infinitos e Operador",
    "Ajuda e Orientação"
])

# Aba 1: Gravidade e Buracos Negros
with tab1:
    st.header("Gravidade e Buracos Negros")
    gravidade = calcular_gravidade(massa, distancia)
    gravidade_ajustada = bobina_aurea(gravidade)
    st.write(f"Gravidade: {gravidade:.6e} m/s²")
    st.write(f"Gravidade Ajustada (Bobina Áurea): {gravidade_ajustada:.6e} m/s²")

    # Gráfico 3D de Gravidade vs Distância vs Massa
    distancias = np.linspace(distancia / 10, distancia * 10, 100)
    massas = np.linspace(massa / 10, massa * 10, 100)
    gravidades = [[calcular_gravidade(m, d) for d in distancias] for m in massas]

    fig = go.Figure(data=[go.Surface(z=gravidades, x=distancias, y=massas)])
    fig.update_layout(title="Gravidade vs Distância vs Massa", scene=dict(
        xaxis_title="Distância (m)",
        yaxis_title="Massa (kg)",
        zaxis_title="Gravidade (m/s²)"
    ))
    st.plotly_chart(fig)

# Aba 2: Frequências e Ressonância
with tab2:
    st.header("Frequências e Ressonância")
    frequencia = calcular_frequencia(massa, distancia)
    frequencia_ajustada = bobina_aurea(frequencia)
    st.write(f"Frequência Harmônica: {frequencia:.6e} Hz")
    st.write(f"Frequência Ajustada (Bobina Áurea): {frequencia_ajustada:.6e} Hz")

    # Gráfico de Frequência vs Distância
    distancias = np.linspace(distancia / 10, distancia * 10, 100)
    frequencias = [calcular_frequencia(massa, d) for d in distancias]
    frequencias_ajustadas = [bobina_aurea(f) for f in frequencias]

    fig, ax = plt.subplots()
    ax.plot(distancias, frequencias, label="Frequência Original")
    ax.plot(distancias, frequencias_ajustadas, label="Frequência Ajustada (Bobina Áurea)")
    ax.set_title("Frequência Harmônica vs Distância")
    ax.set_xlabel("Distância (m)")
    ax.set_ylabel("Frequência (Hz)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Aba 3: Territórios e Zonas de Calor
with tab3:
    st.header("Territórios e Zonas de Calor")
    energia = calcular_energia(massa)
    energia_ajustada = bobina_aurea(energia)
    st.write(f"Energia: {energia:.6e} Joules")
    st.write(f"Energia Ajustada (Bobina Áurea): {energia_ajustada:.6e} Joules")

    # Mapa de Calor de Zonas Energéticas
    mapa = folium.Map(location=[-15.788497, -47.879873], zoom_start=4)  # Exemplo: Brasília
    # Linha 115 (corrigida)
folium.TileLayer(
    tiles='https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
    attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.',
    name='Stamen Toner'
).add_to(mapa)
    folium_static(mapa)

# Aba 4: Desequilíbrios e Energia
with tab4:
    st.header("Desequilíbrios e Energia")
    singularidade = calcular_singularidade(massa, distancia)
    singularidade_ajustada = bobina_aurea(singularidade)
    st.write(f"Singularidade: {singularidade:.6e}")
    st.write(f"Singularidade Ajustada (Bobina Áurea): {singularidade_ajustada:.6e}")

    # Gráfico de Singularidade vs Distância
    distancias = np.linspace(distancia / 10, distancia * 10, 100)
    singularidades = [calcular_singularidade(massa, d) for d in distancias]
    singularidades_ajustadas = [bobina_aurea(s) for s in singularidades]

    fig, ax = plt.subplots()
    ax.plot(distancias, singularidades, label="Singularidade Original")
    ax.plot(distancias, singularidades_ajustadas, label="Singularidade Ajustada (Bobina Áurea)")
    ax.set_title("Singularidade vs Distância")
    ax.set_xlabel("Distância (m)")
    ax.set_ylabel("Singularidade")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Aba 5: Valores Infinitos e Operador
with tab5:
    st.header("Valores Infinitos e Operador")
    odds = calcular_odds(probabilidade)
    odds_ajustada = bobina_aurea(odds)
    st.write(f"ODDS: {odds:.2f}")
    st.write(f"ODDS Ajustada (Bobina Áurea): {odds_ajustada:.2f}")
    st.write(f"Redistribuição de Apostas: {redistribuir_apostas(odds, investimento_total):.2f}")

    # Gráfico de ODDS vs Probabilidade
    probabilidades = np.linspace(0.01, 1.0, 100)
    odds_list = [calcular_odds(p) for p in probabilidades]
    odds_ajustadas = [bobina_aurea(o) for o in odds_list]

    fig, ax = plt.subplots()
    ax.plot(probabilidades, odds_list, label="ODDS Original")
    ax.plot(probabilidades, odds_ajustadas, label="ODDS Ajustada (Bobina Áurea)")
    ax.set_title("ODDS vs Probabilidade")
    ax.set_xlabel("Probabilidade")
    ax.set_ylabel("ODDS")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Aba 6: Ajuda e Orientação
with tab6:
    st.header("Ajuda e Orientação")
    st.write("### Como Usar o Universo Áurea")
    st.write("""
    1. **Parâmetros de Entrada**: Ajuste os valores de massa, distância, probabilidade e investimento total na barra lateral.
    2. **Módulos**: Navegue pelas abas para visualizar os cálculos e gráficos de cada módulo.
    3. **Bobina Áurea**: Todos os cálculos são ajustados automaticamente pela Bobina Áurea para garantir harmonia.
    4. **Feedback**: Verifique se os valores estão em harmonia (verde) ou desequilíbrio (vermelho).
    """)

    st.write("### Tópicos de Ajuda")
    st.write("""
    - **Gravidade e Buracos Negros**: Cálculos de gravidade e distorções no espaço-tempo.
    - **Frequências e Ressonância**: Análise de frequências harmônicas e ressonâncias.
    - **Territórios e Zonas de Calor**: Mapeamento de zonas energéticas e desequilíbrios.
    - **Desequilíbrios e Energia**: Transformação de energia e singularidades.
    - **Valores Infinitos e Operador**: Aplicação da Lei Áurea na bolsa de valores e apostas.
    """)

    st.write("### Encontrou um Erro?")
    st.write("""
    - Verifique se os parâmetros de entrada estão dentro dos limites recomendados.
    - Se o problema persistir, entre em contato com o suporte ou envie feedback.
    """)

    st.write("### Aprimoramentos")
    st.write("""
    - Adicione mais funcionalidades ou contextos conforme necessário.
    - Compartilhe suas sugestões para melhorar o aplicativo.
    """)

# Rodapé
st.sidebar.markdown("---")
st.sidebar.write("### Feedback e Suporte")
st.sidebar.write("Encontrou um problema ou tem uma sugestão? Envie um e-mail para suporte@universoaureo.com.")