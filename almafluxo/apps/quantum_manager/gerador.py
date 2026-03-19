# QUANTUM_CODE_MANAGER_PRO_ULTIMATE.py
from pathlib import Path
from datetime import datetime
import ast
import streamlit as st
import pandas as pd
import numpy as np
import re
import os
import locale
import sys
import platform
import subprocess
import pkg_resources
import importlib
import shutil
from collections import defaultdict
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import tkinter as tk
from tkinter import filedialog
from charset_normalizer import from_bytes
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qiskit.circuit import Measure
import cpuinfo
import psutil

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')  # Para Windows
    except locale.Error:
        locale.setlocale(locale.LC_ALL, '')  # Usa configuração padrão do sistema
        
if sys.platform.startswith('win'):
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    
    # Configurar encoding padrão para todas as saídas
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
else:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        
# Configurações globais
st.set_page_config(
    page_title="🚀 Quantum Code Manager Pro Ultimate Supreme",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos Avançados com melhorias
st.markdown("""
<style>
    :root {
        --primary: #00FF88;
        --background: #0E1117;
        --secondary: #1F2937;
    }
    
    .main { 
        background: linear-gradient(180deg, var(--background) 0%, #1a1a2e 100%);
        color: white; 
    }
    
    .stAlert { 
        border: 2px solid var(--primary); 
        border-radius: 15px;
        background: rgba(0, 255, 136, 0.1) !important;
    }
    
    .quantum-card { 
        padding: 1.5rem; 
        border: 2px solid var(--primary);
        border-radius: 15px; 
        margin: 1rem 0;
        background: rgba(16, 25, 40, 0.8);
    }
    
    .terminal { 
        background: #000; 
        color: var(--primary); 
        font-family: 'Courier New', monospace; 
        padding: 1.5rem; 
        border-radius: 10px;
        border: 1px solid var(--primary);
    }
    
    .hover-card:hover {
        transform: scale(1.02);
        transition: transform 0.3s ease;
        box-shadow: 0 0 15px var(--primary);
    }
    
    .stPlotlyChart {
        border: 1px solid var(--primary);
        border-radius: 10px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

try:
    from qiskit_aer import Aer
    print("✅ Qiskit Aer instalado corretamente!")
except ImportError:
    print("❌ Instale o Qiskit Aer: pip install qiskit-aer")
    exit()

class SystemInspector:
    def _get_qiskit_version(self):
        try:
            return Aer.__version__
        except AttributeError:
            return "Não instalado"

    def get_detailed_report(self):
        mem = psutil.virtual_memory()
        return {
            "🖥️ Sistema Operacional": f"{platform.platform()}",
            "🏗️ Arquitetura": f"{platform.architecture()[0]}",
            "⚡ CPU": f"{cpuinfo.get_cpu_info()['brand_raw']} ({os.cpu_count()} núcleos)",
            "💾 Memória": f"Total: {mem.total / (1024**3):.1f} GB | Livre: {mem.available / (1024**3):.1f} GB",
            "🐍 Python": f"{sys.version.split()[0]}",
            "🚀 Qiskit Aer": f"v{self._get_qiskit_version()}"
        }

    def check_essential_tools(self):
        return {
            '💻 Terminal Padrão': self._check_cmd(),
            '🔋 PowerShell': self._check_powershell(),
            '🐙 Git': self._check_git(),
            '🐍 Python 3': self._check_python(),
            '📦 Pip': self._check_pip()
        }

    def _check_cmd(self):
        return "✅ Instalado" if os.name == 'nt' else "⚠️ Não disponível no Linux"

    def _check_powershell(self):
        try:
            subprocess.run(["pwsh", "--version"], check=True, capture_output=True)
            return "✅ Instalado"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "❌ Não instalado"

    def _check_git(self):
        try:
            subprocess.run(["git", "--version"], check=True, capture_output=True)
            return "✅ Instalado"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "❌ Não instalado"

    def _check_python(self):
        return "✅ Python 3.x" if sys.version_info.major == 3 else "❌ Versão não suportada"

    def _check_pip(self):
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
            return "✅ Instalado"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "❌ Não instalado"

def select_directory():
    """Seleção de diretório com tratamento de erros melhorado"""
    try:
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        selected_path = filedialog.askdirectory(title="Selecione a pasta do projeto")
        root.destroy()
    
        if not selected_path:
            return None
        
        path = Path(selected_path).resolve()
        if not path.exists():
            st.error("Diretório não existe!")
            return None
        
        return path.as_posix()
    except Exception as e:
        st.error(f"Erro na seleção: {str(e)}")
        return None

class QuantumDependencyManager:
    def __init__(self):
        # Lista de módulos built-in que não devem ser incluídos
        self.builtins = set(sys.builtin_module_names) | {
            '__future__', 'os', 'sys', 're', 'pathlib', 'shutil', 
            'subprocess', 'platform', 'collections', 'ast',
            'importlib', 'locale', 'tkinter', 'pkg_resources'
        }
        
        # Diretórios a serem excluídos da análise
        self.excluded_dirs = {'venv', '.venv', '__pycache__', '.git', 'env', 'node_modules'}
        
        # Mapeamento de imports para nomes de pacotes
        self.import_map = {
            'yaml': 'PyYAML',
            'sklearn': 'scikit-learn',
            'PIL': 'Pillow',
            'cv2': 'opencv-python-headless',
            'streamlit_ace': 'streamlit-ace',
            'cpuinfo': 'py-cpuinfo',
            'folium': 'folium',
            'streamlit_folium': 'streamlit-folium',
            'plotly': 'plotly',
            'seaborn': 'seaborn',
            'sklearn': 'scikit-learn',
            'numpy': 'numpy',
            'pandas': 'pandas',
            'matplotlib': 'matplotlib',
            'qiskit': 'qiskit',
            'qiskit_aer': 'qiskit-aer',
            'psutil': 'psutil'
        }

    def analyze_project_dependencies(self, project_path, selected_files=None):
        all_imports = self._scan_project_imports(Path(project_path), selected_files)
        return self._generate_requirements(all_imports)

    def _scan_project_imports(self, project_path, selected_files):
        all_imports = set()
        
        if selected_files:
            py_files = [project_path / f for f in selected_files if (project_path / f).is_file()]
        else:
            py_files = [f for f in project_path.rglob("*.py") if f.is_file()]
        
        for py_file in py_files:
            # Verificar se o arquivo está em um diretório excluído
            if any(part in self.excluded_dirs for part in py_file.parts):
                continue
                
            content = self._safe_read_file(py_file)
            all_imports.update(self._parse_imports(content))
            
        return all_imports

    def _parse_imports(self, content):
        try:
            tree = ast.parse(content)
            imports = set()
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if (root := alias.name.split('.')[0]) not in self.builtins:
                            imports.add(root)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    if (root := node.module.split('.')[0]) not in self.builtins:
                        imports.add(root)
            return imports
        except SyntaxError as e:
            st.warning(f"⚠️ Erro de sintaxe: {str(e)}")
            return set()

    def _safe_read_file(self, file_path):
        try:
            with file_path.open('rb') as f:
                raw_data = f.read()
                result = from_bytes(raw_data).best()
                return str(result) if result else raw_data.decode('utf-8', errors='replace')
        except UnicodeDecodeError as e:
            st.error(f"Erro de decodificação em {file_path.name}: {str(e)}")
            return raw_data.decode('utf-8', errors='replace')
        except Exception as e:
            st.error(f"Erro de leitura: {file_path.name} - {str(e)}")
            return ''

    def _generate_requirements(self, imports):
        req = []
        installed = {pkg.key.lower(): pkg for pkg in pkg_resources.working_set}
        
        for imp in sorted(imports, key=lambda x: x.lower()):
            # Ignorar módulos built-in
            if imp in self.builtins:
                continue
                
            pkg_name = self.import_map.get(imp, imp)
            pkg = installed.get(pkg_name.lower())
            
            if pkg:
                req.append(f"{pkg_name}=={pkg.version}")
            else:
                try:
                    version_info = subprocess.check_output(
                        [sys.executable, "-m", "pip", "show", pkg_name],
                        stderr=subprocess.STDOUT
                    ).decode('utf-8', errors='replace')
                    
                    version = re.search(r'Version:\s*(.*)', version_info)
                    if version:
                        req.append(f"{pkg_name}=={version.group(1).strip()}")
                    else:
                        if self._is_installable(pkg_name):
                            req.append(pkg_name)
                except Exception:
                    if self._is_installable(pkg_name):
                        req.append(pkg_name)
        
        # Adicionar Python apenas se houver outras dependências
        if req:
            req.insert(0, f"python=={platform.python_version()}")
            
        return req

    def _is_installable(self, package_name):
        """Verifica se o pacote existe no PyPI"""
        try:
            import requests
            response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=3)
            return response.status_code == 200
        except Exception:
            return False

class ProjectDoctor:
    def __init__(self):
        self.excluded_dirs = {'venv', '.venv', '.git', '__pycache__', 'env', 'node_modules'}
        self.dependency_manager = QuantumDependencyManager()

    def analyze_project_dependencies(self, project_path, selected_files=None):
        return self.dependency_manager.analyze_project_dependencies(project_path, selected_files)

    def perform_full_scan(self, project_path):
        with st.spinner("🔍 Varredura quântica do projeto..."):
            try:
                project_path = Path(project_path).resolve()
                if not project_path.exists():
                    raise ValueError("Diretório não existe")

                return {
                    'requirements': self._find_requirements(project_path),
                    'init_files': self._find_missing_inits(project_path),
                    'structure': self._map_structure(project_path),
                    'stats': self._calculate_stats(project_path)
                }
            except Exception as e:
                st.error(f"Erro na análise quântica: {str(e)}")
                return None

    def _find_requirements(self, project_path):
        return self.dependency_manager.analyze_project_dependencies(project_path)

    def _find_missing_inits(self, project_path):
        missing = []
        project_path = Path(project_path)
        
        for root, dirs, _ in os.walk(project_path):
            # Remove diretórios excluídos da lista de diretórios a serem percorridos
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            for d in dirs:
                dir_path = Path(root) / d
                init_path = dir_path / "__init__.py"
                
                # Verifica se é um subdiretório válido e não está na lista de exclusão
                if not init_path.exists() and dir_path != project_path:
                    try:
                        rel_path = dir_path.relative_to(project_path)
                        missing.append(str(rel_path))
                    except ValueError:
                        continue
        return missing

    def _map_structure(self, project_path):
        structure = []
        try:
            for root, dirs, files in os.walk(project_path):
                dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
                rel_path = Path(root).relative_to(project_path)
                indent = '    ' * len(rel_path.parts)
                structure.append(f"{indent}📁 {Path(root).name}/")
                for f in files:
                    structure.append(f"{indent}    📄 {f}")
            return structure if structure else ["Nenhum arquivo encontrado"]
        except Exception as e:
            st.error(f"Erro no mapeamento quântico: {str(e)}")
            return []

    def _calculate_stats(self, project_path):
        stats = defaultdict(int)
        for root, dirs, files in os.walk(project_path):
            stats['Diretórios'] += len([d for d in dirs if d not in self.excluded_dirs])
            stats['Arquivos'] += len(files)
            stats['Arquivos Python'] += sum(1 for f in files if f.endswith('.py'))
        return stats

class QuantumLabPro:
    def __init__(self):
        self.simulator = Aer.get_backend('aer_simulator')
        self.circuit = None
        self.history = []
        self.examples = {
            'iniciante': self._exemplo_entrelacamento,
            'intermediario': self._exemplo_portas_controladas,
            'avancado': self._exemplo_algoritmo_grover
        }
        self.gate_map = {
            'h': {'name': 'Hadamard', 'function': self._aplicar_h},
            'x': {'name': 'Pauli-X', 'function': self._aplicar_x},
            'cx': {'name': 'CNOT', 'function': self._aplicar_cx},
            'rz': {'name': 'Rotação Z', 'function': self._aplicar_rz},
            'swap': {'name': 'Troca', 'function': self._aplicar_swap},
            'measure': {'name': 'Medição', 'function': self._aplicar_measure}
        }

    # Todos os métodos de aplicação de portas devem estar DENTRO desta classe
    def aplicar_porta(self, porta, *args, **kwargs):
        if porta not in self.gate_map:
            raise ValueError(f"Porta '{porta}' não suportada")
        try:
            self.gate_map[porta]['function'](*args, **kwargs)
        except Exception as e:
            error_msg = f"❌ Erro na porta {self.gate_map[porta]['name']}: {str(e)}"
            raise RuntimeError(error_msg)

    def _aplicar_h(self, target):
        """Aplica porta Hadamard"""
        self.circuit.h(target)
        self.history.append(f"🔧 Hadamard no qubit {target}")

    def _aplicar_x(self, target):
        """Aplica porta Pauli-X"""
        self.circuit.x(target)
        self.history.append(f"🔧 Pauli-X no qubit {target}")

    def _aplicar_cx(self, control, target):
        """Aplica porta CNOT"""
        self.circuit.cx(control, target)
        self.history.append(f"🔧 CNOT (ctrl: {control}, alvo: {target})")

    def _aplicar_rz(self, target, theta):
        """Aplica rotação Z"""
        self.circuit.rz(theta, target)
        self.history.append(f"🔧 Rotação Z (θ={theta:.2f}) no qubit {target}")

    def _aplicar_swap(self, qubit1, qubit2):
        """Aplica operação SWAP"""
        self.circuit.swap(qubit1, qubit2)
        self.history.append(f"🔧 SWAP entre {qubit1} e {qubit2}")

    def _aplicar_measure(self, target):
        """Realiza medição"""
        self.circuit.measure(target, target)
        self.history.append(f"📊 Medição no qubit {target}")      
        
    def _exemplo_entrelacamento(self):
        """Exemplo de circuito de entrelaçamento quântico"""
        self.criar_circuito(2)
        self.aplicar_porta('h', 0)
        self.aplicar_porta('cx', 0, 1)
        return "🔰 Circuito de Entrelaçamento Quântico (2 Qubits)"

    def _exemplo_portas_controladas(self):
        """Exemplo de portas controladas complexas"""
        self.criar_circuito(3)
        for qubit in range(3):
            self.aplicar_porta('h', qubit)
        self.aplicar_porta('cx', 0, 1)
        self.aplicar_porta('swap', 1, 2)
        return "⚡ Circuito de Portas Controladas (3 Qubits)"

    def _exemplo_algoritmo_grover(self):
        """Exemplo simplificado do algoritmo de Grover"""
        self.criar_circuito(4)
        for qubit in range(4):
            self.aplicar_porta('h', qubit)
            self.aplicar_porta('rz', qubit, np.pi/4)
        self.aplicar_porta('cx', 1, 0)
        self.aplicar_porta('cx', 3, 2)
        return "🌀 Algoritmo de Grover (4 Qubits)"

    def carregar_exemplo(self, nivel):
        """Carrega exemplos pré-configurados com tratamento de erro melhorado"""
        try:
            nivel = nivel.lower().strip()
            if nivel in self.examples:
                return self.examples[nivel]()
            raise KeyError(f"Exemplo '{nivel}' não encontrado")
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar exemplo: {str(e)}") from e

    # Métodos de exemplo mantidos conforme original...

    def criar_circuito(self, qubits=2):
        """Cria novo circuito quântico com verificação de entrada"""
        if not isinstance(qubits, int) or qubits < 1:
            raise ValueError("Número de qubits deve ser inteiro positivo")
        self.circuit = QuantumCircuit(qubits, qubits)
        self.history.append(f"🆕 Circuito criado com {qubits} qubits")
        return self.circuit

    def simular(self, shots=1024):
        try:
            if not self.circuit:
                raise ValueError("Nenhum circuito criado")
            
            # Verificação corrigida usando a classe Measure importada
            if not any(isinstance(op.operation, Measure) for op in self.circuit.data):
                self.circuit.measure_all()
            
            compiled = transpile(self.circuit, self.simulator)
            job = self.simulator.run(compiled, shots=shots)
            result = job.result()
            return result.get_counts()
            
        except Exception as e:
            error_msg = f"Erro na simulação: {str(e)}"
            if "measurements" in str(e).lower():
                error_msg += "\n⚠️ Adicione medições ao circuito!"
            raise RuntimeError(error_msg)
        
def gerar_comunicacao_modulos():
    try:
        for root, dirs, _ in os.walk(st.session_state.project_path):
            for d in dirs:
                dir_path = Path(root) / d
                init_file = dir_path / "__init__.py"
                
                if init_file.exists():
                    # Leitura com tratamento universal de encoding
                    with init_file.open('r', encoding='utf-8', errors='replace') as f:
                        conteudo = f.read()
                    
                    # Adiciona novo conteúdo
                    novo_conteudo = "# Comunicação automática\n"
                    for req in st.session_state.get('requirements', []):
                        pkg = req.split('==')[0].replace("-", "_")
                        novo_conteudo += f"from {pkg} import *\n"
                    
                    # Escrita com encoding universal
                    with init_file.open('w', encoding='utf-8', errors='replace') as f:
                        f.write(novo_conteudo + "\n" + conteudo)
        
        st.success("Rede de comunicação estabelecida com sucesso! 🌐")
    
    except Exception as e:
        st.error(f"Erro na comunicação: {str(e)}")
        st.markdown("""
        **Solução:**  
        1. Verifique arquivos com caracteres especiais
        2. Use apenas texto UTF-8 nos nomes e conteúdos
        3. Execute como administrador se for Windows
        """)
    
    except UnicodeEncodeError as e:
        st.error(f"Erro de encoding: {str(e)}")
        st.markdown("""
        **Solução:**  
        Adicione esta linha no início do seu arquivo Python:
        ```python
        # -*- coding: utf-8 -*-
        """)
    
    except Exception as e:
        st.error(f"Erro na comunicação: {str(e)}")

def mostrar_tutorial_avançado():
    with st.expander("🎓 Academia Quântica Pro", expanded=True):
        tab1, tab2, tab3 = st.tabs(["🧠 Teoria", "🛠️ Prática", "📈 Visualização"])
        
        with tab1:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("""
                ### Princípios Fundamentais
                - **Superposição Quântica**
                - **Emaranhamento de Qubits**
                - **Interferência Quântica**
                - **Teorema da Não-Clonagem**
                """)
                
            with col2:
                st.markdown("""
                ### 📚 Leis e Teoremas
                1. Equação de Schrödinger
                2. Princípio da Incerteza
                3. Algoritmo de Shor
                4. Protocolo BB84 (QKD)
                """)

        with tab2:
            with st.container(border=True):
                cols = st.columns(3)
                with cols[0]:
                    st.markdown("""
                    **Portas Básicas**
                    ```python
                    circuito.h(0)       # Hadamard
                    circuito.x(1)       # Pauli-X
                    circuito.cx(0, 1)   # CNOT
                    ```
                    """)
                with cols[1]:
                    st.markdown("""
                    **Portas Avançadas**
                    ```python
                    circuito.rz(np.pi/2, 0)  # Rotação Z
                    circuito.swap(0, 1)      # Troca
                    circuito.toffoli(0,1,2)  # CCNOT
                    ```
                    """)
                with cols[2]:
                    st.markdown("""
                    **Medições**
                    ```python
                    circuito.measure_all()
                    circuito.measure([0, 1], [0, 1])
                    ```
                    """)

        with tab3:
            st.markdown("""
            ### 📊 Técnicas de Visualização
            - Diagramas de Circuito
            - Histograma de Resultados
            - Estado de Amplitude dos Qubits
            """)
            if st.session_state.lab.circuit:
                st.plotly_chart(plot_histogram(st.session_state.lab.simular()))

def interface_principal_aprimorada():
    st.title("🚀 Quantum Code Manager Pro Ultimate")
    st.caption("⭐ Plataforma Integrada para Desenvolvimento Quântico e Clássico")

    if 'lab' not in st.session_state:
        st.session_state.update({
            'lab': QuantumLabPro(),
            'project_path': str(Path.cwd()),
            'analysis': None,
            'requirements': [],
            'selected_inits': []
        })

    with st.sidebar:
        st.header("⚙️ Navegação Principal")
        menu = st.radio("Ir para:", ["📂 Projetos", "⚛️ Quantum Lab", "🛠️ Utilitários", "🔍 Diagnóstico"], index=0)

    if menu == "📂 Projetos":
        mostrar_gerenciamento_projetos()
    elif menu == "⚛️ Quantum Lab":
        mostrar_laboratorio_quantico()
    elif menu == "🛠️ Utilitários":
        mostrar_utilitarios()
    elif menu == "🔍 Diagnóstico":
        mostrar_diagnostico_sistema()

def mostrar_gerenciamento_projetos():
    with st.container():
        st.header("📂 Gerenciamento de Projetos")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            new_path = st.text_input("Caminho do Projeto", value=st.session_state.project_path)
        with col2:
            if st.button("📁 Selecionar Diretório"):
                if selected := select_directory():
                    st.session_state.project_path = selected
                    st.rerun()

        if st.session_state.project_path:
            tab1, tab2 = st.tabs(["📦 Requirements.txt", "🧩 __init__.py"])
            
            with tab1:
                gerenciar_requirements()
            
            with tab2:
                gerenciar_inits()

def gerenciar_requirements():
    st.subheader("Gerenciamento de Dependências")
    
    with st.expander("🌳 Estrutura do Projeto", expanded=True):
        mostrar_arvore_diretorios()

    try:
        py_files = [
            str(p.relative_to(st.session_state.project_path))
            for p in Path(st.session_state.project_path).rglob('*.py')
            if p.is_file() and not any(part.startswith('.') for part in p.parts)
        ]
        selected_files = st.multiselect("Selecione os arquivos para análise:", py_files)
    except Exception as e:
        st.error(f"Erro ao listar arquivos: {str(e)}")
        selected_files = []

    if st.button("🔍 Analisar Dependências"):
        with st.spinner("Varrendo projeto..."):
            doctor = ProjectDoctor()
            st.session_state.analysis = doctor.perform_full_scan(st.session_state.project_path)
            st.session_state.requirements = doctor.analyze_project_dependencies(
                st.session_state.project_path,
                selected_files if selected_files else None
            )

    if st.session_state.get('requirements'):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📋 Dependências Detectadas")
            st.code("\n".join(st.session_state.requirements), language='text')
            
            if st.button("💾 Salvar Requirements.txt"):
                try:
                    req_path = Path(st.session_state.project_path)/"requirements.txt"
                    # Escrever com encoding UTF-8 e tratamento de BOM para Windows
                    with req_path.open('w', encoding='utf-8-sig', errors='replace') as f:
                        f.write("\n".join(st.session_state.requirements))
                    st.success(f"Arquivo salvo em: {req_path}")
                except Exception as e:
                    st.error(f"Erro ao salvar: {str(e)}")
        
        with col2:
            st.subheader("📦 Status das Instalações")
            verificar_instalacoes()

def verificar_instalacoes():
    installed = {pkg.key.lower(): pkg for pkg in pkg_resources.working_set}
    for req in st.session_state.requirements:
        if '==' in req:
            pkg, ver = req.split('==', 1)
            pkg = pkg.strip().lower()
            if pkg in installed:
                status = "✅" if installed[pkg].version == ver else "⚠️"
                st.markdown(f"{status} **{pkg}** (Exigido: `{ver}`, Instalado: `{installed[pkg].version}`)")
            else:
                st.markdown(f"❌ **{pkg}** (Pacote não instalado)")
                if st.button(f"📥 Instalar {pkg}", key=f"install_{pkg}"):
                    install_package(pkg)

def install_package(package):
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", package], capture_output=True, text=True)
        if result.returncode == 0:
            st.success(f"✅ {package} instalado com sucesso!")
        else:
            st.error(f"❌ Erro na instalação: {result.stderr}")
    except Exception as e:
        st.error(f"Erro crítico: {str(e)}")

def gerenciar_inits():
    st.subheader("🧩 Sistema de Comunicação Quântica (`__init__.py`)")
    
    project_path = Path(st.session_state.project_path)
    
    # Opção de seleção: pasta ou arquivo específico
    opcao_selecao = st.radio(
        "Selecione o tipo de análise:",
        ["📁 Pasta completa", "📄 Arquivo específico"],
        horizontal=True
    )
    
    if opcao_selecao == "📄 Arquivo específico":
        # Listar arquivos .py para seleção
        try:
            # Garante que não listamos os próprios __init__.py
            py_files = [
                str(p.relative_to(project_path))
                for p in project_path.rglob('*.py')
                if p.is_file() and p.name != '__init__.py' and not any(part.startswith('.') for part in p.parts)
            ]
            selected_files = st.multiselect(
                "Selecione os arquivos para análise:",
                sorted(py_files), # Ordenado para melhor UX
                help="Selecione arquivos Python específicos para gerar/atualizar o __init__.py em suas respectivas pastas."
            )
        except Exception as e:
            st.error(f"Erro ao listar arquivos: {str(e)}")
            selected_files = []
    else:
        selected_files = None
    
    # Opção de conteúdo do __init__.py
    conteudo_init = st.radio(
        "Tipo de conteúdo para __init__.py:",
        ["📦 Automático (com classes e imports)", "📭 Em branco"],
        horizontal=True
    )
    
    if st.button("🌀 Gerar Portais Quânticos", type="primary"):
        with st.spinner("Estabelecendo comunicação dimensional..."):
            automatico = (conteudo_init == "📦 Automático (com classes e imports)")
            if opcao_selecao == "📁 Pasta completa":
                # Processar toda a pasta
                gerar_inits_para_pasta(project_path, automatico)
            else:
                # Processar apenas arquivos selecionados
                if not selected_files:
                    st.error("Selecione pelo menos um arquivo!")
                else:
                    # Usamos um set para processar cada diretório apenas uma vez
                    diretorios_a_processar = set()
                    for rel_path in selected_files:
                        diretorios_a_processar.add((project_path / rel_path).parent)
                    
                    for dir_path in sorted(list(diretorios_a_processar)):
                        _gerar_e_escrever_init(dir_path, automatico)
            st.success("Operação de Geração de Portais Concluída!")
        
        # O rerun é opcional, pode ser removido se causar atualizações indesejadas
        # st.rerun()

def extrair_classes_principais(arquivo_path):
    """Extrai todas as classes de nível superior de um arquivo Python, mantendo a ordem original. (Sua função original, sem alterações)"""
    classes = []
    try:
        with open(arquivo_path, 'r', encoding='utf-8', errors='ignore') as f:
            tree = ast.parse(f.read())
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if hasattr(node, 'col_offset') and node.col_offset == 0:
                    classes.append(node.name)
                    
        seen = set()
        classes = [cls for cls in classes if not (cls in seen or seen.add(cls))]
        
    except Exception as e:
        st.warning(f"Não foi possível analisar {arquivo_path.name}: {e}")
    
    return classes

def _gerar_e_escrever_init(dir_path: Path, automatico: bool):
    """
    Função auxiliar corrigida. Gera o conteúdo para um __init__.py analisando
    TODOS os arquivos .py no diretório fornecido e depois escreve o arquivo.
    Isso resolve o problema de sobrescrita.
    """
    init_path = dir_path / "__init__.py"
    
    try:
        if automatico:
            conteudo = f"# 🌌 Portal Quântico para o módulo '{dir_path.name}'\n"
            conteudo += f"# Gerado por Quantum Code Manager em {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            todas_as_classes = []
            
            # Itera em todos os arquivos .py da pasta para agregar o conteúdo
            for py_file in sorted(dir_path.glob('*.py')):
                if py_file.name == '__init__.py':
                    continue
                
                modulo_nome = py_file.stem
                classes = extrair_classes_principais(py_file)
                
                if classes:
                    # Formata os imports em linhas separadas para melhor legibilidade
                    imports_formatados = ',\n    '.join(classes)
                    conteudo += f"from .{modulo_nome} import (\n    {imports_formatados}\n)\n\n"
                    todas_as_classes.extend(classes)
            
            if todas_as_classes:
                # Remove duplicados e ordena para o __all__
                exports_unicos = sorted(list(set(todas_as_classes)))
                exports_formatados = ',\n    '.join([f'"{cls}"' for cls in exports_unicos])
                conteudo += f"__all__ = [\n    {exports_formatados}\n]\n"
            else:
                conteudo += "# Nenhuma classe exportável encontrada nos módulos deste pacote.\n__all__ = []\n"
        
        else:
            # Conteúdo em branco
            conteudo = f"# Arquivo __init__.py gerado por Quantum Code Manager\n"
            conteudo += f"# 📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            conteudo += "__all__ = []\n"
        
        # Escreve o arquivo final com o conteúdo agregado
        with init_path.open('w', encoding='utf-8') as f:
            f.write(conteudo)
            
        st.write(f"✅ Portal Quântico gerado/atualizado em: `{init_path.relative_to(Path(st.session_state.project_path).parent)}`")

    except Exception as e:
        st.error(f"❌ Erro ao gerar portal em `{dir_path}`: {e}")


def gerar_inits_para_pasta(project_path: Path, automatico: bool):
    """
    Função corrigida para não usar dependências inexistentes.
    Ela agora encontra todas as pastas com arquivos .py e chama a função auxiliar.
    """
    st.write("🔎 Verificando toda a estrutura do projeto...")
    
    # Usa um set para encontrar todos os diretórios únicos que contêm arquivos .py
    diretorios_de_pacotes = set()
    for py_file in project_path.rglob('*.py'):
        # Ignora arquivos em pastas ocultas (como .venv, .git)
        if not any(part.startswith('.') for part in py_file.parts):
            diretorios_de_pacotes.add(py_file.parent)

    if not diretorios_de_pacotes:
        st.info("Nenhum diretório com arquivos Python (pacotes) encontrado para processar.")
        return

    st.write(f" blissful Encontrados {len(diretorios_de_pacotes)} diretórios de pacotes. Gerando portais...")

    for dir_path in sorted(list(diretorios_de_pacotes)):
        # Não gera __init__.py na pasta raiz do projeto
        if dir_path != project_path:
            _gerar_e_escrever_init(dir_path, automatico)
        
def install_requirements_safely(requirements_path):
    """Instala as dependências com tratamento de erros"""
    with st.status("Instalando dependências...", expanded=True) as status:
        try:
            # Usar pip atual para instalar
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_path)],
                capture_output=True,
                text=True,
                check=True
            )
            
            status.update(label="✅ Instalação concluída!", state="complete")
            st.code(result.stdout, language="text")
            
            return True
        except subprocess.CalledProcessError as e:
            status.update(label="❌ Erro na instalação", state="error")
            
            # Análise de erros comum
            error_msg = e.stderr.lower()
            if "not found" in error_msg:
                st.error("Arquivo requirements.txt não encontrado!")
            elif "no matching distribution" in error_msg:
                bad_pkg = re.search(r"no matching distribution found for (.+?)\s", error_msg)
                if bad_pkg:
                    st.error(f"Pacote não encontrado no PyPI: {bad_pkg.group(1)}")
            else:
                st.error(f"Erro desconhecido: {e.stderr}")
            
            return False
        
def scan_quantum_portals(project_path):
    """Varredura quântica avançada da estrutura do projeto"""
    quantum_map = defaultdict(list)
    missing_portals = []
    
    for root, dirs, files in os.walk(project_path):
        dirs[:] = [d for d in dirs if d not in {'venv', '.git', '__pycache__'}]
        
        current_dir = Path(root)
        rel_path = current_dir.relative_to(project_path)
        
        # Mapeamento de módulos
        for f in files:
            if f.endswith('.py') and f != '__init__.py':
                quantum_map[str(rel_path)].append(f[:-3])
                
        # Detecção de portais ausentes
        if not (current_dir / '__init__.py').exists() and rel_path != Path('.'):
            missing_portals.append(str(rel_path))
            
    return missing_portals, quantum_map

def generate_quantum_content(rel_path, module_map):
    """Gera código quântico de comunicação entre módulos"""
    imports = []
    modules = module_map.get(rel_path, [])
    
    # 1. Imports relativos automáticos
    if modules:
        imports.append("# Módulos locais\n")
        for module in modules:
            imports.append(f"from . import {module}  # Conexão local direta")
    
    # 2. Imports de dependências globais
    if st.session_state.get('requirements'):
        imports.append("\n# Dependências quânticas\n")
        for req in st.session_state.requirements:
            pkg = req.split('==')[0].replace("-", "_")
            imports.append(f"import {pkg}  # Portal universal")
    
    # 3. Interface unificada
    imports.append("\n# Interface quântica\n")
    imports.append("__all__ = [\n    " + ",\n    ".join([f'"{m}"' for m in modules]) + "\n]")
    
    # 4. Metadados quânticos
    imports.insert(0, f"# 🌌 Portal Quântico: {rel_path}\n")
    imports.append("\n# 🔄 Conexão temporal estabilizada")
    
    return '\n'.join(imports)

def criar_inits(diretorios):
    success = []
    errors = []
    
    for rel_path in diretorios:
        try:
            dir_path = Path(st.session_state.project_path) / rel_path
            init_file = dir_path / '__init__.py'
            
            # Garantir encoding UTF-8 com BOM se necessário
            with init_file.open('w', encoding='utf-8-sig') as f:
                f.write(generate_init_content(dir_path))
            
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                st.toast(f"📂 Criado diretório: {rel_path}")

            # Conteúdo quântico inicial
            conteudo = "# Portal de Entrada Quântica\n"
            conteudo += f"# Caminho: {rel_path}\n\n"
            conteudo += "__all__ = [\n    # Insira seus módulos quânticos aqui\n]\n"
            
            init_path.write_text(conteudo, encoding="utf-8")
            success.append(f"🌀 {rel_path}/__init__.py")
            
            # Atualização em tempo real
            st.session_state.selected_inits.append(rel_path)
            
        except Exception as e:
            errors.append(f"💥 {rel_path}: {str(e)}")
            st.error(f"Erro na criação de {rel_path}: {str(e)}")

    # Feedback visual dinâmico
    if success:
        st.success("Portais estabilizados com sucesso!")
        st.balloons()
        st.code("\n".join(success), language="python")
        
    if errors:
        st.error("Distorções temporais detectadas:")
        st.code("\n".join(errors), language="python")

def mostrar_arvore_diretorios():
    try:
        project_path = Path(st.session_state.project_path)
        paths = []
        
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if d not in {'venv', '.venv', '__pycache__'}]
            current_path = Path(root)
            rel_path = str(current_path.relative_to(project_path))
            
            paths.append({
                "id": rel_path,
                "label": current_path.name,
                "parent": str(current_path.parent.relative_to(project_path)) if rel_path != "." else "",
                "type": "folder"
            })
            
            for f in files:
                paths.append({
                    "id": f"{rel_path}/{f}",
                    "label": f,
                    "parent": rel_path,
                    "type": "file"
                })

        if paths:
            df = pd.DataFrame(paths)
            fig = px.treemap(
                df, 
                path=['parent', 'label'], 
                color='type',
                color_discrete_map={'folder': '#00FF88', 'file': '#FFFFFF'},
                height=600
            )
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Erro na visualização: {str(e)}")

def criar_inits(diretorios):
    """Cria arquivos __init__.py com conteúdo inteligente"""
    success = []
    errors = []
    
    for rel_path in diretorios:
        try:
            dir_path = Path(st.session_state.project_path) / rel_path
            init_path = dir_path / "__init__.py"
            
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
            
            # Gera conteúdo baseado nas dependências e estrutura do projeto
            conteudo = generate_init_content(dir_path)
            
            init_path.write_text(conteudo)
            success.append(f"📄 {rel_path}/__init__.py")
        except Exception as e:
            errors.append(f"❌ {rel_path}: {str(e)}")
    
    if success:
        st.success("Arquivos criados com sucesso:\n" + "\n".join(success))
    if errors:
        st.error("Erros encontrados:\n" + "\n".join(errors))

def generate_init_content(directory):
    """Gera conteúdo inteligente para __init__.py"""
    content = "# -*- coding: utf-8 -*-\n\n"
    content += f"# Módulo: {directory.name}\n"
    content += "# Gerado automaticamente pelo Quantum Code Manager\n\n"
    
    # 1. Imports relativos dos módulos locais
    py_files = [f for f in directory.glob("*.py") 
               if f.is_file() and f.name != "__init__.py"]
    
    if py_files:
        content += "# Módulos locais\n"
        for py_file in py_files:
            module_name = py_file.stem
            content += f"from . import {module_name}\n"
    
    # 2. __all__ com todos os módulos locais
    if py_files:
        content += "\n__all__ = [\n"
        content += ",\n".join([f"    '{f.stem}'" for f in py_files])
        content += "\n]\n"
    
    # 3. Metadados quânticos
    content += "\n# 🌌 Portal Quântico ativo\n"
    content += f"# 📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return content

def mostrar_laboratorio_quantico():
    with st.container():
        st.header("⚛️ Laboratório Quântico Pro")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            with st.form("controles_quanticos"):
                st.subheader("🔧 Controles Quânticos")
                
                # Sistema de exemplos com validação
                exemplo = st.selectbox(
                    "Exemplos Pré-configurados:",
                    ["Personalizado", "Iniciante", "Intermediário", "Avançado"],
                    help="Selecione um circuito pré-configurado para iniciar"
                )
                
                if st.form_submit_button("🎲 Carregar Exemplo", 
                                       help="Carrega o exemplo selecionado"):
                    try:
                        if exemplo != "Personalizado":
                            msg = st.session_state.lab.carregar_exemplo(exemplo.lower())
                            st.toast(f"✅ {msg}")
                    except Exception as e:
                        st.error(f"❌ Erro: {str(e)}")
                
                # Controle de portas com validação
                qubits = st.number_input("Número de Qubits", 2, 8, 2,
                                       help="Define o tamanho do circuito quântico")
                porta = st.selectbox("Porta Quântica", 
                                   list(st.session_state.lab.gate_map.keys()),
                                   format_func=lambda x: st.session_state.lab.gate_map[x]['name'])
                
                # Parâmetros dinâmicos
                params = {}
                if porta in ['cx', 'swap']:
                    params['control'] = st.number_input("Qubit de Controle", 0, qubits-1, 0,
                                                      help="Qubit que controla a operação")
                params['target'] = st.number_input("Qubit Alvo", 0, qubits-1, 0,
                                                 help="Qubit que recebe a operação")
                
                if porta == 'rz':
                    params['theta'] = st.slider("Ângulo θ (radianos)", 0.0, 2*np.pi, np.pi/2,
                                              help="Ângulo de rotação no eixo Z")
                
                # Botões de ação com feedback
                cols = st.columns(2)
                with cols[0]:
                    if st.form_submit_button("🔧 Aplicar Porta",
                                          help="Aplica a porta selecionada ao circuito"):
                        try:
                            st.session_state.lab.aplicar_porta(porta, **params)
                            st.toast("Porta aplicada com sucesso!")
                        except Exception as e:
                            st.error(f"Erro na porta {porta}: {str(e)}")
                with cols[1]:
                    if st.form_submit_button("🧹 Novo Circuito",
                                          help="Reinicia todo o circuito"):
                        st.session_state.lab = QuantumLabPro()
                        st.toast("Circuito reiniciado!")

        with col2:
            # Visualização do circuito com múltiplas opções
            if st.session_state.lab.circuit:
                with st.expander("🔎 Visualização do Circuito", expanded=True):
                    viz_type = st.radio("Tipo de Visualização:", 
                                      ["Matplotlib", "Texto", "Interativo"],
                                      horizontal=True)
                    
                    try:
                        if viz_type == "Matplotlib":
                            fig = st.session_state.lab.circuit.draw('mpl', style='clifford')
                            st.pyplot(fig)
                        elif viz_type == "Texto":
                            st.code(st.session_state.lab.circuit.draw('text'))
                        elif viz_type == "Interativo":
                            st.plotly_chart(plot_histogram(st.session_state.lab.simular(shots=1024)))
                    except Exception as e:
                        st.error(f"Erro na visualização: {str(e)}")
            
            # Sistema de simulação com progresso
            if st.button("⚡ Executar Simulação Quântica", 
                       help="Executa o circuito atual no simulador quântico"):
                with st.status("Executando simulação...", expanded=True) as status:
                    try:
                        progress_bar = st.progress(0)
                        result = st.session_state.lab.simular(shots=2048)
                        progress_bar.progress(100)
                        st.session_state.resultados = result
                        status.update(label="Simulação concluída!", state="complete")
                    except Exception as e:
                        status.update(label="Erro na simulação!", state="error")
                        st.error(str(e))
            
            # Visualização dos resultados
            if st.session_state.get('resultados'):
                with st.expander("📊 Análise dos Resultados", expanded=True):
                    tab1, tab2 = st.tabs(["Histograma", "Dados Brutos"])
                    with tab1:
                        fig = plot_histogram(st.session_state.resultados)
                        st.plotly_chart(fig, use_container_width=True)
                    with tab2:
                        st.json(st.session_state.resultados)

def mostrar_utilitarios():
    with st.container():
        st.header("🛠️ Central de Utilitários Avançados")
        
        col1, col2 = st.columns(2)
        with col1:
            # Terminal Integrado com exemplos
            with st.container(border=True):
                st.subheader("🖥️ Terminal Integrado")
                st.markdown("""
                **Exemplos de Uso:**
                ```bash
                # Instalar dependências
                pip install -r requirements.txt
                
                # Executar testes
                python -m pytest tests/
                
                # Iniciar servidor
                streamlit run app.py
                ```
                """)
                
                term_type = st.selectbox("Selecione o Terminal:", 
                                       ["CMD", "PowerShell", "Bash"])
                
                if st.button(f"▶️ Abrir {term_type}", 
                           help=f"Inicia o terminal {term_type} no diretório do projeto"):
                    try:
                        commands = {
                            "CMD": f"start cmd /K \"cd /D {st.session_state.project_path}\"",
                            "PowerShell": f"start powershell -NoExit -Command \"cd '{st.session_state.project_path}'\"",
                            "Bash": f"gnome-terminal -- bash -c \"cd '{st.session_state.project_path}'; exec bash\""
                        }
                        subprocess.Popen(commands[term_type], shell=True)
                    except Exception as e:
                        st.error(f"Erro ao abrir terminal: {str(e)}")

            # Ferramentas de Desenvolvimento
            with st.container(border=True):
                st.subheader("🔧 Kit de Desenvolvimento")
                if st.button("🌳 Visualizar Árvore de Dependências",
                           help="Mostra todas as dependências e suas relações"):
                    try:
                        result = subprocess.run([sys.executable, "-m", "pipdeptree"], 
                                              capture_output=True, text=True, 
                                              cwd=st.session_state.project_path)
                        st.code(result.stdout, language='text')
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")
                
                if st.button("🧹 Limpeza de Cache",
                           help="Remove arquivos temporários e caches"):
                    try:
                        clean_paths = [
                            Path(st.session_state.project_path)/"__pycache__",
                            Path(st.session_state.project_path)/".mypy_cache"
                        ]
                        for path in clean_paths:
                            if path.exists():
                                shutil.rmtree(path)
                        st.toast("✅ Cache limpo com sucesso!")
                    except Exception as e:
                        st.error(f"Erro na limpeza: {str(e)}")

        with col2:
            # Gestão de Ambientes Virtuais
            with st.container(border=True):
                st.subheader("🐍 Gestão de Ambientes")
                env_type = st.radio("Tipo de Ambiente:", ["venv", "conda"], horizontal=True)
                
                if st.button(f"➕ Criar Ambiente {env_type}",
                           help=f"Cria novo ambiente virtual usando {env_type}"):
                    try:
                        if env_type == "venv":
                            subprocess.run([sys.executable, "-m", "venv", ".venv"], 
                                          cwd=st.session_state.project_path)
                        else:
                            subprocess.run(["conda", "create", "--prefix", ".conda", "python=3.10", "-y"],
                                          cwd=st.session_state.project_path)
                        st.success(f"Ambiente {env_type} criado!")
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")
                
                if st.button("⚙️ Instalar Requirements.txt",
                           help="Instala todas as dependências do projeto"):
                    try:
                        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                                              capture_output=True, text=True,
                                              cwd=st.session_state.project_path)
                        st.code(result.stdout, language='text')
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

            # Integração com Ferramentas Externas
            with st.container(border=True):
                st.subheader("🔗 Integração com IDEs")
                cols = st.columns(2)
                with cols[0]:
                    if st.button("⌨️ Abrir VS Code",
                               help="Abre o projeto no Visual Studio Code"):
                        try:
                            subprocess.Popen(f"code \"{st.session_state.project_path}\"", shell=True)
                        except:
                            st.error("VS Code não encontrado!")
                with cols[1]:
                    if st.button("📊 Abrir Jupyter",
                               help="Inicia um servidor Jupyter Notebook"):
                        try:
                            subprocess.Popen("jupyter notebook", 
                                           cwd=st.session_state.project_path, 
                                           shell=True)
                        except:
                            st.error("Jupyter não instalado!")

            with st.container(border=True):
                st.subheader("🚀 Automação de Deployment")
                
                # Criar run.bat
                if st.button("🛠️ Criar run.bat", help="Gera arquivo batch para execução automática"):
                    try:
                        project_path = Path(st.session_state.project_path)
                        bat_path = project_path / "run.bat"
                        script_name = os.path.basename(__file__)
                        
                        bat_content = f"""@echo off
call venv\\Scripts\\activate
streamlit run {script_name}
pause
"""
                        bat_path.write_text(bat_content, encoding="utf-8")
                        st.success(f"✅ run.bat criado em: {bat_path}")
                        st.code(bat_content, language="bat")
                    except Exception as e:
                        st.error(f"❌ Erro ao criar arquivo: {str(e)}")
                
                # Converter para EXE
                if st.button("📦 Gerar Executável", help="Cria versão .exe do projeto usando PyInstaller"):
                    try:
                        import PyInstaller
                    except ImportError:
                        with st.status("Instalando PyInstaller...") as status:
                            try:
                                subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
                                status.update(label="PyInstaller instalado!", state="complete")
                            except Exception as e:
                                status.update(label="Erro na instalação!", state="error")
                                st.error(str(e))
                                return
                    
                    with st.status("Criando executável...", expanded=True) as status:
                        try:
                            script_path = Path(__file__).resolve()
                            cmd = f"pyinstaller --onefile --name QuantumApp {script_path}"
                            
                            result = subprocess.run(cmd.split(), 
                                                  cwd=st.session_state.project_path,
                                                  capture_output=True,
                                                  text=True)
                            
                            if result.returncode == 0:
                                exe_path = Path(st.session_state.project_path)/"dist"/"QuantumApp.exe"
                                status.update(label=f"✅ EXE criado em: {exe_path}", state="complete")
                                st.code(result.stdout, language="text")
                            else:
                                status.update(label="❌ Erro na compilação", state="error")
                                st.error(result.stderr)
                        except Exception as e:
                            st.error(f"Falha crítica: {str(e)}")

        mostrar_tutorial_avançado()

def mostrar_diagnostico_sistema():
    inspector = SystemInspector()
    
    with st.container():
        st.header("🔍 Diagnóstico Completo do Sistema Quântico")
        st.caption("📊 Análise em tempo real do ambiente de desenvolvimento")

        # Seção de Hardware
        with st.expander("🖥️ Telemetria do Sistema", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                cpu_usage = psutil.cpu_percent()
                st.metric("Utilização da CPU", f"{cpu_usage}%")
                st.progress(cpu_usage/100)
                
            with col2:
                mem = psutil.virtual_memory()
                st.metric("Memória Disponível", f"{mem.available / (1024**3):.1f} GB")
                st.progress(mem.percent/100)
            
            st.markdown("### 📋 Especificações Técnicas")
            sys_report = inspector.get_detailed_report()
            for key, value in sys_report.items():
                st.markdown(f"**{key}:** `{value}`")

        # Seção de Ferramentas
        with st.expander("🧰 Ferramentas Essenciais", expanded=True):
            tools = {
                'PowerShell': 'pwsh --version',
                'Git': 'git --version',
                'Python': 'python --version',
                'Pip': 'pip --version'
            }
            
            cols = st.columns(3)
            for i, (tool, cmd) in enumerate(tools.items()):
                with cols[i % 3]:
                    try:
                        output = subprocess.check_output(cmd.split(), stderr=subprocess.STDOUT, text=True)
                        version = output.split('\n')[0]
                        st.success(f"✅ **{tool}**\n`{version}`")
                    except Exception:
                        st.error(f"❌ **{tool} Não Instalado**")
                        st.markdown(f"[🔗 Instalar {tool}](https://www.google.com/search?q=install+{tool.lower()})")

        # Seção de Pacotes Python
        with st.expander("🐍 Pacotes Python", expanded=True):
            packages = ['streamlit', 'qiskit', 'numpy', 'pandas', 'matplotlib', 'seaborn']
            cols = st.columns(3)
            
            for i, pkg in enumerate(packages):
                with cols[i % 3]:
                    try:
                        version = pkg_resources.get_distribution(pkg).version
                        st.success(f"✅ **{pkg}**\n`v{version}`")
                    except Exception:
                        st.error(f"❌ **{pkg} Não Instalado**")
                        st.code(f"pip install {pkg}", language='bash')

        # Seção de Otimizações
        with st.expander("🚀 Recomendações de Otimização", expanded=True):
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            
            cols = st.columns(2)
            with cols[0]:
                st.markdown("### 🔧 Ajustes de Performance")
                if cpu > 80:
                    st.error("**CPU Sobrecarregada**")
                    st.markdown("""
                    - Fechar aplicativos desnecessários
                    - Considerar upgrade de hardware
                    - Otimizar circuitos quânticos""")
                else:
                    st.success("Performance da CPU dentro do esperado ✅")
                    
            with cols[1]:
                st.markdown("### 🛠️ Gestão de Memória")
                if mem.percent > 80:
                    st.error("**Memória Insuficiente**")
                    st.markdown("""
                    - Aumentar memória virtual
                    - Reduzir uso de datasets grandes
                    - Reiniciar aplicativos pesados""")
                else:
                    st.success("Uso de memória adequado ✅")

            if any("❌" in status for status in tools.values()):
                with st.expander("🔧 Soluções Recomendadas", expanded=True):
                    tab_win, tab_linux, tab_mac = st.tabs(["Windows", "Linux", "macOS"])
                    
                    with tab_win:
                        st.markdown("""
                        ```powershell
                        # Instalar PowerShell
                        winget install --id Microsoft.PowerShell --source winget

                        # Instalar Python
                        winget install Python.Python.3.12

                        # Instalar Git
                        winget install Git.Git
                        """)
                    
                    with tab_linux:
                        st.markdown("""
                        ```bash
                        # Ubuntu/Debian
                        sudo apt update && sudo apt install -y \
                            python3 \
                            python3-pip \
                            git \
                            powershell

                        # Fedora
                        sudo dnf install -y \
                            python3 \
                            python3-pip \
                            git \
                            powershell
                        """)
                    
                    with tab_mac:
                        st.markdown("""
                        ```bash
                        # Usando Homebrew
                        brew install python git
                        brew install --cask powershell

                        # Verificar instalações
                        python3 --version
                        pip3 --version
                        """)

        # Verificação de Pacotes Python com ações
        with st.container(border=True):
            st.subheader("🐍 Ecossistema Python")
            required = ['streamlit', 'qiskit', 'numpy', 'pandas', 'plotly', 'matplotlib', 'seaborn']
            status_map = {}
            
            for pkg in required:
                try:
                    version = pkg_resources.get_distribution(pkg).version
                    status_map[pkg] = ('✅', version)
                except Exception:
                    status_map[pkg] = ('❌', 'N/I')

            cols = st.columns(3)
            for i, (pkg, (status, ver)) in enumerate(status_map.items()):
                with cols[i % 3]:
                    st.markdown(f"""
                    <div style="margin: 0.5rem 0; padding: 0.5rem; 
                                border: 1px solid {'#00ff88' if status == '✅' else '#ff0000'}; 
                                border-radius: 8px;">
                        <div style="display: flex; justify-content: space-between;">
                            <strong>{pkg}</strong>
                            <span style="color: {'#00ff88' if status == '✅' else '#ff0000'}">{status}</span>
                        </div>
                        <div style="color: #888; font-size: 0.8em;">Versão: {ver}</div>
                    </div>
                    """, unsafe_allow_html=True)

            if any(status == '❌' for (status, _) in status_map.values()):
                st.warning("Algumas dependências estão faltando!")
                if st.button("📥 Instalar Todas as Dependências Python", 
                           help="Instala todos os pacotes necessários", 
                           type="secondary"):
                    try:
                        with st.status("Instalando pacotes...", expanded=True) as status:
                            result = subprocess.run([sys.executable, "-m", "pip", "install"] + required,
                                                  capture_output=True, text=True)
                            status.update(label="Instalação completa!", state="complete")
                            st.code(result.stdout, language='text')
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro crítico: {str(e)}")

        # Otimizações recomendadas
        with st.container(border=True):
            st.subheader("🚀 Otimizações Recomendadas")
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory()
            
            cols = st.columns(2)
            with cols[0]:
                st.markdown("### 🔧 Ajustes de Performance")
                if cpu > 80:
                    st.error("**CPU Sobrecarregada** - Considere:")
                    st.markdown("- Fechar aplicativos desnecessários\n- Upgrade do hardware\n- Otimizar algoritmos quânticos")
                else:
                    st.success("Performance da CPU dentro do esperado")
                    
            with cols[1]:
                st.markdown("### 🛠️ Configuração de Ambiente")
                if mem.percent > 80:
                    st.error("**Memória Limitada** - Ações sugeridas:")
                    st.markdown("- Aumentar memória swap\n- Reduzir consumo de aplicativos\n- Usar datasets menores")
                else:
                    st.success("Uso de memória adequado")
                    
class QuantumModuleManager:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.excluded_dirs = {'venv', '.venv', '__pycache__', '.git', 'env'}
        
    def scan_project_modules(self):
        """Varre o projeto e retorna estrutura de módulos"""
        module_map = {}
        missing_inits = []
        
        for root, dirs, files in os.walk(self.project_path):
            # Remove diretórios excluídos
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            current_dir = Path(root)
            rel_path = current_dir.relative_to(self.project_path)
            
            # Verifica se é um pacote Python (tem __init__.py)
            is_package = (current_dir / "__init__.py").exists()
            
            # Mapeia os módulos
            modules = [f[:-3] for f in files if f.endswith('.py') and f != '__init__.py']
            
            if modules or is_package:
                module_map[str(rel_path)] = {
                    'is_package': is_package,
                    'modules': modules,
                    'path': current_dir
                }
            
            # Verifica se precisa de __init__.py
            if not is_package and rel_path != Path('.') and modules:
                missing_inits.append(str(rel_path))
                
        return module_map, missing_inits
    
    def create_quantum_portal(self, rel_path, module_map):
        """Cria um arquivo __init__.py com comunicação quântica"""
        portal_path = self.project_path / rel_path
        init_file = portal_path / "__init__.py"
        
        # Conteúdo base
        content = generate_init_content(portal_path)
        
        # Adiciona imports de dependências
        if 'requirements' in st.session_state:
            content += "\n# Dependências quânticas\n"
            for req in st.session_state.requirements:
                pkg = req.split('==')[0].replace("-", "_")
                content += f"try:\n    import {pkg}\nexcept ImportError:\n    pass\n\n"
        
        # Adiciona comunicação com módulos filhos
        child_modules = self._find_child_modules(rel_path, module_map)
        if child_modules:
            content += "\n# Comunicação dimensional\n"
            for child in child_modules:
                content += f"from . import {child}\n"
        
        # Escreve o arquivo
        init_file.write_text(content, encoding='utf-8')
        return init_file
    
    def _find_child_modules(self, rel_path, module_map):
        """Encontra módulos filhos diretos"""
        children = []
        parent_path = Path(rel_path)
        
        for module_path in module_map:
            if Path(module_path).parent == parent_path:
                children.append(Path(module_path).name)
                
        return children

if __name__ == "__main__":
    # Configuração inicial de dependências
    try:
        required_packages = ['streamlit', 'qiskit', 'numpy', 'pandas', 'plotly']
        missing = []
        
        for pkg in required_packages:
            try:
                importlib.import_module(pkg.split('-')[0].replace(' ', '_'))
            except ImportError:
                missing.append(pkg)
        
        if missing:
            with st.status("Instalando dependências faltantes...") as status:
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install"] + missing, check=True)
                    status.update(label="Instalação concluída!", state="complete")
                    st.rerun()
                except subprocess.CalledProcessError as e:
                    status.update(label="Erro na instalação!", state="error")
                    st.error(f"Falha crítica: {str(e)}")
                    st.stop()
        
        interface_principal_aprimorada()
    except Exception as e:
        st.error(f"ERRO INICIALIZADOR: {str(e)}")
        st.stop()