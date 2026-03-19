"""
═══════════════════════════════════════════════════════════════════════════════
    🌌 UNIVERSO ÁUREO - FLUXO MATEMÁTICO (VERSÃO EXPANDIDA)
    
    Este sistema unifica matemática clássica, física quântica, geometria sagrada
    e o Fluxo Matemático de Catharino, permitindo explorar padrões universais
    através das constantes π, φ, Fibonacci, 1,80 (Gratidão), 0,54 (Marc),
    0,18 (Deus), constantes de Planck, gravidade da Terra e gravidade quântica.
    
    Versão: 10.0.0 - Expansão de Padrões e Validações
    Autor: Marcelo Jubilado Catharino (aprimorado)
    Data: 2025
    
    CARACTERÍSTICAS PRINCIPAIS:
    - Todas as funções originais preservadas e aprimoradas
    - Mais de 2500 linhas de código explicativo e comentado
    - Novas seções: Padrões e Validações, Todas as Mentes, Gravidade Quântica
    - Validação automática de resultados com π, φ, Fibonacci, 1,80, etc.
    - Visualizações expandidas e explicações detalhadas
    - Relógio Quântico mantido em tempo espiralado
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import base64
from io import BytesIO
import time
import math
import datetime
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import pytz
from datetime import datetime as dt
from PIL import Image
import random
import hashlib
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURAÇÃO INICIAL DA PÁGINA
# =============================================================================
st.set_page_config(
    layout="wide",
    page_title="🌌 Universo Áureo - Fluxo Matemático Expandido",
    page_icon="🌀",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CONSTANTES E CONFIGURAÇÕES GLOBAIS (ORIGINAIS + NOVAS)
# =============================================================================
FREQUENCIA_BASE = 432  # Hz
PULSOS_POR_GIRO = 432 * 9  # 9 Vibes
GIROS_POR_CICLO = 9
CICLOS_POR_ERA = 9
SINGULARIDADE = datetime.datetime(2023, 3, 9, 0, 0, 0, tzinfo=pytz.UTC)

# Constantes do Fluxo Matemático (Catharino) - preservadas
MARC = 0.54          # Constante fundamental de transição
DEUS = 0.18          # Trindade (0,06 × 3) – representa a unidade trina
GRATIDAO = 1.80      # Equilíbrio universal (3 × 0,6)
PHI = 1.618033988749895  # Proporção áurea (Fibonacci)

# Constantes físicas (originais)
C_LUZ = 299792458          # m/s
H_PLANCK = 6.62607015e-34  # J·s
G_NEWTON = 6.67430e-11     # N·m²/kg²
MU0 = 4 * np.pi * 1e-7     # Permeabilidade do vácuo
GRAVIDADE_TERRA = 9.80665  # m/s²

# NOVAS CONSTANTES para expansão
PI = math.pi                # 3.141592653589793
GRAVIDADE_QUANTICA = 1.0e-43  # Exemplo: força gravitacional na escala de Planck (m/s²)
CONSTANTE_ESTRUTURA_FINA = 0.0072973525693  # α ≈ 1/137
PLANCK_MASSA = 2.176434e-8   # kg
PLANCK_COMPRIMENTO = 1.616255e-35  # m
PLANCK_TEMPO = 5.391247e-44   # s
PLANCK_ENERGIA = 1.956e9      # J

# =============================================================================
# FUNÇÕES MATEMÁTICAS BASE (FLUXO MATEMÁTICO) - ORIGINAIS, NÃO MODIFICADAS
# =============================================================================

def reduzir_teosoficamente(n):
    """
    Redução teosófica: soma dos dígitos até um único dígito (1-9).
    Funciona com números inteiros ou float, removendo pontos e sinais.
    """
    try:
        # Converte para string e remove caracteres não numéricos
        str_num = str(n).replace('.', '').replace('-', '')
        # Se for notação científica, simplifica
        if 'e' in str_num.lower():
            n_float = float(n)
            str_num = f"{n_float:.0f}".replace('.', '')
        while len(str_num) > 1:
            str_num = str(sum(int(d) for d in str_num if d.isdigit()))
        return int(str_num)
    except Exception:
        return 0

def fator_fluxo(N):
    """
    Calcula F(N) = C(N) + R(N)/10
    onde C(N) = ciclo (N // 9) e R(N) = redução teosófica de N.
    """
    try:
        N = int(abs(N))
        ciclo = N // 9
        reducao = reduzir_teosoficamente(N)
        return ciclo + reducao / 10.0
    except:
        return 0.0

def operacao_dual(a, b, operador, modo='classico', entrelacamento=0.54):
    """
    Realiza operação matemática nos modos:
    - 'classico': resultado padrão
    - 'fluxo': resultado clássico * entrelacamento * fator_fluxo (se aplicável)
    - 'dual': retorna (clássico, fluxo)
    Suporta +, -, *, /, **, %, //
    """
    try:
        a = float(a)
        b = float(b)
    except:
        return None, "Entrada inválida"

    # Operações básicas
    if operador == '+':
        res = a + b
    elif operador == '-':
        res = a - b
    elif operador == '*':
        res = a * b
    elif operador == '/':
        if b == 0:
            return None, "Divisão por zero"
        res = a / b
    elif operador == '**':
        res = a ** b
    elif operador == '%':
        res = a % b
    elif operador == '//':
        if b == 0:
            return None, "Divisão por zero"
        res = a // b
    else:
        return None, "Operador desconhecido"

    if modo == 'classico':
        return res, "Cálculo clássico"
    elif modo == 'fluxo':
        # Aplica constante de fluxo e entrelaçamento
        res_fluxo = res * entrelacamento
        # Se for multiplicação/potência, aplica também fator de fluxo baseado nos números
        if operador in ('*', '**'):
            f = fator_fluxo(reduzir_teosoficamente(a) * 10 + reduzir_teosoficamente(b))
            res_fluxo *= f
        return res_fluxo, f"Aplicado fluxo ×{entrelacamento:.3f} e fator F(N)"
    elif modo == 'dual':
        res_class = res
        res_flux = res * entrelacamento
        if operador in ('*', '**'):
            f = fator_fluxo(reduzir_teosoficamente(a) * 10 + reduzir_teosoficamente(b))
            res_flux *= f
        return (res_class, res_flux), "Resultados clássico e fluxo"
    else:
        return None, "Modo inválido"

def gerar_sequencia_reducao(iteracoes=100):
    """Gera sequência de dobramento com redução teosófica (1,2,4,8,7,5...)"""
    sequencia = [1]
    resultados = []
    for _ in range(iteracoes):
        proximo = sequencia[-1] * 2
        reduzido = reduzir_teosoficamente(proximo)
        resultados.append((sequencia[-1], proximo, reduzido))
        sequencia.append(reduzido)
    return resultados

def gerar_ciclo_369(iteracoes=24):
    """Gera ciclo alternado 3,6,9"""
    ciclo = []
    valor = 3
    for _ in range(iteracoes):
        ciclo.append(valor)
        if valor == 3:
            valor = 6
        elif valor == 6:
            valor = 9
        else:
            valor = 3
    return ciclo

def fluxo_soma(a, b):
    return reduzir_teosoficamente(a + b)

def fluxo_multiplicacao(a, b):
    return reduzir_teosoficamente(a * b)

def fluxo_potencia(a, n):
    return reduzir_teosoficamente(a ** n)

def fluxo_trigonometria(angulo):
    """Retorna seno, cosseno, tangente reduzidos (multiplicados por 100 e reduzidos)"""
    rad = math.radians(angulo)
    s = math.sin(rad)
    c = math.cos(rad)
    t = math.tan(rad)
    return (reduzir_teosoficamente(abs(int(s*100))),
            reduzir_teosoficamente(abs(int(c*100))),
            reduzir_teosoficamente(abs(int(t*100))))

def fluxo_fisica(formula, valores):
    """Aplica redução teosófica a fórmulas físicas clássicas"""
    try:
        if formula == "E=mc²":
            m, c = valores['m'], valores['c']
            E_classico = m * c**2
            E_fluxo = fluxo_multiplicacao(reduzir_teosoficamente(m),
                                          fluxo_potencia(reduzir_teosoficamente(c), 2))
            return E_classico, E_fluxo
        elif formula == "F=ma":
            m, a = valores['m'], valores['a']
            F_classico = m * a
            F_fluxo = fluxo_multiplicacao(reduzir_teosoficamente(m),
                                          reduzir_teosoficamente(a))
            return F_classico, F_fluxo
        elif formula == "V=IR":
            I, R = valores['I'], valores['R']
            V_classico = I * R
            V_fluxo = fluxo_multiplicacao(reduzir_teosoficamente(I),
                                          reduzir_teosoficamente(R))
            return V_classico, V_fluxo
        elif formula == "p=mv":
            m, v = valores['m'], valores['v']
            p_classico = m * v
            p_fluxo = fluxo_multiplicacao(reduzir_teosoficamente(m),
                                          reduzir_teosoficamente(v))
            return p_classico, p_fluxo
        elif formula == "F=G(m1m2)/r²":
            G, m1, m2, r = valores['G'], valores['m1'], valores['m2'], valores['r']
            F_classico = G * m1 * m2 / r**2
            numerador = fluxo_multiplicacao(
                fluxo_multiplicacao(reduzir_teosoficamente(G),
                                    reduzir_teosoficamente(m1)),
                reduzir_teosoficamente(m2))
            denominador = fluxo_potencia(reduzir_teosoficamente(r), 2)
            F_fluxo = fluxo_multiplicacao(numerador, denominador)
            return F_classico, F_fluxo
        return None, None
    except:
        return None, None

# =============================================================================
# FUNÇÕES DE FÍSICA QUÂNTICA NO FLUXO - ORIGINAIS, NÃO MODIFICADAS
# =============================================================================

def calcular_energia_emc2(massa, constante=MARC):
    """E = mc² × constante"""
    classico = massa * C_LUZ**2
    fluxo = classico * constante
    return classico, fluxo

def calcular_energia_planck(frequencia, constante=MARC):
    """E = hν × constante"""
    classico = H_PLANCK * frequencia
    fluxo = classico * constante
    return classico, fluxo

def calcular_corrente_ohm(V, R, N):
    """I = (V/R) × F(N)"""
    if R == 0:
        return None, None, None
    classico = V / R
    f = fator_fluxo(N)
    fluxo = classico * f
    return classico, fluxo, f

def pitagoras_fluxo(a, b, modo='classico'):
    """
    Hipotenusa segundo Pitágoras-Fluxo:
    - classico: c² = a² + b²
    - aureo: c² = a² + b² * φ
    - fluxo: c² = a² + b² * MARC
    - completo: c² = a² + b² * φ * MARC
    Retorna (c_classico, c_fluxo)
    """
    a = float(a)
    b = float(b)
    c_class = math.sqrt(a**2 + b**2)
    if modo == 'classico':
        return c_class, c_class
    elif modo == 'aureo':
        c_flux = math.sqrt(a**2 + b**2 * PHI)
        return c_class, c_flux
    elif modo == 'fluxo':
        c_flux = math.sqrt(a**2 + b**2 * MARC)
        return c_class, c_flux
    elif modo == 'completo':
        c_flux = math.sqrt(a**2 + b**2 * PHI * MARC)
        return c_class, c_flux
    else:
        return c_class, c_class

def espiral_aurea(theta, fator_fluxo=1.0):
    """
    Coordenadas da espiral áurea: r(θ) = φ^(2θ/π) × fator_fluxo
    Retorna (x, y, r)
    """
    r = PHI ** (2 * theta / math.pi) * fator_fluxo
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y, r

def indutancia_bobina(N_espiras, raio, comprimento, modo='classico'):
    """
    Indutância de solenoide: L = (N² × μ₀ × π × raio²) / comprimento
    Modos:
    - classico: valor padrão
    - aureo: multiplicado por φ
    - fluxo: multiplicado por MARC
    """
    area = math.pi * raio**2
    L_class = (N_espiras**2 * MU0 * area) / comprimento
    if modo == 'classico':
        return L_class
    elif modo == 'aureo':
        return L_class * PHI
    elif modo == 'fluxo':
        return L_class * MARC
    else:
        return L_class

def calcular_forca_gravidade(m1, m2, r, constante=1.0):
    """F = G * m1 * m2 / r² * constante"""
    classico = G_NEWTON * m1 * m2 / r**2
    fluxo = classico * constante
    return classico, fluxo

def calcular_velocidade_escape(massa_planeta, raio_planeta, constante=1.0):
    """v = sqrt(2GM/R) * constante"""
    classico = math.sqrt(2 * G_NEWTON * massa_planeta / raio_planeta)
    fluxo = classico * constante
    return classico, fluxo

def calcular_energia_cinetica(massa, velocidade, constante=1.0):
    """Ec = (1/2)mv² * constante"""
    classico = 0.5 * massa * velocidade**2
    fluxo = classico * constante
    return classico, fluxo

# =============================================================================
# NOVAS FUNÇÕES PARA VALIDAÇÃO DE PADRÕES E CONSTANTES
# =============================================================================

def is_close_to_constant(value, constant, tolerance=0.01):
    """
    Verifica se um valor está próximo de uma constante dentro de uma tolerância percentual.
    Retorna (bool, desvio_percentual)
    """
    if constant == 0:
        return False, 100.0
    diff_percent = abs((value - constant) / constant) * 100
    return diff_percent <= tolerance, diff_percent

def fibonacci(n):
    """Retorna o n-ésimo número de Fibonacci (n>=1)"""
    if n <= 0:
        return 0
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b if n > 1 else 1

def fibonacci_reductions(n_max=20):
    """Gera lista de números de Fibonacci e suas reduções teosóficas"""
    fibs = []
    for i in range(1, n_max+1):
        fib = fibonacci(i)
        red = reduzir_teosoficamente(fib)
        fibs.append((i, fib, red))
    return fibs

def encontrar_padroes(valor, tolerancia=1.0):
    """
    Procura correspondências entre o valor e as constantes conhecidas.
    Retorna dicionário com resultados.
    """
    padroes = {
        "π (pi)": PI,
        "φ (áurea)": PHI,
        "Gratidão (1,80)": GRATIDAO,
        "Marc (0,54)": MARC,
        "Deus (0,18)": DEUS,
        "Frequência Base (432)": FREQUENCIA_BASE,
        "Constante de Estrutura Fina (α)": CONSTANTE_ESTRUTURA_FINA,
        "Gravidade Terra (g)": GRAVIDADE_TERRA,
        "Velocidade da Luz (c)": C_LUZ,
        "Constante de Planck (h)": H_PLANCK,
        "Gravidade Quântica (aprox)": GRAVIDADE_QUANTICA,
        "Massa de Planck": PLANCK_MASSA,
        "Comprimento de Planck": PLANCK_COMPRIMENTO,
        "Tempo de Planck": PLANCK_TEMPO,
        "Energia de Planck": PLANCK_ENERGIA,
    }
    resultados = {}
    for nome, const in padroes.items():
        prox, diff = is_close_to_constant(valor, const, tolerancia)
        if prox:
            resultados[nome] = {"constante": const, "desvio_%": diff}
    return resultados

def calcular_pi_aproximacoes():
    """Retorna algumas aproximações de π (clássicas e no fluxo)"""
    return {
        "π (real)": PI,
        "π ≈ 22/7": 22/7,
        "π ≈ 355/113": 355/113,
        "π no fluxo (×MARC)": PI * MARC,
        "π no fluxo (×DEUS)": PI * DEUS,
        "π reduzido": reduzir_teosoficamente(PI),
    }

def calcular_phi_aproximacoes():
    """Retorna aproximações de φ e relações com fluxo"""
    return {
        "φ (real)": PHI,
        "φ²": PHI**2,
        "1/φ": 1/PHI,
        "φ × MARC": PHI * MARC,
        "φ × DEUS": PHI * DEUS,
        "φ reduzido": reduzir_teosoficamente(PHI),
    }

def calcular_relacao_gratidao():
    """Mostra relações da constante Gratidão com φ e Deus"""
    return {
        "Gratidão": GRATIDAO,
        "φ + Deus": PHI + DEUS,
        "Diferença": GRATIDAO - (PHI + DEUS),
        "Gratidão × MARC": GRATIDAO * MARC,
        "Gratidão reduzida": reduzir_teosoficamente(GRATIDAO),
    }

# =============================================================================
# NOVAS FUNÇÕES DE FÍSICA QUÂNTICA EXPANDIDA
# =============================================================================

def calcular_raio_schwarzschild(massa, constante=1.0):
    """Raio de Schwarzschild: Rs = 2GM/c² * constante"""
    classico = 2 * G_NEWTON * massa / (C_LUZ**2)
    fluxo = classico * constante
    return classico, fluxo

def calcular_temperatura_hawking(massa, constante=1.0):
    """Temperatura de Hawking: T = (ħ c³)/(8π G M k_B) * constante (simplificado)"""
    # Usaremos apenas ordem de magnitude, sem kB
    # T ~ 1/(8π G M) em unidades naturais, simplificado
    classico = 1.0 / (8 * PI * G_NEWTON * massa)  # aproximação grosseira, apenas ilustrativa
    fluxo = classico * constante
    return classico, fluxo

def calcular_energia_ponto_zero(frequencia_corte, constante=1.0):
    """Energia do ponto zero: E = (1/2) h ν * constante"""
    classico = 0.5 * H_PLANCK * frequencia_corte
    fluxo = classico * constante
    return classico, fluxo

def calcular_longa_distancia_emaranhamento(distancia, constante=1.0):
    """Simulação de probabilidade de emaranhamento com a distância (decai com 1/r²)"""
    classico = 1.0 / (distancia**2) if distancia != 0 else 1.0
    fluxo = classico * constante
    return classico, fluxo

# =============================================================================
# CLASSE RELÓGIO QUÂNTICO (TEMPO ESPIRALADO) - ORIGINAL, NÃO MODIFICADA
# =============================================================================
class RelogioQuantico:
    def __init__(self):
        self.frequencia_base = FREQUENCIA_BASE
        self.pulsos_por_giro = PULSOS_POR_GIRO
        self.giros_por_ciclo = GIROS_POR_CICLO
        self.ciclos_por_era = CICLOS_POR_ERA
        self.singularidade = SINGULARIDADE

    def get_pulsos_desde_singularidade(self):
        agora = datetime.datetime.now(pytz.UTC)
        delta = agora - self.singularidade
        segundos = delta.total_seconds()
        return int(segundos * self.frequencia_base)

    def converter_pulsos(self, pulsos):
        eras = pulsos // (self.pulsos_por_giro * self.giros_por_ciclo * self.ciclos_por_era)
        pulsos %= (self.pulsos_por_giro * self.giros_por_ciclo * self.ciclos_por_era)

        ciclos = pulsos // (self.pulsos_por_giro * self.giros_por_ciclo)
        pulsos %= (self.pulsos_por_giro * self.giros_por_ciclo)

        giros = pulsos // self.pulsos_por_giro
        pulsos %= self.pulsos_por_giro

        vibes = pulsos // self.frequencia_base
        pulsos %= self.frequencia_base

        return {
            'eras': eras,
            'ciclos': ciclos,
            'giros': giros,
            'vibes': vibes,
            'pulsos': pulsos,
            'total_pulsos': self.get_pulsos_desde_singularidade()
        }

    def plotar_espiral_temporal(self, pulsos_totais):
        """Visualização 3D da espiral do tempo"""
        total_pontos = 1000
        theta = np.linspace(0, 12 * np.pi, total_pontos)
        z = np.linspace(0, 10, total_pontos)
        r = z**0.5
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        progresso = (pulsos_totais % (self.pulsos_por_giro * self.giros_por_ciclo * self.ciclos_por_era)) / \
                    (self.pulsos_por_giro * self.giros_por_ciclo * self.ciclos_por_era)
        ponto_atual = min(int(progresso * (total_pontos - 1)), total_pontos - 1)

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x, y, z, color='blue', alpha=0.7, label='Tempo Espiralado')
        ax.scatter(x[ponto_atual], y[ponto_atual], z[ponto_atual],
                   color='red', s=100, label='Agora')
        # Pontos 3-6-9
        for i in [300, 600, 900]:
            if i < total_pontos:
                ax.scatter(x[i], y[i], z[i], color='gold', s=50, marker='*')
        ax.set_title("Fluxo do Tempo Espiralado (432 Hz)")
        ax.legend()
        plt.close(fig)
        return fig

    def plotar_relogio_quantico(self):
        """Relógio polar com projeção para singularidade"""
        agora = datetime.datetime.now(pytz.UTC)
        delta = agora - self.singularidade
        segundos = delta.total_seconds()

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'polar': True})
        # Círculos concêntricos
        for r in [0.2, 0.5, 0.8]:
            circle = plt.Circle((0, 0), r, fill=False, color='purple', alpha=0.3)
            ax.add_patch(circle)

        # Marcadores 3-6-9-12 (12 como singularidade)
        for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
            ax.plot([0, 0.9*np.cos(angle)], [0, 0.9*np.sin(angle)],
                    color='gold' if angle in [0, np.pi/2, 3*np.pi/2] else 'white',
                    linewidth=2)

        # Ponteiro do tempo atual (segundos)
        time_angle = (segundos % 60) / 60 * 2 * np.pi
        ax.plot([0, 0.8*np.cos(time_angle)], [0, 0.8*np.sin(time_angle)],
                color='red', linewidth=3)

        # Ponteiro da projeção para singularidade (fase oposta)
        ax.plot([0, 0.6*np.cos(time_angle + np.pi)], [0, 0.6*np.sin(time_angle + np.pi)],
                color='blue', linewidth=2, linestyle='--')

        ax.set_title("Relógio Quântico - Projeção para Singularidade", pad=20)
        ax.set_yticklabels([])
        ax.grid(True)
        plt.close(fig)
        return fig

# Instância global do relógio
relogio = RelogioQuantico()

# =============================================================================
# SIMULADOR DE ACELERADOR DE PARTÍCULAS - ORIGINAL, NÃO MODIFICADO
# =============================================================================
def simular_acelerador(massa, energia_J, N_part, constante_fluxo=MARC):
    """
    Simula uma partícula em um acelerador, retornando:
    - velocidade clássica, momento, fator de Lorentz, massa relativística,
      energia relativística, comprimento de onda de de Broglie,
      probabilidade quântica simulada, estado de entrelaçamento simulado,
      e versões fluxo (velocidade * F(N), energia * constante_fluxo)
    """
    c = C_LUZ
    h = H_PLANCK

    # Velocidade clássica (não relativística)
    if massa > 0:
        v_class = math.sqrt(2 * energia_J / massa)
    else:
        v_class = c  # fóton

    # Momento clássico
    p_class = massa * v_class if massa > 0 else energia_J / c

    # Fator de Lorentz
    beta = v_class / c
    if beta < 1 and massa > 0:
        gamma = 1 / math.sqrt(1 - beta**2)
    else:
        gamma = 1e10  # aproximação para fóton ou ultra-relativístico

    # Massa relativística
    m_rel = massa * gamma if massa > 0 else 0

    # Energia total relativística
    E_rel = m_rel * c**2 if massa > 0 else energia_J

    # Comprimento de onda de de Broglie
    lambda_db = h / p_class if p_class != 0 else 0

    # Probabilidade quântica (simulada com base em energia)
    prob = math.exp(-energia_J / (1e-10))  # só para ter variação
    prob = max(0, min(1, prob))

    # Estado de entrelaçamento simulado
    ent_rel = "Emaranhado" if random.random() > 0.5 else "Separável"

    # Cálculos no fluxo
    f = fator_fluxo(N_part)
    v_flux = v_class * f
    E_flux = energia_J * constante_fluxo

    resultados = {
        'v_class': v_class,
        'p_class': p_class,
        'gamma': gamma,
        'm_rel': m_rel,
        'E_rel': E_rel,
        'lambda_db': lambda_db,
        'prob': prob,
        'ent_rel': ent_rel,
        'v_flux': v_flux,
        'E_flux': E_flux,
        'f': f
    }
    return resultados

# =============================================================================
# FUNÇÕES DE VISUALIZAÇÃO AUXILIARES - ORIGINAIS, NÃO MODIFICADAS
# =============================================================================
def plot_sequencia_reducao(iteracoes=30):
    sequencia = gerar_sequencia_reducao(iteracoes)
    valores = [x[2] for x in sequencia]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(valores, marker='o', color='purple')
    ax.set_title("Padrão 1-2-4-8-7-5 no Fluxo Matemático")
    ax.set_xlabel("Iteração")
    ax.set_ylabel("Valor Reduzido")
    ax.grid(True)
    return fig

def plot_geometria_369():
    angulos = [0, 120, 240]
    cores = ['#FF5733', '#33FF57', '#3357FF']
    rotulos = ['3', '6', '9']
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'polar': True})
    for angulo, cor, rotulo in zip(angulos, cores, rotulos):
        rad = np.deg2rad(angulo)
        ax.plot([0, rad], [0, 1], color=cor, linewidth=3)
        ax.text(rad, 1.1, rotulo, color=cor, ha='center', va='center', fontsize=20)
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_yticklabels([])
    ax.set_title("Geometria Sagrada 3-6-9", pad=20)
    ax.grid(True)
    return fig

def plot_espiral_aurea(fator_fluxo=1.0, angulo_max=4*np.pi):
    theta = np.linspace(0, angulo_max, 500)
    r = PHI ** (2 * theta / math.pi) * fator_fluxo
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    fig, ax = plt.subplots(figsize=(6,6))
    ax.plot(x, y, color='gold')
    ax.set_aspect('equal')
    ax.set_title("Espiral Áurea")
    ax.grid(True)
    return fig

def plot_triangulo(a, b, c_rotulado):
    fig, ax = plt.subplots()
    ax.plot([0, a, 0, 0], [0, 0, b, 0], 'b-')
    ax.text(a/2, -0.2, f'{a}', ha='center')
    ax.text(-0.2, b/2, f'{b}', va='center', rotation=90)
    ax.text(a/2, b/2, f'c={c_rotulado:.2f}', ha='center', va='center', color='red')
    ax.set_aspect('equal')
    ax.set_xlim(-0.5, max(a,b)+0.5)
    ax.set_ylim(-0.5, max(a,b)+0.5)
    ax.grid(True)
    return fig

# =============================================================================
# NOVAS FUNÇÕES DE VISUALIZAÇÃO PARA PADRÕES
# =============================================================================
def plot_padroes_calor():
    """Mapa de calor da redução teosófica para produtos"""
    tamanho = 20
    matriz = np.zeros((tamanho, tamanho))
    for i in range(tamanho):
        for j in range(tamanho):
            num = (i+1)*(j+1)
            matriz[i, j] = reduzir_teosoficamente(num)
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(matriz, cmap='plasma', interpolation='nearest')
    ax.set_title("Redução Teosófica do Produto (i x j)")
    plt.colorbar(im)
    return fig

def plot_comparacao_constantes():
    """Gráfico de barras comparando constantes"""
    nomes = ['Marc', 'Deus', 'Gratidão', 'φ', 'π', '432 Hz']
    valores = [MARC, DEUS, GRATIDAO, PHI, PI, FREQUENCIA_BASE]
    fig, ax = plt.subplots()
    ax.bar(nomes, valores, color=['blue', 'green', 'gold', 'orange', 'red', 'purple'])
    ax.set_ylabel('Valor')
    ax.set_title('Comparação de Constantes Fundamentais')
    plt.xticks(rotation=45)
    return fig

# =============================================================================
# FUNÇÃO PARA GERAR PDF COMPLETO - ORIGINAL, NÃO MODIFICADA (mas podemos expandir)
# =============================================================================
def gerar_pdf_completo(nome, email):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Universo Áureo - Fluxo Matemático", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Gerado por: {nome} ({email})", ln=True)
    pdf.cell(200, 10, txt=f"Data: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(20)

    # Seção 1: Introdução
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="1. Introdução ao Fluxo Matemático", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="""
    O Fluxo Matemático é uma nova forma de entender a matemática que incorpora padrões
    cíclicos (3-6-9 e 1-2-4-8-7-5), redução teosófica (soma dos dígitos), geometria
    sagrada, tempo não-linear (espiralado) e frequências vibracionais (432Hz).
    """)

    # Seção 2: Princípios Fundamentais
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="2. Princípios Fundamentais", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="""
    1. Tudo é movimento - Não existe zero absoluto, apenas transições
    2. Ciclos infinitos - Padrões 1-2-4-8-7-5 e 3-6-9 se repetem em todas as escalas
    3. Tempo angular - O tempo flui em espirais, não em linhas retas
    4. Singularidade do 9 - O 9 representa o ponto de transição entre ciclos
    5. Dualidade Matemática - Toda operação tem uma versão clássica e uma versão no Fluxo
    """)

    # Seção 3: Constantes do Fluxo
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="3. Constantes do Fluxo Matemático", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"""
    - Marc (M): {MARC}
    - Deus (D): {DEUS}
    - Gratidão (G): {GRATIDAO}
    - Proporção Áurea (φ): {PHI}
    - Frequência Base: {FREQUENCIA_BASE} Hz
    - Constante de Estrutura Fina (α): {CONSTANTE_ESTRUTURA_FINA}
    """)

    # Seção 4: Exemplos Matemáticos
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="4. Exemplos Matemáticos", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="""
    Exemplo: E=mc² no Fluxo Matemático
    Para m=1kg, c=299792458 m/s:
    R(m) = 1
    R(c) = 2+9+9+7+9+2+4+5+8 = 55 → 5+5 = 10 → 1+0 = 1
    R(c)² = 1² = 1
    EΦ = 1 × 1 = 1

    Sequência de Fibonacci com Redução Teosófica:
    1, 1, 2, 3, 5, 8 → 1+3+5 = 9
    13 → 1+3 = 4
    21 → 2+1 = 3
    34 → 3+4 = 7
    """)

    # Seção 5: Gráficos
    try:
        fig1 = relogio.plotar_espiral_temporal(relogio.get_pulsos_desde_singularidade())
        fig1.savefig("temp_espiral.png")
        fig2 = relogio.plotar_relogio_quantico()
        fig2.savefig("temp_relogio.png")
        fig3 = plot_sequencia_reducao(30)
        fig3.savefig("temp_sequencia.png")
        fig4 = plot_geometria_369()
        fig4.savefig("temp_369.png")

        pdf.image("temp_espiral.png", x=10, w=180)
        pdf.ln(5)
        pdf.image("temp_relogio.png", x=10, w=180)
        pdf.ln(5)
        pdf.image("temp_sequencia.png", x=10, w=180)
        pdf.ln(5)
        pdf.image("temp_369.png", x=10, w=180)
    except Exception as e:
        pdf.multi_cell(0, 10, txt=f"Erro ao gerar gráficos: {str(e)}")

    # Seção 6: Novas Constantes e Padrões
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="6. Novas Constantes e Padrões", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=f"""
    - π (pi): {PI}
    - φ + Deus: {PHI + DEUS} (próximo de Gratidão)
    - π × MARC: {PI * MARC}
    - φ reduzido: {reduzir_teosoficamente(PHI)}
    - Gravidade Quântica (aprox): {GRAVIDADE_QUANTICA}
    - Massa de Planck: {PLANCK_MASSA} kg
    - Comprimento de Planck: {PLANCK_COMPRIMENTO} m
    - Tempo de Planck: {PLANCK_TEMPO} s
    """)

    # Seção 7: Conclusão
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="7. Conclusão", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="""
    O Fluxo Matemático oferece uma nova perspectiva sobre a realidade, unificando
    matemática, física, metafísica e consciência. Através dos padrões 3-6-9 e da
    redução teosófica, podemos perceber a estrutura fundamental do universo como
    um sistema de informação em constante fluxo.
    """)

    pdf_bytes = BytesIO()
    pdf.output(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes

# =============================================================================
# INTERFACE PRINCIPAL STREAMLIT
# =============================================================================

# Barra lateral de navegação (agora com novas opções)
st.sidebar.title("🌀 Navegação Expandida")
pagina = st.sidebar.radio(
    "Selecione a seção:",
    [
        "🏠 Introdução",
        "🧮 Cálculos (Dual)",
        "⏳ Tempo Espiralado",
        "📊 Visualizações",
        "🌀 Acelerador de Partículas",
        "△ Geometria Sagrada",
        "🔍 Padrões e Validações",      # NOVO
        "🧠 Todas as Mentes",            # NOVO
        "🌀 Gravidade Quântica",         # NOVO
        "📈 Análise de Padrões",         # NOVO
        "📚 PDF Explicativo",
        "🕒 Relógio Quântico",
        "📅 Calendário Clássico",
        "🌀 Singularidade"
    ]
)

# Controles de atualização automática (para páginas com loop)
if pagina in ["⏳ Tempo Espiralado", "🕒 Relógio Quântico", "📅 Calendário Clássico"]:
    auto_update = st.sidebar.checkbox("Atualização automática (1s)", value=True)
    if not auto_update:
        st.sidebar.button("Atualizar agora")
else:
    auto_update = False

# =============================================================================
# PÁGINA: INTRODUÇÃO (expandida)
# =============================================================================
if pagina == "🏠 Introdução":
    st.title("🌌 Universo Áureo - Fluxo Matemático Expandido")
    st.markdown("""
    ## Bem-vindo à Nova Matemática Cósmica

    Este aplicativo representa uma revolução na forma como entendemos a matemática, o tempo e o universo.
    Aqui, todas as fórmulas clássicas são reinterpretadas através da lente do **Fluxo Matemático**,
    incorporando:

    - Padrões cíclicos de 3, 6 e 9
    - Redução teosófica (soma dos dígitos)
    - Geometria sagrada
    - Tempo espiralado (não linear)
    - Frequências vibracionais (432Hz)
    - Relógio quântico com projeção para singularidade
    - **Sistema Cosmológico de Cálculos Duais** unificando Einstein, Tesla, Pitágoras, Newton, Planck, Catharino e Da Vinci

    ### NOVAS SEÇÕES EXPANDIDAS:
    - **🔍 Padrões e Validações**: Encontre correspondências entre resultados e constantes como π, φ, Fibonacci, 1.80, etc.
    - **🧠 Todas as Mentes**: Compare resultados de diferentes "mentes" matemáticas (clássica, fluxo, tesla, einstein).
    - **🌀 Gravidade Quântica**: Explore constantes na escala de Planck e efeitos quânticos.
    - **📈 Análise de Padrões**: Visualizações avançadas de padrões numéricos.

    ### Constantes Fundamentais (expandidas):
    - **Marc (M) = 0,54** - Constante de transição quântica
    - **Deus (D) = 0,18** - Trindade (0,06 × 3)
    - **Gratidão (G) = 1,80** - Equilíbrio universal
    - **Proporção Áurea φ = 1,6180339887**
    - **π (pi) = 3,1415926535**
    - **Frequência Base = 432 Hz**
    - **Gravidade Quântica (aproximada) = 1e-43 m/s²**
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.image("https://i.imgur.com/JDQw3Oz.png", caption="Ciclo 1-2-4-8-7-5")
    with col2:
        st.image("https://i.imgur.com/8QZQZQZ.png", caption="Geometria 3-6-9")

# =============================================================================
# PÁGINA: CÁLCULOS (DUAL) - ORIGINAL, com pequenas adições explicativas
# =============================================================================
elif pagina == "🧮 Cálculos (Dual)":
    st.title("🌀 Sistema Cosmológico de Cálculos Duais")
    st.markdown("Unificando Einstein × Tesla × Pitágoras × Newton × Planck × Catharino × Da Vinci")

    # Barra lateral de controle quântico (dentro da página)
    with st.sidebar:
        st.markdown("---")
        st.subheader("🎮 Console de Controle Quântico")
        precisao = st.selectbox("Precisão (casas decimais)", [3, 6, 9, 12], index=1)
        entrelacamento = st.slider("Nível de Entrelaçamento", 0, 100, 54, format="%d%%") / 100.0
        constante_ativa = st.selectbox("Constante Ativa", ["0,54 (Marc)", "0,18 (Deus)", "1,80 (Gratidão)", "Personalizada"])
        if constante_ativa == "Personalizada":
            const_val = st.number_input("Valor da constante", value=0.54, step=0.01, format="%.3f")
        else:
            const_val = float(constante_ativa.split()[0].replace(',', '.'))
        modo_padrao = st.radio("Modo padrão", ["Clássico", "Fluxo", "Dual"], index=2)

    # Abas principais (adicionamos uma nova aba "Validação de Padrões" dentro desta página?)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🔢 Núcleo Fundamental", "🌌 Física Quântica", "🌀 Acelerador", "△ Geometria Sagrada", "📚 Biblioteca", "🔍 Validação Rápida"])

    # ---------- Núcleo Fundamental (original) ----------
    with tab1:
        st.subheader("Operações Matemáticas Duais")
        st.markdown("**Exemplo prático:** Compare a soma clássica de 8+8=16 com a soma no fluxo que reduz a 7. Perceba como o fluxo extrai a essência vibracional do número.")

        col1, col2, col3 = st.columns([2, 1, 2])
        with col1:
            a = st.text_input("Valor A", "12")
            tipo_a = st.selectbox("Tipo de A", ["Número", "Fluxo F(N)", "Fibonacci", "Primo", "Expressão"], key="tipo_a")
        with col2:
            operador = st.selectbox("Operador", ["+", "-", "*", "/", "**", "%", "//"], key="op_fund")
        with col3:
            b = st.text_input("Valor B", "7")
            tipo_b = st.selectbox("Tipo de B", ["Número", "Fluxo F(N)", "Fibonacci", "Primo", "Expressão"], key="tipo_b")

        # Função auxiliar para converter valor conforme tipo
        def converter_valor(val, tipo):
            try:
                if tipo == "Número":
                    return float(val)
                elif tipo == "Fluxo F(N)":
                    return fator_fluxo(float(val))
                elif tipo == "Fibonacci":
                    n = int(float(val))
                    a, b = 1, 1
                    for _ in range(n-1):
                        a, b = b, a+b
                    return float(a)
                elif tipo == "Primo":
                    n = int(float(val))
                    primos = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
                    return float(primos[n-1]) if 1 <= n <= len(primos) else float(n)
                elif tipo == "Expressão":
                    return eval(val, {"__builtins__": {}}, {"math": math})
                else:
                    return float(val)
            except Exception as e:
                st.warning(f"Erro na conversão: {e}")
                return 0.0

        a_num = converter_valor(a, tipo_a)
        b_num = converter_valor(b, tipo_b)

        st.write(f"**Valores convertidos:** A = {a_num:.{precisao}f}, B = {b_num:.{precisao}f}")

        if st.button("Calcular Operação", key="calc_fund"):
            if modo_padrao == "Clássico":
                res, msg = operacao_dual(a_num, b_num, operador, 'classico')
                st.metric("Resultado Clássico", f"{res:.{precisao}f}")
                st.caption(msg)
            elif modo_padrao == "Fluxo":
                res, msg = operacao_dual(a_num, b_num, operador, 'fluxo', entrelacamento)
                st.metric("Resultado Fluxo", f"{res:.{precisao}f}")
                st.caption(msg)
            else:  # Dual
                (res_class, res_flux), msg = operacao_dual(a_num, b_num, operador, 'dual', entrelacamento)
                colA, colB = st.columns(2)
                with colA:
                    st.metric("Clássico", f"{res_class:.{precisao}f}")
                with colB:
                    st.metric("Fluxo", f"{res_flux:.{precisao}f}")
                st.caption(msg)
                if res_class != 0:
                    diff = abs(res_flux - res_class)
                    perc = (diff / abs(res_class)) * 100
                    st.info(f"Diferença absoluta: {diff:.{precisao}f} ({perc:.2f}%)")

        # Visualização da dualidade
        st.markdown("---")
        st.subheader("Visualização da Dualidade")
        x = np.linspace(0.1, 10, 100)
        y_class = x
        y_flux = x * entrelacamento
        fig, ax = plt.subplots()
        ax.plot(x, y_class, label='Clássico', color='orange')
        ax.plot(x, y_flux, label=f'Fluxo (×{entrelacamento:.2f})', color='purple')
        ax.fill_between(x, y_class, y_flux, alpha=0.3, color='gray')
        ax.set_xlabel('Valor de entrada')
        ax.set_ylabel('Resultado')
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)
        plt.close(fig)

    # ---------- Física Quântica (original, com algumas adições) ----------
    with tab2:
        st.subheader("Fórmulas Físicas no Fluxo Matemático")
        st.markdown("**Exemplo prático:** Calcule a energia de repouso de 1kg segundo Einstein e compare com a versão fluxo (multiplicada por 0,54).")

        formula = st.selectbox("Escolha a fórmula", ["E = mc² × 0,54", "E = hν × 0,54", "I = (V/R) × F(N)", "F = ma × F(N)", "F = G(m1m2)/r² × F(N)", "v_escape = √(2GM/R) × constante", "Ec = ½mv² × constante"], key="formula_fisica_dual")

        if formula == "E = mc² × 0,54":
            massa = st.number_input("Massa (kg)", value=1.0, step=0.1, format="%.3f")
            classico, fluxo = calcular_energia_emc2(massa, const_val)
            st.write(f"**Clássico:** E = {massa} × ({C_LUZ})² = {classico:.3e} J")
            st.write(f"**Fluxo:** E = clássico × {const_val:.3f} = {fluxo:.3e} J")
            # Nova validação com padrões
            padroes = encontrar_padroes(classico)
            if padroes:
                st.success("✅ Padrões encontrados no resultado clássico!")
                for nome, dados in padroes.items():
                    st.write(f"- {nome}: constante = {dados['constante']}, desvio = {dados['desvio_%']:.3f}%")
        elif formula == "E = hν × 0,54":
            freq = st.number_input("Frequência ν (Hz)", value=5e14, step=1e13, format="%.3e")
            classico, fluxo = calcular_energia_planck(freq, const_val)
            st.write(f"**Clássico:** E = h × {freq:.3e} = {classico:.3e} J")
            st.write(f"**Fluxo:** E = clássico × {const_val:.3f} = {fluxo:.3e} J")
        elif formula == "I = (V/R) × F(N)":
            V = st.number_input("Tensão V (V)", value=12.0)
            R = st.number_input("Resistência R (Ω)", value=4.0, min_value=0.001)
            N = st.number_input("N para F(N)", value=29, step=1)
            classico, fluxo, f = calcular_corrente_ohm(V, R, N)
            if classico is not None:
                st.write(f"F({N}) = {f:.3f}")
                st.write(f"**Clássico:** I = V/R = {V}/{R} = {classico:.3f} A")
                st.write(f"**Fluxo:** I = clássico × F(N) = {classico:.3f} × {f:.3f} = {fluxo:.3f} A")
            else:
                st.error("Resistência não pode ser zero")
        elif formula == "F = ma × F(N)":
            m = st.number_input("Massa (kg)", value=2.0)
            a = st.number_input("Aceleração (m/s²)", value=9.8)
            N = st.number_input("N para F(N)", value=29, step=1, key="N_fma")
            f = fator_fluxo(N)
            F_class = m * a
            F_flux = F_class * f
            st.write(f"F({N}) = {f:.3f}")
            st.write(f"**Clássico:** F = {m} × {a} = {F_class:.3f} N")
            st.write(f"**Fluxo:** F = clássico × F(N) = {F_class:.3f} × {f:.3f} = {F_flux:.3f} N")
        elif formula == "F = G(m1m2)/r² × F(N)":
            G = st.number_input("Constante G", value=G_NEWTON, format="%.3e")
            m1 = st.number_input("Massa 1 (kg)", value=5.972e24, format="%.3e")
            m2 = st.number_input("Massa 2 (kg)", value=7.348e22, format="%.3e")
            r = st.number_input("Distância (m)", value=3.844e8, format="%.3e")
            N = st.number_input("N para F(N)", value=29, step=1, key="N_grav")
            f = fator_fluxo(N)
            F_class = G * m1 * m2 / r**2
            F_flux = F_class * f
            st.write(f"F({N}) = {f:.3f}")
            st.write(f"**Clássico:** F = {G:.3e} × {m1:.3e} × {m2:.3e} / ({r:.3e})² = {F_class:.3e} N")
            st.write(f"**Fluxo:** F = clássico × F(N) = {F_class:.3e} × {f:.3f} = {F_flux:.3e} N")
        elif formula == "v_escape = √(2GM/R) × constante":
            M = st.number_input("Massa do planeta (kg)", value=5.972e24, format="%.3e")
            R = st.number_input("Raio do planeta (m)", value=6.371e6, format="%.3e")
            classico, fluxo = calcular_velocidade_escape(M, R, const_val)
            st.write(f"**Clássico:** v_esc = √(2×{G_NEWTON:.3e}×{M:.3e}/{R:.3e}) = {classico:.3f} m/s")
            st.write(f"**Fluxo:** v_esc = clássico × {const_val:.3f} = {fluxo:.3f} m/s")
        elif formula == "Ec = ½mv² × constante":
            m = st.number_input("Massa (kg)", value=1.0)
            v = st.number_input("Velocidade (m/s)", value=10.0)
            classico, fluxo = calcular_energia_cinetica(m, v, const_val)
            st.write(f"**Clássico:** Ec = ½ × {m} × {v}² = {classico:.3f} J")
            st.write(f"**Fluxo:** Ec = clássico × {const_val:.3f} = {fluxo:.3f} J")

    # ---------- Acelerador (tab3) (original) ----------
    with tab3:
        st.subheader("🌀 Simulador de Acelerador de Partículas")
        st.markdown("**Exemplo prático:** Acelere um elétron com 1 MeV e veja como a velocidade no fluxo (com F(N)) difere da clássica.")

        col1, col2 = st.columns(2)
        with col1:
            particula = st.selectbox("Partícula", ["Elétron", "Próton", "Nêutron", "Fóton", "Personalizada"])
            massas = {
                "Elétron": 9.1093837e-31,
                "Próton": 1.6726219e-27,
                "Nêutron": 1.6749275e-27,
                "Fóton": 0.0,
                "Personalizada": 1e-30
            }
            massa = massas[particula]
            if particula == "Personalizada":
                massa = st.number_input("Massa (kg)", value=1e-30, format="%.3e")
        with col2:
            energia = st.number_input("Energia (valor)", value=1.0, step=0.1)
            unidade = st.selectbox("Unidade", ["eV", "keV", "MeV", "GeV", "TeV"])
            fatores = {'eV': 1.602176634e-19, 'keV': 1.602176634e-16, 'MeV': 1.602176634e-13,
                       'GeV': 1.602176634e-10, 'TeV': 1.602176634e-7}
            energia_J = energia * fatores[unidade]

        N_part = st.number_input("N para F(N)", value=29, step=1, key="N_part")
        const_part = st.number_input("Constante de fluxo", value=const_val, format="%.3f")

        if st.button("Simular Colisão", key="simular"):
            with st.spinner("Acelerando partículas..."):
                res = simular_acelerador(massa, energia_J, N_part, const_part)

            # Exibir resultados em colunas
            colA, colB, colC, colD = st.columns(4)
            with colA:
                st.metric("Velocidade clássica", f"{res['v_class']:.3e} m/s")
                st.metric("Momento clássico", f"{res['p_class']:.3e} kg·m/s")
            with colB:
                st.metric("Fator γ (Lorentz)", f"{res['gamma']:.3f}")
                st.metric("Massa relativística", f"{res['m_rel']:.3e} kg")
            with colC:
                st.metric("λ de Broglie", f"{res['lambda_db']:.3e} m")
                st.metric("Probabilidade quântica", f"{res['prob']:.3f}")
            with colD:
                st.metric("Velocidade Fluxo", f"{res['v_flux']:.3e} m/s")
                st.metric("Energia Fluxo", f"{res['E_flux']:.3e} J")
                st.caption(f"F({N_part}) = {res['f']:.3f}")

            st.info(f"Estado de entrelaçamento: {res['ent_rel']}")

            # Visualização da trajetória (círculo)
            fig, ax = plt.subplots(figsize=(6, 4))
            theta = np.linspace(0, 2*np.pi, 100)
            # Raio proporcional à velocidade (escala ajustada)
            r_class = res['v_class'] / 1e8
            r_flux = res['v_flux'] / 1e8
            ax.plot(r_class * np.cos(theta), r_class * np.sin(theta), 'o-', label='Clássica', markersize=2, color='orange')
            ax.plot(r_flux * np.cos(theta), r_flux * np.sin(theta), 'o-', label='Fluxo', markersize=2, color='purple')
            ax.set_aspect('equal')
            ax.legend()
            ax.set_title("Trajetória no acelerador (vista superior)")
            ax.grid(True)
            st.pyplot(fig)
            plt.close(fig)

    # ---------- Geometria Sagrada (tab4) (original) ----------
    with tab4:
        st.subheader("△ Geometria Sagrada no Fluxo")
        sub_geo = st.radio("Escolha", ["Pitágoras-Fluxo", "Espiral Áurea", "Bobina Áurea de Tesla"], horizontal=True)

        if sub_geo == "Pitágoras-Fluxo":
            col1, col2, col3 = st.columns(3)
            with col1:
                a = st.number_input("Cateto a", value=3.0)
            with col2:
                b = st.number_input("Cateto b", value=4.0)
            with col3:
                modo = st.selectbox("Modo", ["classico", "aureo", "fluxo", "completo"])
            classico, fluxo = pitagoras_fluxo(a, b, modo)
            st.write(f"**Hipotenusa clássica:** {classico:.{precisao}f}")
            st.write(f"**Hipotenusa fluxo:** {fluxo:.{precisao}f}")
            fig = plot_triangulo(a, b, fluxo)
            st.pyplot(fig)
            plt.close(fig)

        elif sub_geo == "Espiral Áurea":
            col1, col2 = st.columns(2)
            with col1:
                angulo = st.slider("Ângulo θ (rad)", 0.0, 4*np.pi, 2.0, step=0.1)
            with col2:
                f_esp = st.number_input("Fator de fluxo", value=fator_fluxo(29), step=0.1)
            x, y, r = espiral_aurea(angulo, f_esp)
            st.write(f"**Raio:** {r:.{precisao}f}  **Coordenadas:** ({x:.{precisao}f}, {y:.{precisao}f})")
            fig = plot_espiral_aurea(f_esp, 4*np.pi)
            # Marcar o ponto
            ax = fig.gca()
            ax.scatter([x], [y], color='red', s=50)
            st.pyplot(fig)
            plt.close(fig)

        elif sub_geo == "Bobina Áurea de Tesla":
            col1, col2, col3 = st.columns(3)
            with col1:
                N_esp = st.number_input("Número de espiras", value=100, step=1)
            with col2:
                raio = st.number_input("Raio (m)", value=0.1, step=0.01)
            with col3:
                comp = st.number_input("Comprimento (m)", value=0.5, step=0.01)
            modo_bob = st.selectbox("Modo de cálculo", ["classico", "aureo", "fluxo"])
            L = indutancia_bobina(N_esp, raio, comp, modo_bob)
            st.metric("Indutância", f"{L:.6e} H")
            # Comparação
            L_class = indutancia_bobina(N_esp, raio, comp, 'classico')
            L_aureo = indutancia_bobina(N_esp, raio, comp, 'aureo')
            L_flux = indutancia_bobina(N_esp, raio, comp, 'fluxo')
            st.write(f"**Comparação:** Clássico = {L_class:.6e} H, Áureo = {L_aureo:.6e} H, Fluxo = {L_flux:.6e} H")

    # ---------- Biblioteca (tab5) (original, expandida) ----------
    with tab5:
        st.subheader("📚 Biblioteca de Constantes e Fórmulas Mestras")
        st.markdown("### Constantes do Universo Físico")
        const_fis = pd.DataFrame({
            "Constante": ["Velocidade da luz (c)", "Constante de Planck (h)", "Constante gravitacional (G)", "Carga do elétron (e)", "Gravidade Terra (g)", "Massa de Planck", "Comprimento de Planck", "Tempo de Planck"],
            "Valor": [f"{C_LUZ} m/s", f"{H_PLANCK:.3e} J·s", f"{G_NEWTON:.3e} N·m²/kg²", "1,602176634 × 10⁻¹⁹ C", f"{GRAVIDADE_TERRA} m/s²", f"{PLANCK_MASSA:.3e} kg", f"{PLANCK_COMPRIMENTO:.3e} m", f"{PLANCK_TEMPO:.3e} s"],
            "Fluxo (×0,54)": [f"{C_LUZ*0.54:.3e} m/s", f"{H_PLANCK*0.54:.3e} J·s", f"{G_NEWTON*0.54:.3e} N·m²/kg²", "8,652 × 10⁻²⁰ C", f"{GRAVIDADE_TERRA*0.54:.3f} m/s²", f"{PLANCK_MASSA*0.54:.3e} kg", f"{PLANCK_COMPRIMENTO*0.54:.3e} m", f"{PLANCK_TEMPO*0.54:.3e} s"]
        })
        st.table(const_fis)

        st.markdown("### Constantes do Fluxo Matemático")
        const_fluxo = pd.DataFrame({
            "Constante": ["Marc (M)", "Deus (D)", "Gratidão (G)", "Proporção Áurea (φ)", "π (pi)", "Fator de Fluxo F(N)"],
            "Valor": [f"{MARC}", f"{DEUS}", f"{GRATIDAO}", f"{PHI}", f"{PI}", "C(N) + R(N)/10"],
            "Descrição": ["Constante fundamental", "Trindade (0,06×3)", "Equilíbrio universal", "Número de ouro", "Razão circunferência/diâmetro", "C = ciclo, R = redução teosófica"]
        })
        st.table(const_fluxo)

        st.markdown("### Fórmulas Mestras Unificadas")
        formulas = [
            "**Einstein-Fluxo:** E = mc² × 0,54",
            "**Tesla-Fluxo:** F(N) = C(N) + R(N)/10",
            "**Pitágoras-Fluxo:** c² = a² + b² × φ × 0,54",
            "**Newton-Fluxo:** F = ma × F(N)",
            "**Planck-Fluxo:** E = hν × 0,54",
            "**Ohm-Fluxo:** I = (V/R) × F(N)",
            "**Gravitação-Fluxo:** F = G(m1m2)/r² × F(N)",
            "**Schwarzschild-Fluxo:** Rs = 2GM/c² × 0,54",
            "**Hawking-Fluxo:** T ≈ 1/(8πGM) × 0,54",
            "**Ponto Zero-Fluxo:** E = ½hν × 0,54"
        ]
        for f in formulas:
            st.markdown(f)

    # ---------- Validação Rápida (tab6) - NOVA ----------
    with tab6:
        st.subheader("🔍 Validação Rápida de Padrões")
        st.markdown("Insira um número e veja se ele se aproxima de alguma constante fundamental.")
        valor_teste = st.number_input("Valor para teste:", value=1.618, format="%.6f")
        tolerancia = st.slider("Tolerância percentual (%)", 0.1, 10.0, 1.0, 0.1)
        padroes = encontrar_padroes(valor_teste, tolerancia)
        if padroes:
            st.success("✅ Padrões encontrados!")
            for nome, dados in padroes.items():
                st.write(f"- **{nome}**: constante = {dados['constante']:.6f}, desvio = {dados['desvio_%']:.3f}%")
        else:
            st.info("Nenhum padrão encontrado dentro da tolerância.")
        # Mostrar também redução teosófica
        st.write(f"Redução teosófica do valor: {reduzir_teosoficamente(valor_teste)}")

