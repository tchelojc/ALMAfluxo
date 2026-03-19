import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

# Constantes fundamentais
G = 6.67430e-11  # Constante gravitacional (m³/kg/s²)
c = 299792458    # Velocidade da luz (m/s)
ano_luz = 9.461e15  # 1 ano-luz em metros
h = 6.62607015e-34  # Constante de Planck (J·s)
q = 1.602176634e-19  # Carga do elétron (C)

# Funções compartilhadas
def distorcao_espaco_tempo(M, r, modelo):
    if modelo == "Clássico":
        return (2 * G * M) / (c**2 * r)
    elif modelo == "Fluxo Matemático":
        return (2 * G * M) / (c**2 * r) * np.cos(np.radians(9))  # Exemplo de ajuste

def energia_quantica_fluxo(f_F):
    return h * f_F

def tensao_fluxo(E_F):
    return E_F / q

def corrente_fluxo(P, V_F, theta_F):
    return (P / V_F) * np.cos(np.radians(theta_F))

def modulo_buracos_negros():
    st.header("Buracos Negros e Anomalias")
    
    # Sidebar para entrada de dados
    st.sidebar.subheader("Entrada de Dados")
    modelo = st.sidebar.radio("Escolha o Modelo", ["Clássico", "Fluxo Matemático"])
    
    # Buraco Negro
    st.sidebar.subheader("Buraco Negro")
    massa_bn = st.sidebar.number_input("Massa do Buraco Negro (kg)", value=1e31, format="%.2e", min_value=0.0)
    tamanho_bn = st.sidebar.number_input("Tamanho do Buraco Negro (anos-luz)", value=0.01, min_value=0.0)
    
    # Astros
    st.sidebar.subheader("Astros")
    num_astros = st.sidebar.number_input("Número de Astros", min_value=1, max_value=5, value=1)
    massas_astros = []
    distancias_astros = []
    
    for i in range(num_astros):
        st.sidebar.write(f"Astro {i+1}")
        massa_astro = st.sidebar.number_input(f"Massa do Astro {i+1} (kg)", value=1e30, format="%.2e", min_value=0.0)
        distancia_astro = st.sidebar.number_input(f"Distância do Astro {i+1} ao Buraco Negro (anos-luz)", value=1000.0, min_value=0.0)
        
        massas_astros.append(massa_astro)
        distancias_astros.append(distancia_astro)
    
    # Planetas
    st.sidebar.subheader("Planetas")
    num_planetas = st.sidebar.number_input("Número de Planetas", min_value=1, max_value=5, value=1)
    massas_planetas = []
    distancias_planetas = []
    
    for i in range(num_planetas):
        st.sidebar.write(f"Planeta {i+1}")
        massa_planeta = st.sidebar.number_input(f"Massa do Planeta {i+1} (kg)", value=1e24, format="%.2e", min_value=0.0)
        distancia_planeta = st.sidebar.number_input(f"Distância do Planeta {i+1} ao Astro (anos-luz)", value=1.0, min_value=0.0)
        
        massas_planetas.append(massa_planeta)
        distancias_planetas.append(distancia_planeta)
    
    # Simulação de órbitas e energia
    st.subheader("Simulação de Órbitas e Energia")
    perturbação = st.slider("Intensidade da Perturbação (Matéria Escura)", 0.0, 0.1, 0.02)
    
    # Parâmetros iniciais do planeta
    pos = np.array([5.0, 0.0])  # Posição inicial
    vel = np.array([0.0, 1.0])  # Velocidade inicial
    
    # Simulação
    dt = 0.05  # Passo de tempo
    num_passos = 1000  # Número de passos
    trajetoria = []
    energia_orbita = []
    
    for _ in range(num_passos):
        F = forca_gravitacional(pos, massa_bn, massas_planetas[0], perturbação)
        vel += F * dt  # Atualiza velocidade
        pos += vel * dt  # Atualiza posição
        trajetoria.append(pos.copy())
        
        # Cálculo da energia ao longo da órbita
        r = np.linalg.norm(pos)
        energia = -G * massa_bn * massas_planetas[0] / r
        energia_orbita.append(energia)
    
    trajetoria = np.array(trajetoria)
    energia_orbita = np.array(energia_orbita)
    
    # Visualização 3D
    fig = go.Figure()
    
    # Adicionar trajetória do planeta
    fig.add_trace(go.Scatter3d(
        x=trajetoria[:, 0],
        y=trajetoria[:, 1],
        z=np.zeros_like(trajetoria[:, 0]),
        mode="lines",
        line=dict(color="blue", width=2),
        name="Órbita do Planeta"
    ))
    
    # Adicionar buraco negro
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode="markers",
        marker=dict(size=10, color="black"),
        name="Buraco Negro"
    ))
    
    # Configurações do gráfico
    fig.update_layout(
        title="Simulação de Órbitas e Energia",
        scene=dict(
            xaxis_title="X (anos-luz)",
            yaxis_title="Y (anos-luz)",
            zaxis_title="Z (anos-luz)"
        ),
        margin=dict(l=0, r=0, b=0, t=30)
    )
    
    st.plotly_chart(fig)
    
    # Gráfico de energia ao longo da órbita
    st.subheader("Energia ao Longo da Órbita")
    fig_energia, ax = plt.subplots()
    ax.plot(energia_orbita, label="Energia Orbital (J)", color="green")
    ax.set_xlabel("Passo de Tempo")
    ax.set_ylabel("Energia (J)")
    ax.legend()
    ax.grid()
    st.pyplot(fig_energia)
    
    # Exportação de Resultados
    resultados = pd.DataFrame({
        "Passo de Tempo": np.arange(num_passos),
        "Energia Orbital (J)": energia_orbita
    })
    csv = resultados.to_csv(index=False)
    st.download_button("Baixar Resultados (CSV)", csv, file_name="resultados_orbita.csv")

# Executar o módulo
modulo_buracos_negros()