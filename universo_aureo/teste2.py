import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

# Título do aplicativo
st.title("Universo Áurea - Módulos Integrados")

# Sidebar para escolha do módulo
st.sidebar.header("Escolha o Módulo")
modulo = st.sidebar.radio(
    "Selecione o módulo:",
    [
        "Buracos Negros e Anomalias",
        "Captação e Transformação de Energia",
        "Sistema Planetário e Espaço-Tempo",
        "Frequências Áureas e Territórios",
        "Bolsa de Valores e Apostas",
        "Ajuda e Orientação"
    ]
)

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

def bobina_aurea(valor):
    phi = (1 + np.sqrt(5)) / 2  # Proporção áurea
    return valor / phi  # Ajusta o valor para a proporção áurea

# Módulo 1: Buracos Negros e Anomalias
if modulo == "Buracos Negros e Anomalias":
    st.header("Buracos Negros e Anomalias")
    massa_buraco = st.number_input("Massa do Buraco Negro (kg)", value=1e30)
    distancia_buraco = st.number_input("Distância do Buraco Negro (metros)", value=1e6)
    
    gravidade = calcular_gravidade(massa_buraco, distancia_buraco)
    gravidade_ajustada = bobina_aurea(gravidade)
    st.write(f"Gravidade: {gravidade:.6e} m/s²")
    st.write(f"Gravidade Ajustada (Bobina Áurea): {gravidade_ajustada:.6e} m/s²")

    # Gráfico de Gravidade vs Distância
    distancias = np.linspace(distancia_buraco / 10, distancia_buraco * 10, 100)
    gravidades = [calcular_gravidade(massa_buraco, d) for d in distancias]
    gravidades_ajustadas = [bobina_aurea(g) for g in gravidades]

    fig, ax = plt.subplots()
    ax.plot(distancias, gravidades, label="Gravidade Original")
    ax.plot(distancias, gravidades_ajustadas, label="Gravidade Ajustada (Bobina Áurea)")
    ax.set_title("Gravidade vs Distância")
    ax.set_xlabel("Distância (m)")
    ax.set_ylabel("Gravidade (m/s²)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Módulo 2: Captação e Transformação de Energia
elif modulo == "Captação e Transformação de Energia":
    st.header("Captação e Transformação de Energia")
    massa_energia = st.number_input("Massa para Conversão (kg)", value=1.0)
    energia = calcular_energia(massa_energia)
    energia_ajustada = bobina_aurea(energia)
    st.write(f"Energia: {energia:.6e} Joules")
    st.write(f"Energia Ajustada (Bobina Áurea): {energia_ajustada:.6e} Joules")

    # Gráfico de Energia vs Massa
    massas = np.linspace(massa_energia / 10, massa_energia * 10, 100)
    energias = [calcular_energia(m) for m in massas]
    energias_ajustadas = [bobina_aurea(e) for e in energias]

    fig, ax = plt.subplots()
    ax.plot(massas, energias, label="Energia Original")
    ax.plot(massas, energias_ajustadas, label="Energia Ajustada (Bobina Áurea)")
    ax.set_title("Energia vs Massa")
    ax.set_xlabel("Massa (kg)")
    ax.set_ylabel("Energia (Joules)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Módulo 3: Sistema Planetário e Espaço-Tempo
elif modulo == "Sistema Planetário e Espaço-Tempo":
    st.header("Sistema Planetário e Espaço-Tempo")
    massa_astro = st.number_input("Massa do Astro (kg)", value=5.972e24)
    distancia_planeta = st.number_input("Distância do Planeta (metros)", value=1e6)
    
    singularidade = calcular_singularidade(massa_astro, distancia_planeta)
    singularidade_ajustada = bobina_aurea(singularidade)
    st.write(f"Singularidade: {singularidade:.6e}")
    st.write(f"Singularidade Ajustada (Bobina Áurea): {singularidade_ajustada:.6e}")

    # Gráfico de Singularidade vs Distância
    distancias = np.linspace(distancia_planeta / 10, distancia_planeta * 10, 100)
    singularidades = [calcular_singularidade(massa_astro, d) for d in distancias]
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

# Módulo 4: Frequências Áureas e Territórios
elif modulo == "Frequências Áureas e Territórios":
    st.header("Frequências Áureas e Territórios")
    frequencia = st.number_input("Frequência Observada (Hz)", value=1.0)
    frequencia_ajustada = bobina_aurea(frequencia)
    st.write(f"Frequência: {frequencia:.6e} Hz")
    st.write(f"Frequência Ajustada (Bobina Áurea): {frequencia_ajustada:.6e} Hz")

    # Mapa de Calor de Zonas Energéticas
    mapa = folium.Map(location=[-15.788497, -47.879873], zoom_start=4)  # Exemplo: Brasília
    folium.TileLayer(
        tiles='https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
        attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.',
        name='Stamen Toner'
    ).add_to(mapa)
    folium_static(mapa)

# Módulo 5: Bolsa de Valores e Apostas
elif modulo == "Bolsa de Valores e Apostas":
    st.header("Bolsa de Valores e Apostas")
    probabilidade = st.slider("Probabilidade", 0.0, 1.0, 0.5)
    investimento_total = st.number_input("Investimento Total", value=1000.0)
    
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

# Módulo 6: Ajuda e Orientação
elif modulo == "Ajuda e Orientação":
    st.header("Ajuda e Orientação")
    st.write("### Como Usar o Universo Áurea")
    st.write("""
    1. **Selecione o Módulo**: Escolha o módulo desejado na barra lateral.
    2. **Insira os Parâmetros**: Ajuste os valores de entrada conforme necessário.
    3. **Visualize os Resultados**: Gráficos, mapas e cálculos serão exibidos automaticamente.
    4. **Ajuste com a Bobina Áurea**: Todos os cálculos são ajustados para garantir harmonia.
    """)

    st.write("### Tópicos de Ajuda")
    st.write("""
    - **Buracos Negros e Anomalias**: Analise o impacto de buracos negros e detecte anomalias.
    - **Captação e Transformação de Energia**: Simule a captação e transformação de energia.
    - **Sistema Planetário e Espaço-Tempo**: Calcule distorções no espaço-tempo.
    - **Frequências Áureas e Territórios**: Analise frequências e resolva problemas.
    - **Bolsa de Valores e Apostas**: Calcule investimentos e redistribuição de apostas.
    """)

    st.write("### Encontrou um Erro?")
    st.write("""
    - Verifique se os parâmetros de entrada estão dentro dos limites recomendados.
    - Se o problema persistir, entre em contato com o suporte.
    """)

# Rodapé
st.sidebar.markdown("---")
st.sidebar.write("### Feedback e Suporte")
st.sidebar.write("Encontrou um problema ou tem uma sugestão? Envie um e-mail para suporte@universoaureo.com.")