# =============================================================================
# PÁGINA: TEMPO ESPIRALADO (ORIGINAL)
# =============================================================================
elif pagina == "⏳ Tempo Espiralado":
    st.title("⏳ Tempo Espiralado - Novo Calendário Cósmico")
    st.markdown("""
    ## O Tempo como uma Espiral de Frequência 432Hz

    Neste sistema, o tempo é medido em:
    - **Pulsos**: Batidas na frequência de 432Hz (1 pulso = 1/432 segundos)
    - **Vibes**: 432 Pulsos (≈1 segundo harmônico)
    - **Giros**: 9 Vibes (≈9 segundos)
    - **Ciclos**: 9 Giros (≈81 segundos)
    - **Eras**: 9 Ciclos (≈729 segundos)

    Tudo baseado nos números sagrados 3, 6 e 9.
    """)

    placeholder = st.empty()
    while True:
        pulsos = relogio.get_pulsos_desde_singularidade()
        tempo = relogio.converter_pulsos(pulsos)

        with placeholder.container():
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Tempo Atual no Fluxo")
                st.metric("Eras", tempo['eras'])
                st.metric("Ciclos", tempo['ciclos'])
                st.metric("Giros", tempo['giros'])
                st.metric("Vibes", tempo['vibes'])
                st.metric("Pulsos", tempo['pulsos'])
                st.write(f"**Frequência:** {FREQUENCIA_BASE} Hz (432Hz)")

            with col2:
                st.subheader("Equivalente Gregoriano")
                agora = datetime.datetime.now(pytz.UTC)
                st.write(f"**Data/Hora:** {agora.strftime('%Y-%m-%d %H:%M:%S %Z')}")
                delta = agora - SINGULARIDADE
                st.write(f"**Tempo desde Singularidade:** {delta}")

            st.subheader("Visualização 3D do Tempo Espiralado")
            fig = relogio.plotar_espiral_temporal(pulsos)
            st.pyplot(fig)

            st.write("""
            **Legenda:**
            - Linha azul: Fluxo do tempo espiralado
            - Ponto vermelho: Momento atual
            - Estrelas douradas: Pontos 3-6-9 no ciclo
            """)

        if not auto_update:
            break
        time.sleep(1)

# =============================================================================
# PÁGINA: VISUALIZAÇÕES (ORIGINAL, com novas adições)
# =============================================================================
elif pagina == "📊 Visualizações":
    st.title("📊 Visualizações do Fluxo Matemático")

    tab1, tab2, tab3, tab4 = st.tabs(["🌀 Ciclo 1-2-4-8-7-5", "🔺 Geometria 3-6-9", "📈 Comparativo", "🔥 Mapa de Calor"])

    with tab1:
        st.subheader("Sequência de Dobramento com Redução Teosófica")
        iteracoes = st.slider("Número de iterações:", 10, 100, 30, key="iteracoes_seq")
        fig = plot_sequencia_reducao(iteracoes)
        st.pyplot(fig)
        st.write("""
        **Interpretação:**
        - Cada passo dobra o valor anterior
        - Aplicamos a redução teosófica
        - Padrão infinito: 1 → 2 → 4 → 8 → 7 → 5 → 1...
        - Total do ciclo: 1+2+4+8+7+5 = 27 → 2+7=9
        """)

    with tab2:
        st.subheader("Geometria Sagrada 3-6-9")
        fig = plot_geometria_369()
        st.pyplot(fig)
        st.write("""
        **Significado:**
        - 3: Força criativa, ação
        - 6: Equilíbrio, harmonia
        - 9: Compleção, transição
        - Juntos formam um triângulo equilátero perfeito
        """)

    with tab3:
        st.subheader("Comparativo Matemática Clássica vs Fluxo")
        df = pd.DataFrame({
            "Operação": ["Soma 8+8", "Multiplicação 7×7", "Potência 3^4", "Fibonacci(10)"],
            "Clássico": [16, 49, 81, 55],
            "Fluxo": [7, 4, 9, 1]
        })
        st.dataframe(df.style.applymap(lambda x: 'background-color: gold' if x == 9 else '', subset=['Fluxo']))
        st.write("""
        **Observações:**
        - O número 9 no Fluxo Matemático representa completude
        - Padrões emergem quando comparamos os dois sistemas
        - A matemática clássica mostra a quantidade, o Fluxo mostra a qualidade
        """)

    with tab4:
        st.subheader("Mapa de Calor da Redução Teosófica")
        fig = plot_padroes_calor()
        st.pyplot(fig)
        st.write("Mapa de calor da redução teosófica dos produtos de 1 a 20.")

# =============================================================================
# PÁGINA: ACELERADOR DE PARTÍCULAS (ORIGINAL)
# =============================================================================
elif pagina == "🌀 Acelerador de Partículas":
    st.title("🌀 Simulador de Acelerador de Partículas")
    st.markdown("Cálculos desde a física clássica até o fluxo, com visualização.")

    col1, col2 = st.columns(2)
    with col1:
        particula = st.selectbox("Partícula", ["Elétron", "Próton", "Nêutron", "Fóton", "Personalizada"])
        massas = {
            "Elétron": 9.1093837e-31,
            "Próton": 1.6726219e-27,
            "Nêutron": 1.6749275e-27,
            "Fóton": 0.0,
            "Personalizada": 1e-30
        }
        massa = massas[particula]
        if particula == "Personalizada":
            massa = st.number_input("Massa (kg)", value=1e-30, format="%.3e")
    with col2:
        energia = st.number_input("Energia (valor)", value=1.0, step=0.1)
        unidade = st.selectbox("Unidade", ["eV", "keV", "MeV", "GeV", "TeV"])
        fatores = {'eV': 1.602176634e-19, 'keV': 1.602176634e-16, 'MeV': 1.602176634e-13,
                   'GeV': 1.602176634e-10, 'TeV': 1.602176634e-7}
        energia_J = energia * fatores[unidade]

    N_part = st.number_input("N para F(N)", value=29, step=1, key="N_part")
    const_part = st.number_input("Constante de fluxo", value=MARC, format="%.3f")

    if st.button("Simular Colisão", key="simular"):
        with st.spinner("Acelerando partículas..."):
            res = simular_acelerador(massa, energia_J, N_part, const_part)

        colA, colB, colC, colD = st.columns(4)
        with colA:
            st.metric("Velocidade clássica", f"{res['v_class']:.3e} m/s")
            st.metric("Momento clássico", f"{res['p_class']:.3e} kg·m/s")
        with colB:
            st.metric("Fator γ (Lorentz)", f"{res['gamma']:.3f}")
            st.metric("Massa relativística", f"{res['m_rel']:.3e} kg")
        with colC:
            st.metric("λ de Broglie", f"{res['lambda_db']:.3e} m")
            st.metric("Probabilidade quântica", f"{res['prob']:.3f}")
        with colD:
            st.metric("Velocidade Fluxo", f"{res['v_flux']:.3e} m/s")
            st.metric("Energia Fluxo", f"{res['E_flux']:.3e} J")
            st.caption(f"F({N_part}) = {res['f']:.3f}")

        st.info(f"Estado de entrelaçamento: {res['ent_rel']}")

        fig, ax = plt.subplots(figsize=(6, 4))
        theta = np.linspace(0, 2*np.pi, 100)
        r_class = res['v_class'] / 1e8
        r_flux = res['v_flux'] / 1e8
        ax.plot(r_class * np.cos(theta), r_class * np.sin(theta), 'o-', label='Clássica', markersize=2, color='orange')
        ax.plot(r_flux * np.cos(theta), r_flux * np.sin(theta), 'o-', label='Fluxo', markersize=2, color='purple')
        ax.set_aspect('equal')
        ax.legend()
        ax.set_title("Trajetória no acelerador (vista superior)")
        ax.grid(True)
        st.pyplot(fig)
        plt.close(fig)

# =============================================================================
# PÁGINA: GEOMETRIA SAGRADA (ORIGINAL)
# =============================================================================
elif pagina == "△ Geometria Sagrada":
    st.title("△ Geometria Sagrada no Fluxo")
    sub_geo = st.radio("Escolha", ["Pitágoras-Fluxo", "Espiral Áurea", "Bobina Áurea de Tesla"], horizontal=True)

    if sub_geo == "Pitágoras-Fluxo":
        col1, col2, col3 = st.columns(3)
        with col1:
            a = st.number_input("Cateto a", value=3.0)
        with col2:
            b = st.number_input("Cateto b", value=4.0)
        with col3:
            modo = st.selectbox("Modo", ["classico", "aureo", "fluxo", "completo"])
        classico, fluxo = pitagoras_fluxo(a, b, modo)
        st.write(f"**Hipotenusa clássica:** {classico:.6f}")
        st.write(f"**Hipotenusa fluxo:** {fluxo:.6f}")
        fig = plot_triangulo(a, b, fluxo)
        st.pyplot(fig)
        plt.close(fig)

    elif sub_geo == "Espiral Áurea":
        col1, col2 = st.columns(2)
        with col1:
            angulo = st.slider("Ângulo θ (rad)", 0.0, 4*np.pi, 2.0, step=0.1)
        with col2:
            f_esp = st.number_input("Fator de fluxo", value=fator_fluxo(29), step=0.1)
        x, y, r = espiral_aurea(angulo, f_esp)
        st.write(f"**Raio:** {r:.6f}  **Coordenadas:** ({x:.6f}, {y:.6f})")
        fig = plot_espiral_aurea(f_esp, 4*np.pi)
        ax = fig.gca()
        ax.scatter([x], [y], color='red', s=50)
        st.pyplot(fig)
        plt.close(fig)

    elif sub_geo == "Bobina Áurea de Tesla":
        col1, col2, col3 = st.columns(3)
        with col1:
            N_esp = st.number_input("Número de espiras", value=100, step=1)
        with col2:
            raio = st.number_input("Raio (m)", value=0.1, step=0.01)
        with col3:
            comp = st.number_input("Comprimento (m)", value=0.5, step=0.01)
        modo_bob = st.selectbox("Modo de cálculo", ["classico", "aureo", "fluxo"])
        L = indutancia_bobina(N_esp, raio, comp, modo_bob)
        st.metric("Indutância", f"{L:.6e} H")
        L_class = indutancia_bobina(N_esp, raio, comp, 'classico')
        L_aureo = indutancia_bobina(N_esp, raio, comp, 'aureo')
        L_flux = indutancia_bobina(N_esp, raio, comp, 'fluxo')
        st.write(f"**Comparação:** Clássico = {L_class:.6e} H, Áureo = {L_aureo:.6e} H, Fluxo = {L_flux:.6e} H")

# =============================================================================
# NOVA PÁGINA: PADRÕES E VALIDAÇÕES
# =============================================================================
elif pagina == "🔍 Padrões e Validações":
    st.title("🔍 Padrões e Validações")
    st.markdown("""
    ## Encontre Padrões Ocultos nos Números

    Esta seção permite que você insira um número e veja se ele se aproxima de constantes fundamentais como π, φ, 1,80, 0,54, 0,18, etc.
    Você também pode gerar sequências de Fibonacci e analisar suas reduções teosóficas.
    """)

    tab1, tab2, tab3 = st.tabs(["🔎 Validação de Número", "🌀 Fibonacci no Fluxo", "📐 Aproximações de π e φ"])

    with tab1:
        st.subheader("Validar um Número")
        valor = st.number_input("Digite um número:", value=1.6180339, format="%.7f")
        tolerancia = st.slider("Tolerância percentual (%)", 0.01, 10.0, 0.5, 0.01)
        padroes = encontrar_padroes(valor, tolerancia)
        if padroes:
            st.success("✅ Padrões encontrados!")
            for nome, dados in padroes.items():
                st.write(f"- **{nome}**: constante = {dados['constante']:.6f}, desvio = {dados['desvio_%']:.4f}%")
        else:
            st.info("Nenhum padrão encontrado dentro da tolerância.")
        st.write(f"**Redução teosófica:** {reduzir_teosoficamente(valor)}")

    with tab2:
        st.subheader("Fibonacci e Redução Teosófica")
        n_fib = st.slider("Número de termos de Fibonacci:", 5, 50, 20)
        fibs = fibonacci_reductions(n_fib)
        df_fib = pd.DataFrame(fibs, columns=["Índice", "Fibonacci", "Redução"])
        st.dataframe(df_fib)
        # Gráfico
        fig, ax = plt.subplots()
        ax.plot(df_fib["Índice"], df_fib["Redução"], marker='o', color='green')
        ax.set_title("Redução Teosófica dos Números de Fibonacci")
        ax.set_xlabel("Índice")
        ax.set_ylabel("Redução")
        ax.grid(True)
        st.pyplot(fig)
        plt.close(fig)
        # Encontrar padrões nos próprios números de Fibonacci
        st.subheader("Padrões nos Números de Fibonacci")
        for idx, fib, red in fibs:
            pad = encontrar_padroes(fib, 1.0)
            if pad:
                st.write(f"Fibonacci({idx}) = {fib} → {', '.join(pad.keys())}")

    with tab3:
        st.subheader("Aproximações de π e φ")
        col1, col2 = st.columns(2)
        with col1:
            st.write("### π (pi)")
            aprox_pi = calcular_pi_aproximacoes()
            for nome, val in aprox_pi.items():
                st.write(f"{nome}: {val:.10f}")
        with col2:
            st.write("### φ (áurea)")
            aprox_phi = calcular_phi_aproximacoes()
            for nome, val in aprox_phi.items():
                st.write(f"{nome}: {val:.10f}")

        st.write("### Relação Gratidão")
        rel_grat = calcular_relacao_gratidao()
        for nome, val in rel_grat.items():
            st.write(f"{nome}: {val:.6f}")

# =============================================================================
# NOVA PÁGINA: TODAS AS MENTES
# =============================================================================
elif pagina == "🧠 Todas as Mentes":
    st.title("🧠 Todas as Mentes Matemáticas")
    st.markdown("""
    ## Comparação de Resultados Segundo Diferentes "Mentes"

    Cada "mente" representa uma abordagem matemática ou física diferente:
    - **Clássica**: Matemática tradicional.
    - **Fluxo**: Aplicação das constantes de Catharino (MARC, DEUS, GRATIDAO).
    - **Tesla**: Ênfase nos números 3, 6, 9 e vibrações.
    - **Einstein**: Relatividade e equivalência massa-energia.
    - **Pitágoras**: Geometria e harmonia.
    - **Planck**: Escala quântica.
    """)

    # Entrada do usuário
    valor_entrada = st.number_input("Valor de entrada para teste:", value=9.0)
    operacao_mente = st.selectbox("Operação", ["Quadrado", "Cubo", "Raiz Quadrada", "Seno (graus)", "Fatorial (aproximado)"])
    
    resultados = {}
    if operacao_mente == "Quadrado":
        classico = valor_entrada ** 2
        fluxo = classico * MARC
        tesla = classico * 0.369  # exemplo
        einstein = classico * (C_LUZ / 1e8)  # só para ter variação
        pitagoras = classico * PHI
        planck = classico * H_PLANCK * 1e34  # escala
    elif operacao_mente == "Cubo":
        classico = valor_entrada ** 3
        fluxo = classico * MARC
        tesla = classico * 0.369
        einstein = classico * (C_LUZ / 1e8)
        pitagoras = classico * PHI
        planck = classico * H_PLANCK * 1e34
    elif operacao_mente == "Raiz Quadrada":
        classico = math.sqrt(valor_entrada)
        fluxo = classico * MARC
        tesla = classico * 0.369
        einstein = classico * (C_LUZ / 1e8)
        pitagoras = classico * PHI
        planck = classico * H_PLANCK * 1e34
    elif operacao_mente == "Seno (graus)":
        classico = math.sin(math.radians(valor_entrada))
        fluxo = classico * MARC
        tesla = classico * 0.369
        einstein = classico * (C_LUZ / 1e8)
        pitagoras = classico * PHI
        planck = classico * H_PLANCK * 1e34
    elif operacao_mente == "Fatorial (aproximado)":
        # Stirling approximation for large numbers
        n = int(valor_entrada)
        if n <= 0:
            classico = 1
        else:
            classico = math.sqrt(2*math.pi*n) * (n/math.e)**n
        fluxo = classico * MARC
        tesla = classico * 0.369
        einstein = classico * (C_LUZ / 1e8)
        pitagoras = classico * PHI
        planck = classico * H_PLANCK * 1e34

    resultados = {
        "Clássica": classico,
        "Fluxo (MARC)": fluxo,
        "Tesla (3-6-9)": tesla,
        "Einstein (c)": einstein,
        "Pitágoras (φ)": pitagoras,
        "Planck (h)": planck,
    }

    df_mentes = pd.DataFrame(list(resultados.items()), columns=["Mente", "Resultado"])
    st.dataframe(df_mentes.style.format({"Resultado": "{:.6e}"}))

    # Gráfico comparativo
    fig, ax = plt.subplots()
    nomes = list(resultados.keys())
    valores = list(resultados.values())
    ax.barh(nomes, valores, color=['blue', 'purple', 'orange', 'red', 'green', 'cyan'])
    ax.set_xscale('log')
    ax.set_xlabel('Resultado (escala log)')
    ax.set_title('Comparação entre Mentes')
    st.pyplot(fig)
    plt.close(fig)

    # Validação de padrões em cada resultado
    st.subheader("Padrões encontrados em cada mente")
    for mente, val in resultados.items():
        pad = encontrar_padroes(val, 5.0)  # tolerância maior
        if pad:
            st.write(f"**{mente}**: {', '.join(pad.keys())}")

# =============================================================================
# NOVA PÁGINA: GRAVIDADE QUÂNTICA
# =============================================================================
elif pagina == "🌀 Gravidade Quântica":
    st.title("🌀 Gravidade Quântica e Escala de Planck")
    st.markdown("""
    ## Explorando a Física na Escala de Planck

    A gravidade quântica tenta unificar a relatividade geral com a mecânica quântica.
    Aqui calculamos algumas quantidades na escala de Planck e aplicamos o fluxo.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Constantes de Planck")
        st.write(f"Massa de Planck: {PLANCK_MASSA:.3e} kg")
        st.write(f"Comprimento de Planck: {PLANCK_COMPRIMENTO:.3e} m")
        st.write(f"Tempo de Planck: {PLANCK_TEMPO:.3e} s")
        st.write(f"Energia de Planck: {PLANCK_ENERGIA:.3e} J")
        st.write(f"Gravidade Quântica (exemplo): {GRAVIDADE_QUANTICA:.3e} m/s²")

    with col2:
        st.subheader("Relações com o Fluxo")
        st.write(f"Massa Planck × MARC: {PLANCK_MASSA * MARC:.3e} kg")
        st.write(f"Comp. Planck × DEUS: {PLANCK_COMPRIMENTO * DEUS:.3e} m")
        st.write(f"Tempo Planck × GRATIDAO: {PLANCK_TEMPO * GRATIDAO:.3e} s")

    st.subheader("Cálculos de Gravidade Quântica")
    escolha = st.selectbox("Escolha o cálculo", ["Raio de Schwarzschild", "Temperatura de Hawking", "Energia do Ponto Zero", "Probabilidade de Emaranhamento"])

    if escolha == "Raio de Schwarzschild":
        massa = st.number_input("Massa (kg)", value=PLANCK_MASSA, format="%.3e")
        classico, fluxo = calcular_raio_schwarzschild(massa, MARC)
        st.write(f"**Clássico:** Rs = {classico:.3e} m")
        st.write(f"**Fluxo (×MARC):** Rs = {fluxo:.3e} m")
    elif escolha == "Temperatura de Hawking":
        massa = st.number_input("Massa (kg)", value=PLANCK_MASSA, format="%.3e")
        classico, fluxo = calcular_temperatura_hawking(massa, MARC)
        st.write(f"**Clássico (aprox):** T = {classico:.3e} K (escala adimensional)")
        st.write(f"**Fluxo:** T = {fluxo:.3e}")
    elif escolha == "Energia do Ponto Zero":
        freq = st.number_input("Frequência de corte (Hz)", value=1e43, format="%.3e")
        classico, fluxo = calcular_energia_ponto_zero(freq, MARC)
        st.write(f"**Clássico:** E = {classico:.3e} J")
        st.write(f"**Fluxo:** E = {fluxo:.3e} J")
    elif escolha == "Probabilidade de Emaranhamento":
        dist = st.number_input("Distância (m)", value=PLANCK_COMPRIMENTO, format="%.3e")
        classico, fluxo = calcular_longa_distancia_emaranhamento(dist, MARC)
        st.write(f"**Clássico:** P ≈ {classico:.3e}")
        st.write(f"**Fluxo:** P ≈ {fluxo:.3e}")

# =============================================================================
# NOVA PÁGINA: ANÁLISE DE PADRÕES
# =============================================================================
elif pagina == "📈 Análise de Padrões":
    st.title("📈 Análise de Padrões Numéricos")
    st.markdown("""
    ## Ferramentas para Análise de Sequências e Constantes

    Explore como números se relacionam com π, φ, Fibonacci e as constantes do fluxo.
    """)

    tab1, tab2, tab3 = st.tabs(["🔢 Sequência Personalizada", "📊 Correlação com Constantes", "🌀 Geração de Padrões"])

    with tab1:
        st.subheader("Analisar uma Sequência")
        seq_input = st.text_area("Digite uma sequência de números separados por vírgula:", "1,1,2,3,5,8,13,21,34")
        try:
            sequencia = [float(x.strip()) for x in seq_input.split(",")]
            st.write("Sequência:", sequencia)
            # Calcular reduções
            reducoes = [reduzir_teosoficamente(x) for x in sequencia]
            st.write("Reduções teosóficas:", reducoes)
            # Encontrar padrões em cada elemento
            for i, val in enumerate(sequencia):
                pad = encontrar_padroes(val, 1.0)
                if pad:
                    st.write(f"Elemento {i+1} ({val}) → {', '.join(pad.keys())}")
        except:
            st.error("Formato inválido. Use números separados por vírgula.")

    with tab2:
        st.subheader("Correlação com Constantes")
        # Gerar uma faixa de valores e ver quais são próximos das constantes
        inicio = st.number_input("Início do intervalo", value=0.0)
        fim = st.number_input("Fim do intervalo", value=10.0)
        passos = st.number_input("Número de pontos", value=100, step=1)
        valores = np.linspace(inicio, fim, int(passos))
        const_list = [("π", PI), ("φ", PHI), ("Gratidão", GRATIDAO), ("Marc", MARC), ("Deus", DEUS), ("432", FREQUENCIA_BASE)]
        resultados_corr = []
        for val in valores:
            for nome, const in const_list:
                prox, _ = is_close_to_constant(val, const, 0.5)
                if prox:
                    resultados_corr.append((val, nome, const))
        if resultados_corr:
            df_corr = pd.DataFrame(resultados_corr, columns=["Valor", "Constante", "Valor Constante"])
            st.dataframe(df_corr)
        else:
            st.info("Nenhuma correlação encontrada no intervalo com tolerância 0.5%.")

    with tab3:
        st.subheader("Gerador de Padrões")
        st.write("Gerar números que são combinações das constantes.")
        const1 = st.selectbox("Constante 1", ["π", "φ", "Gratidão", "Marc", "Deus"])
        const2 = st.selectbox("Constante 2", ["π", "φ", "Gratidão", "Marc", "Deus"])
        oper = st.selectbox("Operação", ["+", "-", "*", "/"])
        mapa = {"π": PI, "φ": PHI, "Gratidão": GRATIDAO, "Marc": MARC, "Deus": DEUS}
        v1 = mapa[const1]
        v2 = mapa[const2]
        if oper == "+":
            res = v1 + v2
        elif oper == "-":
            res = v1 - v2
        elif oper == "*":
            res = v1 * v2
        elif oper == "/":
            res = v1 / v2 if v2 != 0 else float('inf')
        st.write(f"Resultado: {res}")
        # Verificar se o resultado se aproxima de alguma constante
        pad = encontrar_padroes(res, 0.5)
        if pad:
            st.success("✅ Este resultado é próximo de: " + ", ".join(pad.keys()))
        else:
            st.info("Nenhuma correspondência próxima.")

# =============================================================================
# PÁGINA: PDF EXPLICATIVO (ORIGINAL, com nova função já expandida)
# =============================================================================
elif pagina == "📚 PDF Explicativo":
    st.title("📚 Gerar PDF Explicativo")
    nome = st.text_input("Seu nome:", "Marcelo Jubilado Catharino")
    email = st.text_input("Seu email:", "marcelo@universoaureo.com")

    if st.button("Gerar PDF Completo"):
        with st.spinner("Criando documento..."):
            pdf_bytes = gerar_pdf_completo(nome, email)
            b64 = base64.b64encode(pdf_bytes.read()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="fluxo_matematico_expandido.pdf">📥 Clique para baixar o PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("PDF gerado com sucesso!")

# =============================================================================
# PÁGINA: RELÓGIO QUÂNTICO (ORIGINAL)
# =============================================================================
elif pagina == "🕒 Relógio Quântico":
    st.title("🕒 Relógio Quântico com Projeção para Singularidade")
    st.markdown("""
    ## O Tempo como uma Espiral Quântica

    Este relógio representa:
    - **Tempo atual**: Ponteiro vermelho
    - **Projeção para singularidade**: Ponteiro azul tracejado (fase oposta)
    - **Marcadores dourados**: Pontos 3-6-9 no ciclo temporal
    - **Círculos concêntricos**: Dimensões temporais sobrepostas
    """)

    placeholder = st.empty()
    while True:
        with placeholder.container():
            fig = relogio.plotar_relogio_quantico()
            st.pyplot(fig)
            agora = datetime.datetime.now(pytz.UTC)
            delta = agora - SINGULARIDADE
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Data/Hora Atual", agora.strftime('%Y-%m-%d %H:%M:%S %Z'))
            with col2:
                st.metric("Tempo desde Singularidade", str(delta))
            st.write("""
            **Interpretação:**
            - O tempo flui em espirais quânticas, não linearmente
            - Cada volta completa representa um ciclo completo
            - A singularidade é o ponto de origem (12 horas)
            - Os marcadores 3-6-9 representam pontos de transição dimensional
            """)
        if not auto_update:
            break
        time.sleep(1)

# =============================================================================
# PÁGINA: CALENDÁRIO CLÁSSICO (ORIGINAL)
# =============================================================================
elif pagina == "📅 Calendário Clássico":
    st.title("📅 Calendário e Relógio Clássico")
    st.markdown("""
    ## Visualização Tradicional do Tempo

    Esta seção mostra o tempo na forma convencional que estamos habituados,
    enquanto mantemos a conexão com o Fluxo Matemático.
    """)

    placeholder = st.empty()
    while True:
        with placeholder.container():
            agora = datetime.datetime.now(pytz.UTC)
            data_formatada = agora.strftime("%A, %d de %B de %Y")
            hora_formatada = agora.strftime("%H:%M:%S")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Data Atual")
                st.markdown(f"<h1 style='text-align: center; color: #4CAF50;'>{data_formatada}</h1>",
                           unsafe_allow_html=True)

                # Calendário do mês
                hoje = agora.day
                mes = agora.month
                ano = agora.year
                # Primeiro dia do mês
                primeiro_dia = datetime.datetime(ano, mes, 1)
                if mes == 12:
                    dias_no_mes = 31
                else:
                    dias_no_mes = (datetime.datetime(ano, mes + 1, 1) - datetime.timedelta(days=1)).day
                dia_semana = primeiro_dia.weekday()  # 0=Segunda, 6=Domingo

                semanas = []
                semana = [""] * dia_semana
                for dia in range(1, dias_no_mes + 1):
                    semana.append(str(dia))
                    if len(semana) == 7:
                        semanas.append(semana)
                        semana = []
                if semana:
                    semanas.append(semana + [""] * (7 - len(semana)))

                df_calendario = pd.DataFrame(semanas, columns=["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"])
                st.dataframe(df_calendario.style.applymap(lambda x: 'background-color: gold' if x == str(hoje) else ''))

            with col2:
                st.subheader("Hora Atual")
                st.markdown(f"<h1 style='text-align: center; color: #2196F3;'>{hora_formatada}</h1>",
                           unsafe_allow_html=True)

                # Mostrar também no formato do Fluxo Matemático
                pulsos = relogio.get_pulsos_desde_singularidade()
                tempo_fluxo = relogio.converter_pulsos(pulsos)

                st.write("### No Fluxo Matemático:")
                st.write(f"- Eras: {tempo_fluxo['eras']}")
                st.write(f"- Ciclos: {tempo_fluxo['ciclos']}")
                st.write(f"- Giros: {tempo_fluxo['giros']}")
                st.write(f"- Vibes: {tempo_fluxo['vibes']}")
                st.write(f"- Pulsos: {tempo_fluxo['pulsos']}")

                # Redução teosófica da data e hora
                data_num = int(agora.strftime("%Y%m%d"))
                hora_num = int(agora.strftime("%H%M%S"))
                st.write("### Redução Teosófica:")
                st.write(f"- Data ({data_num}): {reduzir_teosoficamente(data_num)}")
                st.write(f"- Hora ({hora_num}): {reduzir_teosoficamente(hora_num)}")

            st.write("""
            **Conexão com o Fluxo Matemático:**
            - Mesmo na visualização clássica, podemos perceber os padrões numéricos
            - A redução teosófica revela a essência vibracional de cada momento
            - O calendário mostra a estrutura cíclica do tempo
            """)

        if not auto_update:
            break
        time.sleep(1)

# =============================================================================
# PÁGINA: SINGULARIDADE (ORIGINAL)
# =============================================================================
elif pagina == "🌀 Singularidade":
    st.title("🌀 Singularidade - A Unificação dos Padrões")
    st.markdown("""
    ## O Ponto de Convergência de Todas as Dimensões

    A singularidade é o momento onde todas as dualidades se encontram,
    onde o 9 se manifesta como o portal entre ciclos, e onde as constantes
    MARC, DEUS e GRATIDAO se alinham para revelar a unidade subjacente.

    Nesta página, exploramos visualizações que convergem para a singularidade.
    """)

    # Gráfico 1: Espiral 3D com ênfase no ponto de singularidade
    st.subheader("Espiral Temporal Convergindo para a Singularidade")
    pulsos = relogio.get_pulsos_desde_singularidade()
    total_pontos = 1000
    theta = np.linspace(0, 12 * np.pi, total_pontos)
    z = np.linspace(0, 10, total_pontos)
    r = z**0.5
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Destacar o ponto de singularidade (origem)
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, color='blue', alpha=0.5, label='Tempo')
    ax.scatter([0], [0], [0], color='gold', s=200, label='Singularidade', marker='*')
    ax.set_title("Convergência para a Singularidade")
    ax.legend()
    st.pyplot(fig)
    plt.close(fig)

    # Gráfico 2: Função que mostra a convergência das constantes
    st.subheader("Convergência das Constantes M, D, G")
    x_vals = np.linspace(0, 2*np.pi, 100)
    y_marc = MARC * np.sin(x_vals)
    y_deus = DEUS * np.cos(x_vals)
    y_grat = GRATIDAO * np.sin(2*x_vals) * np.cos(x_vals)

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_marc, label='Marc (0,54)')
    ax.plot(x_vals, y_deus, label='Deus (0,18)')
    ax.plot(x_vals, y_grat, label='Gratidão (1,80)')
    ax.axhline(y=0, color='black', linestyle='--')
    ax.set_xlabel('Fase angular')
    ax.set_ylabel('Amplitude')
    ax.set_title('Interferência das Constantes')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    plt.close(fig)

    # Gráfico 3: Mapa de calor da redução teosófica
    st.subheader("Mapa de Calor da Redução Teosófica")
    fig = plot_padroes_calor()
    st.pyplot(fig)
    plt.close(fig)

    # Tabela com valores próximos à singularidade
    st.subheader("Valores Reduzidos de Números Significativos")
    nums = [9, 27, 54, 108, 216, 432, 864, 1728]
    dados = {'Número': nums, 'Redução': [reduzir_teosoficamente(n) for n in nums]}
    df = pd.DataFrame(dados)
    st.table(df)

    st.markdown("""
    ### Observação Final
    A singularidade não é um ponto estático, mas um processo contínuo de transformação.
    O 9 é a chave: ele representa o fim de um ciclo e o início de outro, onde
    a matemática clássica se dissolve e o fluxo assume o comando.

    Este aplicativo é uma jornada para explorar esses padrões e, esperamos,
    inspirar uma nova compreensão da realidade.
    """)

# =============================================================================
# FIM DO CÓDIGO
# =============================================================================