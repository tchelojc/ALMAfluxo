# ======================================================================================
# CONFIGURAÇÕES GLOBAIS E SUPORTE A VÍDEO (MODIFICADO)
# ======================================================================================

import os
import subprocess
import importlib.util
import warnings

# Suprimir avisos específicos do MoviePy e outros
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", module="moviepy")

# Estado padrão
DEFAULT_STATE = {
    'base_image': None,
    'video_clip': None,
    'processed_image': None,
    'processed_video_clip': None,
    'theme': "Claro",
    'performance_mode': True,
    'uploaded_file_id': None,
    'export_data': None,
    'export_file': "filtro_config.json",
    'export_mime': "application/json",
    'sound_cache': {},
    'last_processed': None,
    'text_image': None,
    'modular_exports': [],
    'file_export_data': None,
    'file_export_name': None,
    'custom_font': None,
    'video_warning_shown': False  # Adicionado para controlar avisos
}

MAX_IMAGE_PIXELS = 5000 * 5000

# ======================================================================================
# IMPORTS ESSENCIAIS (MODIFICADO)
# ======================================================================================

try:
    import streamlit as st
    from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps, ImageColor, ImageFont
    import numpy as np
    import io
    import base64
    import requests
    import random
    import math
    import pygame
    import tempfile
    import time
    import cv2
    from typing import Dict, Any, List, Tuple, Optional, Union
    from io import BytesIO
    import json
    from importlib.metadata import version, PackageNotFoundError
    from packaging.version import parse as parse_version
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    
    # Tentativa silenciosa de importar VideoFileClip
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from moviepy.editor import VideoFileClip
            VIDEO_SUPPORT = True
    except ImportError:
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                from moviepy.video.io.VideoFileClip import VideoFileClip
                VIDEO_SUPPORT = True
        except ImportError:
            VIDEO_SUPPORT = False

except ImportError as e:
    st.error(f"Erro ao importar bibliotecas essenciais: {e}")
    st.stop()

# ======================================================================================
# SUPORTE A VÍDEO COM FFMPEG + MOVIEPY (MODIFICADO)
# ======================================================================================
def check_video_support() -> bool:
    """Verifica o suporte a vídeo sem mostrar avisos"""
    try:
        # Tentativa silenciosa de importar as dependências
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            import moviepy.editor
            import imageio_ffmpeg
            
            # Verifica se o FFmpeg está disponível
            try:
                ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
                if ffmpeg_path and os.path.exists(ffmpeg_path):
                    return True
                
                # Fallback: verifica se o ffmpeg está no PATH
                try:
                    subprocess.run(["ffmpeg", "-version"], 
                                 check=True, 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
                    return True
                except:
                    return False
            except:
                return False
    except ImportError:
        return False

# Configuração inicial sem avisos
VIDEO_SUPPORT = check_video_support()

# Configuração silenciosa do MoviePy se suporte estiver disponível
if VIDEO_SUPPORT:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            from moviepy.config import change_settings
            import imageio_ffmpeg
            
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            if ffmpeg_path:
                change_settings({"FFMPEG_BINARY": ffmpeg_path})
    except:
        pass
    
def initialize_video_support() -> bool:
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        
        # Verificação mais robusta do executável FFmpeg
        if not os.path.exists(ffmpeg_path):
            # Tentar encontrar o FFmpeg no PATH do sistema
            try:
                ffmpeg_path = 'ffmpeg'  # Tenta usar o comando direto
                subprocess.run([ffmpeg_path, '-version'], check=True, capture_output=True)
            except:
                return False
        
        # Configuração explícita para moviepy
        try:
            from moviepy.config import change_settings
        except ImportError:
            # Para versões mais recentes do MoviePy
            from moviepy.config_defaults import change_settings
        change_settings({"FFMPEG_BINARY": ffmpeg_path})
        
        return True
    except Exception as e:
        print(f"Erro ao inicializar suporte a vídeo: {str(e)}")
        return False

# Garante que VIDEO_SUPPORT esteja pronto ANTES de construir a interface
VIDEO_SUPPORT = initialize_video_support()

def check_module_installed(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None

def find_ffmpeg() -> Optional[str]:
    try:
        if check_module_installed("imageio_ffmpeg"):
            import imageio_ffmpeg
            path = imageio_ffmpeg.get_ffmpeg_exe()
            if os.path.exists(path):
                return path

        common_paths = [
            'ffmpeg',
            '/usr/bin/ffmpeg',
            '/usr/local/bin/ffmpeg',
            'C:\\ffmpeg\\bin\\ffmpeg.exe',
        ]

        for path in common_paths:
            if os.path.exists(path):
                return path

        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
            if result.returncode == 0:
                return 'ffmpeg'
        except Exception:
            pass

        return None
    except Exception as e:
        st.warning(f"Erro ao buscar FFmpeg: {e}")
        return None

def test_ffmpeg(path: str) -> bool:
    try:
        result = subprocess.run([path, '-version'], capture_output=True, text=True)
        return result.returncode == 0 and 'ffmpeg version' in result.stdout
    except Exception as e:
        st.warning(f"Erro ao testar FFmpeg: {e}")
        return False

try:
    # Verifica se MoviePy está disponível
    try:
        from moviepy.editor import VideoFileClip
        has_moviepy = True
    except ImportError:
        has_moviepy = False

    # Verifica se imageio-ffmpeg está disponível
    try:
        import imageio_ffmpeg
        has_imageio_ffmpeg = True
    except ImportError:
        has_imageio_ffmpeg = False

    if has_moviepy and has_imageio_ffmpeg:
        ffmpeg_path = find_ffmpeg()

        if ffmpeg_path and test_ffmpeg(ffmpeg_path):
            os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

            test_file = os.path.join('media', 'test.mp4')
            if os.path.exists(test_file):
                try:
                    with VideoFileClip(test_file, audio=False) as clip:
                        if clip.duration > 0:
                            st.success("🎥 Suporte a vídeo ATIVADO com MoviePy + FFmpeg.")
                            VIDEO_SUPPORT = True
                except Exception as test_error:
                    st.warning(f"⚠️ MoviePy não conseguiu abrir o vídeo de teste: {test_error}")
                    VIDEO_SUPPORT = True  # FFmpeg funcional, mas vídeo pode estar corrompido
            else:
                st.info("ℹ️ FFmpeg está funcional, mas o arquivo de teste não foi encontrado.")
                VIDEO_SUPPORT = True
        else:
            st.warning("⚠️ FFmpeg não encontrado ou não funcional.")
            VIDEO_SUPPORT = False

except Exception as e:
    st.error(f"❌ Erro na configuração de vídeo: {e}")
    VIDEO_SUPPORT = False

# ======================================================================================
# TIPO DE VÍDEO SUPORTADO
# ======================================================================================

SUPPORTED_VIDEO_TYPES = {
    'video/mp4': 'mp4',
    'video/quicktime': 'mov',
    'video/x-msvideo': 'avi',
    'video/x-matroska': 'mkv',
    'video/webm': 'webm'
}

def is_video_supported(file_type: str) -> bool:
    return file_type in SUPPORTED_VIDEO_TYPES

# --- Configuração da Página ---
st.set_page_config(
    page_title="🔥 Criador de Filtros Pro - Super Edition",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/seuuser/filtros-pro',
        'Report a bug': "https://github.com/seuuser/filtros-pro/issues",
        'About': "### Ferramenta profissional para criação de filtros e efeitos visuais"
    }
)

def update_theme():
    """Callback para atualizar o tema no session_state."""
    st.session_state.theme = st.session_state.theme_selector

def check_library_versions():
    """Verifica as versões das bibliotecas principais de forma robusta."""
    required = {
        'Pillow': ('9.0.0', '8.0.0'),
        'numpy': ('1.21.0', '1.19.0'),
        'opencv-python': ('4.5.0', '4.2.0'),
        'streamlit': ('1.12.0', '1.0.0'),
        'moviepy': ('1.0.0', '0.2.0'),
        'imageio-ffmpeg': ('0.4.0', '0.3.0')
    }
    issues = []
    for lib, (recommended, minimum) in required.items():
        try:
            installed = version(lib)
            if parse_version(installed) < parse_version(minimum):
                issues.append(f"❌ {lib} v{installed} é incompatível (mínimo: v{minimum})")
            elif parse_version(installed) < parse_version(recommended):
                issues.append(f"⚠️ {lib} v{installed} pode ser atualizada (recomendado: v{recommended})")
        except PackageNotFoundError:
            issues.append(f"❌ Biblioteca essencial '{lib}' não encontrada. Instale-a.")
    return issues

# Exibe avisos de dependência na barra lateral se houver problemas.
dependency_issues = check_library_versions()
if dependency_issues:
    with st.sidebar.expander("⚠️ Aviso de Dependências", expanded=True):
        for issue in dependency_issues:
            st.warning(issue)

try:
    ctx = get_script_run_ctx()
    if ctx:
        ctx.uploaded_file_mgr._max_file_size = 200  # Em MB
except Exception:
    st.warning("Não foi possível aumentar o limite de upload. Considere usar um arquivo config.toml.")
    
# ======================================================================================
# BANCO DE DADOS DE EFEITOS SUPER COMPLETO
# ======================================================================================
class QualitySettings:
    """Configurações de qualidade para exportação"""
    PRESETS = {
        "Baixa": {"quality": 70, "subsampling": 2, "crf": 28, "scale": 0.5},
        "Média": {"quality": 85, "subsampling": 1, "crf": 23, "scale": 0.75},
        "Alta": {"quality": 95, "subsampling": 0, "crf": 18, "scale": 1.0},
        "Máxima": {"quality": 100, "subsampling": 0, "crf": 14, "scale": 1.0}
    }
    
    @staticmethod
    def get_preset(name: str) -> Dict[str, Any]:
        return QualitySettings.PRESETS.get(name, QualitySettings.PRESETS["Alta"])
    
    @staticmethod
    def get_preset_options():
        """Retorna opções formatadas para exibição"""
        return [
            f"{name} ({QualitySettings.PRESETS[name]['quality']}%)" 
            for name in QualitySettings.PRESETS
        ]
    
class EffectDatabase:
    """Classe para gerenciar todos os efeitos disponíveis"""
    
    SOUND_EFFECTS = {
        "glass_break": {
            "online": "https://assets.mixkit.co/sfx/preview/mixkit-breaking-glass-2581.mp3",
            "description": "Som de vidro quebrando"
        },
        "water_drops": {
            "online": "https://assets.mixkit.co/sfx/preview/mixkit-water-drops-1903.mp3",
            "description": "Som de gotas d'água"
        }
    }

    FRAME_DATABASE = {
        "Nenhuma": {
            "desc": "Sem moldura",
            "params": {},
            "icon": "❌"
        },
        "Janela": {
            "desc": "Moldura de janela com divisórias",
            "params": {
                "estilo": ["Simples", "Clássico", "Vitral"],
                "cor_padrao": "#FFFFFF",
                "min_espessura": 5,
                "max_espessura": 50,
                "dica": "💡 Ideal para fotos de arquitetura e paisagens urbanas"
            },
            "icon": "🪟"
        },
        "Câmera": {
            "desc": "Moldura de câmera fotográfica vintage",
            "params": {
                "estilo": ["Polaroid", "DSLR", "Vintage"],
                "cor_padrao": "#C0C0C0",
                "min_espessura": 10,
                "max_espessura": 80,
                "dica": "💡 Perfeito para fotos antigas ou efeitos retro"
            },
            "icon": "📷"
        },
        "Lupa": {
            "desc": "Efeito de lupa com borda circular",
            "params": {
                "estilo": ["Simples", "Científica", "Vintage"],
                "cor_padrao": "#000000",
                "min_espessura": 15,
                "max_espessura": 100,
                "dica": "💡 Destaque detalhes específicos da imagem"
            },
            "icon": "🔍"
        },
        "Smartphone": {
            "desc": "Moldura de smartphone moderno",
            "params": {
                "estilo": ["iPhone", "Android", "Notch"],
                "cor_padrao": "#000000",
                "min_espessura": 20,
                "max_espessura": 120,
                "dica": "💡 Simule screenshots ou conteúdo para redes sociais"
            },
            "icon": "📱"
        },
        "Portal": {
            "desc": "Efeito de portal dimensional futurístico",
            "params": {
                "estilo": ["Sci-fi", "Mágico", "Glitch"],
                "cor_padrao": "#00FFFF",
                "min_espessura": 10,
                "max_espessura": 150,
                "dica": "💡 Combine com filtros futurísticos para efeito máximo"
            },
            "icon": "🌀"
        },
        "Neon": {
            "desc": "Moldura com efeito de luz neon",
            "params": {
                "estilo": ["Simples", "Pulsante", "RGB"],
                "cor_padrao": "#FF00FF",
                "min_espessura": 5,
                "max_espessura": 30,
                "dica": "💡 Excelente para designs modernos e chamativos"
            },
            "icon": "💡"
        }
    }

    FILTER_DATABASE = {
        "Vintage": {
            "desc": "Efeito sépia com vinheta",
            "example": "https://example.com/vintage_example.jpg",
            "params": {
                "intensidade": {"min": 0, "max": 100, "default": 70, "step": 1},
                "vinheta": {"min": 0, "max": 100, "default": 40, "step": 1},
                "granulacao": {"min": 0, "max": 50, "default": 10, "step": 1}
            },
            "combinations": ["Azulado", "Esverdeado", "Preto e Branco"],
            "icon": "🟤"
        },
        "Azulado": {
            "desc": "Tom frio azulado",
            "params": {
                "intensidade": {"min": 0, "max": 100, "default": 50, "step": 1},
                "brilho": {"min": -20, "max": 20, "default": 0, "step": 1},
                "matiz": {"min": -10, "max": 10, "default": 0, "step": 1}
            },
            "combinations": ["Vintage", "Futurístico"],
            "icon": "🔵"
        },
        "Esverdeado": {
            "desc": "Tom esverdeado cinematográfico",
            "params": {
                "intensidade": {"min": 0, "max": 100, "default": 50, "step": 1},
                "contraste": {"min": 0.5, "max": 1.5, "default": 1.1, "step": 0.1},
                "sombra": {"min": -20, "max": 20, "default": 0, "step": 1}
            },
            "combinations": ["Vintage", "Preto e Branco"],
            "icon": "🟢"
        },
        "Futurístico": {
            "desc": "Efeito cyberpunk com brilho",
            "params": {
                "glow": {"min": 0, "max": 100, "default": 30, "step": 1},
                "neon": {"min": 0, "max": 100, "default": 20, "step": 1},
                "scanlines": {"min": 0, "max": 50, "default": 0, "step": 1}
            },
            "combinations": ["Azulado", "Realça Cores"],
            "icon": "👾"
        },
        "Realça Cores": {
            "desc": "Aumenta a saturação das cores",
            "params": {
                "intensidade": {"min": 0.5, "max": 3.0, "default": 1.5, "step": 0.1},
                "seletividade": {"min": 0, "max": 100, "default": 50, "step": 1}
            },
            "combinations": ["Futurístico", "Vintage"],
            "icon": "🌈"
        },
        "Preto e Branco": {
            "desc": "Efeito monocromático avançado",
            "params": {
                "contraste": {"min": 0.5, "max": 2.0, "default": 1.2, "step": 0.1},
                "tons": {"min": 0, "max": 100, "default": 50, "step": 1},
                "textura": {"min": 0, "max": 30, "default": 0, "step": 1}
            },
            "combinations": ["Vintage", "Esverdeado"],
            "icon": "⚫"
        },
        "Infravermelho": {
            "desc": "Efeito de fotografia infravermelha",
            "params": {
                "intensidade": {"min": 0, "max": 100, "default": 50, "step": 1},
                "brilho": {"min": -30, "max": 30, "default": 0, "step": 1}
            },
            "combinations": ["Preto e Branco", "Futurístico"],
            "icon": "📡"
        },
        "Neon Dream": {
            "desc": "Efeito neon com cores vibrantes e brilho intenso",
            "params": {
                "intensidade": {"min": 0, "max": 100, "default": 70},
                "brilho": {"min": 0, "max": 100, "default": 50},
                "saturação": {"min": 0, "max": 150, "default": 120}
            },
            "combinations": ["Futurístico", "Glitch"],
            "icon": "💡"
        },
        "Vaporwave": {
            "desc": "Estético retrô com tons pastel e gradientes",
            "params": {
                "intensidade": {"min": 0, "max": 100, "default": 80},
                "matiz": {"min": -30, "max": 30, "default": 0}
            },
            "combinations": ["Azulado", "Realça Cores"],
            "icon": "🌌"
        },
        "Sobreposição": {
            "desc": "Camada colorida semi-transparente",
            "params": {
                "cor": {"type": "color", "default": "#FF0000"},
                "opacidade": {"min": 0.0, "max": 1.0, "default": 0.5, "step": 0.05}
            },
            "combinations": ["Vintage", "Azulado", "Esverdeado"],
            "icon": "🎨"
        }
    }

    ANIMATION_DATABASE = {
        "Girar": {
            "desc": "Rotação da tela em 360°",
            "params": {
                "direcao": ["Horário", "Anti-horário"],
                "velocidade": {"min": 1, "max": 10, "default": 5, "step": 1},
                "eixo": ["XY", "X", "Y", "Z"]
            },
            "complexity": 1,
            "icon": "🔄"
        },
        "Zoom": {
            "desc": "Efeito de zoom in/out dinâmico",
            "params": {
                "tipo": ["In", "Out", "Pulsar", "Aleatório"],
                "intensidade": {"min": 1, "max": 5, "default": 2, "step": 1},
                "suavidade": {"min": 1, "max": 10, "default": 5, "step": 1}
            },
            "complexity": 1,
            "icon": "🔍"
        },
        "Deslizar": {
            "desc": "Transição lateral suave",
            "params": {
                "direcao": ["Esquerda", "Direita", "Cima", "Baixo", "Diagonal"],
                "suavidade": {"min": 1, "max": 10, "default": 5, "step": 1},
                "tipo": ["Linear", "Acelerado", "Desacelerado"]
            },
            "complexity": 2,
            "icon": "↔️"
        },
        "Piscar": {
            "desc": "Efeito de piscar rápido",
            "params": {
                "vezes": {"min": 1, "max": 10, "default": 3, "step": 1},
                "velocidade": {"min": 1, "max": 5, "default": 3, "step": 1},
                "intensidade": {"min": 1, "max": 100, "default": 50, "step": 1}
            },
            "complexity": 1,
            "icon": "✨"
        },
        "Pixelar": {
            "desc": "Transição de pixelização criativa",
            "params": {
                "tamanho": {"min": 1, "max": 20, "default": 10, "step": 1},
                "direcao": ["In", "Out", "Aleatória"],
                "estilo": ["Bloco", "Ponto", "Linha"]
            },
            "complexity": 2,
            "icon": "🧊"
        },
        "Vidro Quebrando": {
            "desc": "Efeito de vidro quebrando com som",
            "params": {
                "intensidade": {"min": 1, "max": 10, "default": 5, "step": 1},
                "tipo_quebra": ["Radial", "Horizontal", "Vertical", "Mosaico"],
                "som": ["Sim", "Não"],
                "estilho": ["Realista", "Cartoon", "Futurista"]
            },
            "complexity": 3,
            "icon": "💥"
        },
        "Gotas d'Água": {
            "desc": "Efeito de gotas caindo na superfície",
            "params": {
                "quantidade": {"min": 1, "max": 20, "default": 8, "step": 1},
                "tamanho": {"min": 1, "max": 5, "default": 2, "step": 1},
                "velocidade": {"min": 1, "max": 5, "default": 3, "step": 1},
                "som": ["Sim", "Não"],
                "tipo": ["Água", "Óleo", "Metálico"]
            },
            "complexity": 3,
            "icon": "💧"
        },
        "Glitch": {
            "desc": "Efeito glitch digital",
            "params": {
                "intensidade": {"min": 1, "max": 10, "default": 5, "step": 1},
                "tipo": ["Digital", "Analógico", "RGB Split"],
                "duracao": {"min": 0.1, "max": 2.0, "default": 0.5, "step": 0.1}
            },
            "complexity": 2,
            "icon": "📺"
        }
    }
    
    @staticmethod
    def show_filter_examples(filter_name):
        if filter_name in EffectDatabase.FILTER_DATABASE:
            example_url = EffectDatabase.FILTER_DATABASE[filter_name].get("example")
            if example_url:
                st.image(example_url, caption=f"Exemplo do efeito {filter_name}", width=300)
    

# ======================================================================================
# CLASSE VIDEO PROCESSOR - VERSÃO FINAL E CORRIGIDA
# SUBSTITUA A SUA CLASSE ANTIGA POR ESTA
# ======================================================================================
class VideoProcessor:
    """Classe para processamento de vídeos com mensagens controladas"""
    
    @staticmethod
    def show_video_requirements_warning():
        """Mostra aviso apenas uma vez e de forma controlada"""
        if not VIDEO_SUPPORT and not st.session_state.get('video_warning_shown'):
            with st.sidebar.expander("⚠️ Informações de Vídeo", expanded=False):
                st.info("""
                    Para ativar recursos de vídeo:
                    ```bash
                    pip install moviepy imageio-ffmpeg
                    ```
                    Reinicie o aplicativo após instalação.
                """)
            st.session_state.video_warning_shown = True

    @staticmethod
    def get_video_status() -> str:
        """Retorna o status do suporte a vídeo para exibição controlada"""
        if VIDEO_SUPPORT:
            return "✅ Suporte a vídeo ativado"
        else:
            return "❌ Suporte a vídeo desativado (instale moviepy e imageio-ffmpeg)"
    
    @staticmethod
    def show_video_help():
        """Mostra ajuda de instalação apenas quando explicitamente solicitado"""
        with st.expander("ℹ️ Como ativar suporte a vídeo", expanded=False):
            st.code("pip install moviepy imageio-ffmpeg", language="bash")
            st.info("Reinicie o aplicativo após a instalação")

    @staticmethod
    def load_video(uploaded_file, max_size_mb=200) -> Optional[VideoFileClip]:
        """Carrega vídeo sem exibir erros"""
        if not VIDEO_SUPPORT:
            return None
            
        try:
            # Cria arquivo temporário
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_file.read())
                temp_path = tmp_file.name

            # Configuração silenciosa do FFmpeg
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    from moviepy.config import change_settings
                    change_settings({"FFMPEG_BINARY": os.environ.get("IMAGEIO_FFMPEG_EXE", "ffmpeg")})
            except:
                pass

            # Carrega o vídeo silenciosamente
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                clip = VideoFileClip(temp_path)
                
                # Pré-processamento para preview
                preview_clip = clip.copy()
                if preview_clip.duration > 30:
                    preview_clip = preview_clip.subclip(0, 30)
                if preview_clip.size[0] > 1280:
                    preview_clip = preview_clip.resize(width=1280)

                # Armazena informações necessárias
                st.session_state.original_video_clip = clip
                st.session_state.video_temp_path = temp_path
                
                return preview_clip
        except Exception:
            return None

    @staticmethod
    def export_video(video_clip, output_format='mp4', codec='libx264', fps=24) -> Optional[bytes]:
        """Exporta o vídeo processado sem mostrar erros desnecessários"""
        if not VIDEO_SUPPORT:
            return None
            
        temp_output_path = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{output_format}') as temp_file:
                temp_output_path = temp_file.name

            # Exporta silenciosamente
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                video_clip.write_videofile(temp_output_path, codec=codec, fps=fps, logger=None)

            with open(temp_output_path, 'rb') as f:
                video_bytes = f.read()
            
            return video_bytes
        except Exception:
            return None
        finally:
            if temp_output_path and os.path.exists(temp_output_path):
                try:
                    os.unlink(temp_output_path)
                except:
                    pass
            # Fecha o clipe para liberar recursos
            if hasattr(video_clip, 'close'):
                try:
                    video_clip.close()
                except:
                    pass
            if 'video_temp_path' in st.session_state and os.path.exists(st.session_state.video_temp_path):
                try:
                    os.unlink(st.session_state.video_temp_path)
                except:
                    pass
    
class VideoEffects:
    """Efeitos específicos para vídeo"""
    
    @staticmethod
    def apply_glow_effect(clip, intensity):
        """Aplica efeito glow otimizado para vídeo"""
        def glow_frame(frame):
            # Implementação otimizada usando OpenCV
            frame = cv2.GaussianBlur(frame, (0,0), intensity)
            return frame
            
        return clip.fl_image(glow_frame)
    
    @staticmethod
    def apply_color_tint(clip, color, intensity):
        """Aplica tom de cor otimizado para vídeo"""
        color_array = np.array(color) * intensity
        return clip.fl_image(lambda f: np.clip(f + color_array, 0, 255))
    
    @staticmethod
    def apply_vintage_effect(clip, intensity):
        """Efeito vintage otimizado para vídeo"""
        sepia_matrix = np.array([
            [0.393, 0.769, 0.189],
            [0.349, 0.686, 0.168],
            [0.272, 0.534, 0.131]
        ]) * intensity
        
        def sepia_frame(frame):
            frame = frame.dot(sepia_matrix.T)
            return np.clip(frame, 0, 255)
            
        return clip.fl_image(sepia_frame)
    
# Validar parâmetros de configuração
class ParameterValidator:
    @staticmethod
    def validate_config(config: Dict[str, Any]):
        """Valida a configuração completa"""
        # Validar filtros
        if "filtros" in config:
            for filter_name, params in config["filtros"].items():
                ParameterValidator.validate_filter_params(filter_name, params)
        
        # Validar moldura
        if "moldura" in config:
            if config["moldura"]["tipo"] not in EffectDatabase.FRAME_DATABASE:
                raise ValueError("Tipo de moldura inválido")
                
        # Validar animações
        if "animacao" in config:
            for anim_name, params in config["animacao"].items():
                if anim_name not in ["duracao", "repetir"]:
                    if anim_name not in EffectDatabase.ANIMATION_DATABASE:
                        raise ValueError(f"Animação {anim_name} não existe")
                    
    @staticmethod
    def validate_filter_params(filter_name, params):
        """Valida os parâmetros de um filtro"""
        if filter_name not in EffectDatabase.FILTER_DATABASE:
            raise ValueError(f"Filtro {filter_name} não encontrado")
            
        valid_params = EffectDatabase.FILTER_DATABASE[filter_name]["params"]
        for param_name, value in params.items():
            if param_name not in valid_params:
                raise ValueError(f"Parâmetro {param_name} não existe no filtro {filter_name}")
                
            param_config = valid_params[param_name]
            if isinstance(param_config, dict):  # É um slider
                min_val = param_config["min"]
                max_val = param_config["max"]
                if not (min_val <= value <= max_val):
                    raise ValueError(f"Valor {value} fora do intervalo permitido ({min_val}-{max_val}) para {param_name}")
                
# ======================================================================================
# NOVO BANCO DE DADOS PARA EFEITOS DE TEXTO
# ======================================================================================

class TextEffectDatabase:
    """Classe para gerenciar efeitos de texto disponíveis"""
    
    FONT_DATABASE = {
        "Padrão": {
            "desc": "Fonte simples e legível",
            "params": {},
            "icon": "🔤",
            "file": None  # Usará fallback
        },
        "Moderno": {
            "desc": "Fonte limpa e contemporânea",
            "params": {
                "espessura": ["Normal", "Fino", "Negrito"],
                "inclinação": ["Normal", "Itálico"]
            },
            "icon": "🅰️",
            "file": "arial.ttf"
        },
        "Vintage": {
            "desc": "Fonte retrô com estilo antigo",
            "params": {
                "decoracao": ["Nenhuma", "Sublinhado", "Tachado"]
            },
            "icon": "🖋️",
            "file": "times.ttf"
        },
        "Futurista": {
            "desc": "Fonte tecnológica e moderna",
            "params": {
                "brilho": {"min": 0, "max": 100, "default": 30, "step": 5}
            },
            "icon": "🔠",
            "file": "impact.ttf"
        },
        "Handwritten": {
            "desc": "Fonte manuscrita natural",
            "params": {
                "irregularidade": {"min": 0, "max": 50, "default": 10, "step": 5}
            },
            "icon": "✍️",
            "file": "comic.ttf"
        },
        "Decorativo": {
            "desc": "Fonte com elementos decorativos",
            "params": {
                "complexidade": {"min": 1, "max": 5, "default": 2, "step": 1}
            },
            "icon": "🎨",
            "file": "georgia.ttf"
        },
        "Personalizado": {
            "desc": "Fonte carregada pelo usuário",
            "params": {},
            "icon": "📤",
            "file": None  # Será definido pelo upload
        }
    }

    TEXT_ANIMATION_DATABASE = {
        "Digitação": {
            "desc": "Simula digitação em tempo real",
            "params": {
                "velocidade": {"min": 1, "max": 10, "default": 5, "step": 1},
                "cursor": ["Sim", "Não"],
                "som": ["Sim", "Não"]
            },
            "complexity": 1,
            "icon": "⌨️"
        },
        "Deslizar": {
            "desc": "Texto que desliza para dentro ou fora",
            "params": {
                "direcao": ["Esquerda", "Direita", "Cima", "Baixo"],
                "suavidade": {"min": 1, "max": 10, "default": 5, "step": 1}
            },
            "complexity": 1,
            "icon": "↔️"
        },
        "Pular": {
            "desc": "Letras que pulam para formar o texto",
            "params": {
                "intensidade": {"min": 1, "max": 10, "default": 5, "step": 1},
                "rotacao": ["Sim", "Não"]
            },
            "complexity": 2,
            "icon": "🦘"
        },
        "Girar": {
            "desc": "Texto que gira em 3D",
            "params": {
                "eixo": ["X", "Y", "Z", "XY", "XZ", "YZ"],
                "velocidade": {"min": 1, "max": 10, "default": 5, "step": 1}
            },
            "complexity": 2,
            "icon": "🔄"
        },
        "Dissolver": {
            "desc": "Texto que aparece gradualmente",
            "params": {
                "tipo": ["Aparecer", "Desaparecer", "Ambos"],
                "duracao": {"min": 0.5, "max": 3.0, "default": 1.5, "step": 0.1}
            },
            "complexity": 1,
            "icon": "✨"
        },
        "Zoom": {
            "desc": "Texto que amplia ou reduz",
            "params": {
                "tipo": ["In", "Out", "Pulsar"],
                "intensidade": {"min": 1, "max": 5, "default": 2, "step": 1}
            },
            "complexity": 1,
            "icon": "🔍"
        },
        "Glitch": {
            "desc": "Efeito digital glitch no texto",
            "params": {
                "intensidade": {"min": 1, "max": 10, "default": 5, "step": 1},
                "estilo": ["Digital", "RGB Split", "Estático"]
            },
            "complexity": 3,
            "icon": "📺"
        },
        "Quebra": {
            "desc": "Texto que se quebra e se junta",
            "params": {
                "pedacos": {"min": 2, "max": 10, "default": 4, "step": 1},
                "direcao": ["Horizontal", "Vertical", "Diagonal"]
            },
            "complexity": 3,
            "icon": "💥"
        },
        "Flutuar": {
            "desc": "Letras que flutuam suavemente",
            "params": {
                "intensidade": {"min": 1, "max": 10, "default": 5, "step": 1},
                "aleatorio": ["Sim", "Não"]
            },
            "complexity": 2,
            "icon": "☁️"
        },
        "Escrever": {
            "desc": "Efeito de escrita à mão",
            "params": {
                "velocidade": {"min": 1, "max": 10, "default": 5, "step": 1},
                "estilo": ["Caneta", "Pincel", "Giz"]
            },
            "complexity": 3,
            "icon": "✏️"
        },
        "Digitando": {
            "desc": "Efeito de máquina de escrever",
            "params": {
                "velocidade": {"min": 1, "max": 10, "default": 5},
                "cursor": ["Sim", "Não"],
                "som_teclado": ["Sim", "Não"]
            },
            "complexity": 2,
            "icon": "⌨️"
        },
        "Flutuante": {
            "desc": "Texto que flutua suavemente",
            "params": {
                "intensidade": {"min": 1, "max": 10, "default": 5},
                "direção": ["Cima", "Baixo", "Esquerda", "Direita"]
            },
            "complexity": 1,
            "icon": "🪽"
        }
    }

# ======================================================================================
# NOVAS FUNÇÕES 
# ======================================================================================
# Adicionar nova classe
class PresetManager:
    PRESETS = {
        "Vintage Classic": {
            "filtros": {
                "Vintage": {"intensidade": 80, "vinheta": 50, "granulacao": 15}
            },
            "moldura": {"tipo": "Vintage", "cor": "#8B5A2B", "espessura": 20}
        },
        "Cyberpunk": {
            "filtros": {
                "Futurístico": {"glow": 70, "neon": 50, "scanlines": 30},
                "Azulado": {"intensidade": 40}
            },
            "moldura": {"tipo": "Neon", "cor": "#FF00FF", "espessura": 10}
        }
    }
    
    @staticmethod
    def apply_preset(preset_name: str, config: Dict[str, Any]):
        """Aplica um preset à configuração atual"""
        if preset_name in PresetManager.PRESETS:
            preset = PresetManager.PRESETS[preset_name]
            config.update(preset)
            st.success(f"Preset '{preset_name}' aplicado!")
        else:
            st.error("Preset não encontrado")
    
    @staticmethod
    def render_preset_selector(config: Dict[str, Any]):
        """Renderiza o seletor de presets na UI"""
        with st.sidebar.expander("💾 PRESETS"):
            selected = st.selectbox(
                "Carregar Preset:",
                options=list(PresetManager.PRESETS.keys()),
                index=0
            )
            
            if st.button("Aplicar Preset"):
                PresetManager.apply_preset(selected, config)
            
            if st.button("Salvar como Preset..."):
                # Implementar lógica para salvar presets personalizados
                pass
            
class AdvancedExporter:
    """Classe para exportação avançada com qualidade aprimorada"""
    
    @staticmethod
    def _clean_image_background(img: Image.Image, bg_color: Tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        """Remove artefatos e sujeira do fundo da imagem"""
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            
        datas = img.getdata()
        new_data = []
        
        for item in datas:
            # Limpa pixels quase transparentes (threshold de 10)
            if item[3] < 10:
                new_data.append((bg_color[0], bg_color[1], bg_color[2], 0))
            else:
                # Mantém pixels com opacidade suficiente
                new_data.append(item)
                
        img.putdata(new_data)
        return img

    @staticmethod
    def export_with_quality(base_media: Union[Image.Image, VideoFileClip], 
                          config: Dict[str, Any], 
                          export_format: str,
                          quality_preset: str = "Alta",
                          output_size: str = "Original") -> Tuple[bytes, str, str]:
        """Exporta com controle de qualidade e limpeza de artefatos"""
        quality = QualitySettings.get_preset(quality_preset)
        
        # Determina o tamanho de saída
        if output_size == "HD (1280x720)":
            target_size = (1280, 720)
        elif output_size == "Full HD (1920x1080)":
            target_size = (1920, 1080)
        else:  # Original
            target_size = base_media.size if isinstance(base_media, Image.Image) else base_media.size[::-1]
        
        # Processa a mídia base com limpeza
        if isinstance(base_media, Image.Image):
            return AdvancedExporter._export_image_with_quality(
                base_media, config, export_format, quality, target_size
            )
        else:
            return AdvancedExporter._export_video_with_quality(
                base_media, config, export_format, quality, target_size
            )
            
    @staticmethod
    def _export_image_with_quality(image: Image.Image, 
                                 config: Dict[str, Any],
                                 format: str,
                                 quality: Dict[str, Any],
                                 target_size: Tuple[int, int]) -> Tuple[bytes, str]:
        """Exporta imagem com configurações de qualidade e limpeza"""
        # Redimensiona mantendo proporção se necessário
        if image.size != target_size:
            image = image.resize(target_size, Image.LANCZOS)
        
        # Aplica efeitos com limpeza intermediária
        processed = image.copy()
        if config.get("filtros"):
            processed = ImageProcessor.apply_filters(processed, config["filtros"])
            processed = AdvancedExporter._clean_image_background(processed)
        
        if config.get("moldura", {}).get("tipo", "Nenhuma") != "Nenhuma":
            processed = ImageProcessor.apply_frame(processed, config["moldura"])
            processed = AdvancedExporter._clean_image_background(processed)
        
        if config.get("texto"):
            processed = TextProcessor.apply_text_effect(processed, config)
            processed = AdvancedExporter._clean_image_background(processed)
        
        # Exporta no formato selecionado com limpeza final
        img_byte_arr = io.BytesIO()
        
        if format == "PNG":
            # Para PNG, garantimos transparência limpa
            processed = AdvancedExporter._clean_image_background(processed, (0, 0, 0))
            processed.save(
                img_byte_arr, 
                format='PNG',
                compress_level=9 - int(quality["quality"] / 12.5),  # 0-9
                optimize=True
            )
        else:  # JPG
            # Para JPG, preenchemos o fundo transparente com branco
            if processed.mode == 'RGBA':
                background = Image.new('RGB', processed.size, (255, 255, 255))
                background.paste(processed, mask=processed.split()[3])
                processed = background
            
            processed.save(
                img_byte_arr,
                format='JPEG',
                quality=quality["quality"],
                subsampling=quality["subsampling"],
                optimize=True
            )
        
        return img_byte_arr.getvalue(), f"image.{format.lower()}"
    
    @staticmethod
    def _export_video_with_quality(video_clip: VideoFileClip,
                                 config: Dict[str, Any],
                                 format: str,
                                 quality: Dict[str, Any],
                                 target_size: Tuple[int, int]) -> Tuple[bytes, str]:
        """Exporta vídeo com configurações de qualidade e limpeza"""
        temp_file = tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False)
        temp_file.close()
        
        try:
            # Aplica efeitos com limpeza
            processed = video_clip
            if config.get("filtros"):
                processed = processed.fl_image(
                    lambda f: np.array(AdvancedExporter._clean_image_background(
                        ImageProcessor.apply_filters(Image.fromarray(f), config["filtros"]))
                    )
                )
            
            if config.get("moldura", {}).get("tipo", "Nenhuma") != "Nenhuma":
                processed = processed.fl_image(
                    lambda f: np.array(AdvancedExporter._clean_image_background(
                        ImageProcessor.apply_frame(Image.fromarray(f), config["moldura"]))
                    )
                )
            
            # Redimensiona se necessário
            if processed.size != target_size[::-1]:
                processed = processed.resize(target_size)
            
            # Configurações de exportação com limpeza
            ffmpeg_params = {
                'codec': 'libx264',
                'preset': 'slow',
                'crf': quality["crf"],
                'threads': 4,
                'ffmpeg_params': ['-movflags', 'faststart'],
                'remove_temp': True
            }
            
            processed.write_videofile(
                temp_file.name,
                fps=24,
                **ffmpeg_params
            )
            
            with open(temp_file.name, 'rb') as f:
                video_data = f.read()
            
            return video_data, f"video.{format}"
        finally:
            try:
                os.unlink(temp_file.name)
            except:
                pass
            
    @staticmethod
    def _export_animated_gif(frames: List[Image.Image],
                            duration: float,
                            quality: Dict[str, Any]) -> Tuple[bytes, str]:
        """Exporta GIF animado com configurações de qualidade"""
        gif_bytes = io.BytesIO()
        
        # Otimiza o GIF com paleta de cores reduzida para melhor qualidade/tamanho
        disposal = 2  # Restaura ao fundo para transparência
        transparency = 0  # Índice de cor transparente
        
        # Configurações de otimização
        optimize = quality["quality"] > 70
        duration_ms = int(duration * 1000 / len(frames))
        
        frames[0].save(
            gif_bytes,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=duration_ms,
            loop=0,
            transparency=transparency,
            disposal=disposal,
            optimize=optimize,
            quality=quality["quality"],
            subsampling=0  # Sem subsampling para melhor qualidade
        )
        
        return gif_bytes.getvalue(), "animation.gif"
    
    @staticmethod
    def export_to_format(base_media: Union[Image.Image, VideoFileClip], config: Dict[str, Any], 
                        export_format: str) -> Tuple[bytes, str]:
        """
        Exporta para o formato especificado com suporte a:
        - Imagens estáticas (PNG, JPG)
        - Animações (GIF, MP4, MOV, MPEG)
        - Vídeos processados
        - Efeitos com transparência
        - Textos animados
        """
        # Verifica se é vídeo ou imagem
        is_video = isinstance(base_media, VideoFileClip)
        
        # Progresso
        progress_bar = st.progress(0)
        progress_bar.progress(10, text="Iniciando exportação...")
        
        try:
            # Processamento para vídeo
            if is_video:
                progress_bar.progress(20, text="Processando vídeo...")
                
                # Aplica filtros se existirem
                if config.get("filtros"):
                    base_media = base_media.fl_image(
                        lambda f: np.array(ImageProcessor.apply_filters(Image.fromarray(f), config["filtros"])))
                
                # Aplica moldura se existir
                if config.get("moldura", {}).get("tipo", "Nenhuma") != "Nenhuma":
                    base_media = base_media.fl_image(
                        lambda f: np.array(ImageProcessor.apply_frame(Image.fromarray(f), config["moldura"])))
                
                # Aplica texto se existir
                if config.get("texto"):
                    base_media = base_media.fl_image(
                        lambda f: np.array(TextProcessor.apply_text_effect(Image.fromarray(f), config)))
                
                progress_bar.progress(50, text="Convertendo formato...")
                
                # Exporta para diferentes formatos de vídeo
                if export_format in ["MP4", "MOV", "MPEG"]:
                    return AdvancedExporter._export_video(base_media, export_format.lower())
                elif export_format == "GIF":
                    return AdvancedExporter._export_video_to_gif(base_media)
                else:
                    raise ValueError(f"Formato não suportado para vídeo: {export_format}")
            
            # Processamento para imagem
            else:
                progress_bar.progress(20, text="Processando imagem...")
                
                # Aplica filtros, molduras e textos
                processed_image = base_media.copy()
                if config.get("filtros"):
                    processed_image = ImageProcessor.apply_filters(processed_image, config["filtros"])
                if config.get("moldura", {}).get("tipo", "Nenhuma") != "Nenhuma":
                    processed_image = ImageProcessor.apply_frame(processed_image, config["moldura"])
                if config.get("texto"):
                    processed_image = TextProcessor.apply_text_effect(processed_image, config)
                
                progress_bar.progress(50, text="Convertendo formato...")
                
                # Exporta para diferentes formatos de imagem/animação
                if export_format in ["PNG", "JPG"]:
                    return AdvancedExporter._export_static_image(processed_image, export_format)
                elif export_format == "GIF":
                    # Verifica se há animações de texto para exportar como GIF
                    if config.get("animacao_texto"):
                        return AdvancedExporter._export_text_animation(processed_image, config)
                    return AdvancedExporter._export_animation_gif(processed_image, config)
                elif export_format in ["MP4", "MOV", "MPEG"]:
                    # Verifica se há animações de texto para exportar como vídeo
                    if config.get("animacao_texto"):
                        return AdvancedExporter._export_text_animation_video(processed_image, config, export_format.lower())
                    return AdvancedExporter._export_animation_video(processed_image, config, export_format.lower())
                else:
                    raise ValueError(f"Formato não suportado: {export_format}")
        
        finally:
            progress_bar.progress(100, text="Exportação concluída!")
            time.sleep(0.5)
            progress_bar.empty()
    
    @staticmethod
    def _export_text_animation(base_image: Image.Image, config: Dict[str, Any]) -> Tuple[bytes, str]:
        """Exporta animação de texto como GIF"""
        duration = config["animacao_texto"].get("duracao", 2.0)
        frames = TextProcessor.generate_text_animation_frames(
            base_image, config, config["animacao_texto"], duration
        )
        
        gif_bytes = io.BytesIO()
        frames[0].save(
            gif_bytes,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=int(duration * 1000 / len(frames)),
            loop=0
        )
        return gif_bytes.getvalue(), "text_animation.gif"
            
    @staticmethod
    def _export_static_image(image: Image.Image, format: str) -> Tuple[bytes, str]:
        """Exporta imagem estática"""
        img_byte_arr = io.BytesIO()
        
        if format == "PNG":
            image.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue(), "image.png"
        elif format == "JPG":
            image.save(img_byte_arr, format='JPEG', quality=95)
            return img_byte_arr.getvalue(), "image.jpg"
        else:
            raise ValueError(f"Formato de imagem não suportado: {format}")
        
    @staticmethod
    def _export_video(video_clip: VideoFileClip, format: str) -> Tuple[bytes, str]:
        """Exporta vídeo para formatos MP4, MOV, MPEG"""
        temp_file = tempfile.NamedTemporaryFile(suffix=f'.{format}', delete=False)
        temp_file.close()
        
        try:
            video_clip.write_videofile(temp_file.name, codec='libx264', fps=24, logger=None)
            
            with open(temp_file.name, 'rb') as f:
                video_data = f.read()
            
            return video_data, f"video.{format}"
        finally:
            try:
                os.unlink(temp_file.name)
            except:
                pass
            
    @staticmethod
    def _export_video_to_gif(video_clip: VideoFileClip) -> Tuple[bytes, str]:
        """Converte vídeo para GIF animado"""
        temp_file = tempfile.NamedTemporaryFile(suffix='.gif', delete=False)
        temp_file.close()
        
        try:
            video_clip.write_gif(temp_file.name, fps=15)
            
            with open(temp_file.name, 'rb') as f:
                gif_data = f.read()
            
            return gif_data, "animation.gif"
        finally:
            try:
                os.unlink(temp_file.name)
            except:
                pass
    
    @staticmethod
    def _convert_image_to_video(image: Image.Image, format: str) -> Tuple[bytes, str]:
        """Converte imagem estática em vídeo curto"""
        # Cria um clip de 2 segundos com a imagem
        clip = ImageSequenceClip([np.array(image)], fps=1, durations=[2])
        
        temp_file = tempfile.NamedTemporaryFile(suffix=f'.{format}', delete=False)
        clip.write_videofile(temp_file.name, codec='libx264', fps=24)
        
        with open(temp_file.name, 'rb') as f:
            video_data = f.read()
        
        return video_data, f"animation.{format}"
    
    @staticmethod
    def _export_animation_video(image: Image.Image, config: Dict[str, Any], 
                              format: str) -> Tuple[bytes, str]:
        """Exporta animação como vídeo (MP4, MOV, MPEG)"""
        temp_file = tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False)
        temp_file.close()
        
        try:
            # Gera frames da animação
            duration = config.get("animacao", {}).get("duracao", 2.0)
            
            if config.get("animacao_texto"):
                frames = TextProcessor.generate_text_animation_frames(
                    image, config, config["animacao_texto"], duration
                )
            else:
                frames = AnimationPreviewer.generate_animation_frames(
                    image, config["animacao"], duration
                )
            
            # Salva como GIF primeiro (para conversão)
            gif_file = tempfile.NamedTemporaryFile(suffix=".gif", delete=False)
            gif_file.close()
            
            frames[0].save(
                gif_file.name,
                format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=int(duration * 1000 / len(frames)),
                loop=0
            )
            
            # Converte GIF para vídeo usando ffmpeg
            try:
                import subprocess
                subprocess.run([
                    'ffmpeg', '-y', '-i', gif_file.name,
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                    '-movflags', 'faststart', temp_file.name
                ], check=True)
                
                with open(temp_file.name, 'rb') as f:
                    video_data = f.read()
                
                return video_data, f"animation.{format}"
            
            except Exception as e:
                st.warning(f"Falha ao converter para vídeo: {str(e)}. Exportando como GIF.")
                with open(gif_file.name, 'rb') as f:
                    gif_data = f.read()
                return gif_data, "animation.gif"
        
        finally:
            try:
                os.unlink(temp_file.name)
                os.unlink(gif_file.name)
            except:
                pass
    
    @staticmethod
    def _export_static_video(image: Image.Image, format: str) -> Tuple[bytes, str]:
        """Exporta imagem estática como vídeo curto"""
        temp_file = tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False)
        temp_file.close()
        
        try:
            # Cria um GIF de 1 frame e converte para vídeo
            gif_file = tempfile.NamedTemporaryFile(suffix=".gif", delete=False)
            gif_file.close()
            
            image.save(gif_file.name, format='GIF')
            
            # Converte para vídeo
            try:
                import subprocess
                subprocess.run([
                    'ffmpeg', '-y', '-i', gif_file.name,
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                    '-t', '2',  # 2 segundos de duração
                    '-movflags', 'faststart', temp_file.name
                ], check=True)
                
                with open(temp_file.name, 'rb') as f:
                    video_data = f.read()
                
                return video_data, f"static.{format}"
            
            except Exception as e:
                st.warning(f"Falha ao converter para vídeo: {str(e)}. Exportando como GIF.")
                with open(gif_file.name, 'rb') as f:
                    gif_data = f.read()
                return gif_data, "static.gif"
        
        finally:
            try:
                os.unlink(temp_file.name)
                os.unlink(gif_file.name)
            except:
                pass
    
    @staticmethod
    def _export_animation_gif(image: Image.Image, config: Dict[str, Any]) -> Tuple[bytes, str]:
        """Exporta animação como GIF"""
        duration = config.get("animacao", {}).get("duracao", 2.0)
        
        # Gera frames com animações de texto ou efeitos
        if config.get("animacao_texto"):
            frames = TextProcessor.generate_text_animation_frames(
                image, config, config["animacao_texto"], duration
            )
        else:
            frames = AnimationPreviewer.generate_animation_frames(
                image, config["animacao"], duration
            )
        
        gif_bytes = io.BytesIO()
        frames[0].save(
            gif_bytes,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            duration=int(duration * 1000 / len(frames)),
            loop=0
        )
        gif_bytes.seek(0)
        
        return gif_bytes.getvalue(), "animation.gif"
    
    @staticmethod
    def _export_static_gif(image: Image.Image) -> Tuple[bytes, str]:
        """Exporta imagem estática como GIF"""
        gif_bytes = io.BytesIO()
        image.save(gif_bytes, format='GIF')
        gif_bytes.seek(0)
        return gif_bytes.getvalue(), "image.gif"
    
    @staticmethod
    def export_effects_only(config: Dict[str, Any], size: Tuple[int, int] = (1920, 1080)) -> Tuple[bytes, str]:
        """Exporta apenas os efeitos com transparência"""
        try:
            # Cria imagem transparente
            transparent_bg = Image.new('RGBA', size, (0, 0, 0, 0))
            
            # Aplica efeitos
            processed = ImageProcessor.apply_effects_to_transparent(transparent_bg, config)
            
            # Exporta como PNG
            img_byte_arr = io.BytesIO()
            processed.save(img_byte_arr, format='PNG')
            
            return img_byte_arr.getvalue(), "effects_only.png"
            
        except Exception as e:
            raise ValueError(f"Erro ao exportar efeitos: {str(e)}")
    
class TextProcessor:
    """Classe para processamento avançado de texto e animações"""
    
    @staticmethod
    def get_text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont) -> Tuple[int, int]:
        """Compatível com todas as versões do Pillow"""
        if not isinstance(draw, ImageDraw.ImageDraw):
            raise ValueError("O parâmetro 'draw' deve ser um objeto ImageDraw")
        if not text or not isinstance(text, str):
            raise ValueError("O parâmetro 'text' deve ser uma string não vazia")
        if not font:
            raise ValueError("O parâmetro 'font' é obrigatório")
        
        try:
            # Pillow 8.0+: usa textbbox
            bbox = draw.textbbox((0, 0), text, font=font)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]
        except AttributeError:
            # Pillow mais antigo
            return draw.textsize(text, font=font)
    
    @staticmethod
    def apply_text_effect(image: Image.Image, text_config: Dict[str, Any]) -> Image.Image:
        """Aplica texto estático à imagem com verificação de tamanho"""
        if not text_config.get("texto") or not text_config.get("fonte"):
            return image
            
        try:
            # Verifica e redimensiona a imagem se necessário
            if not ImageProcessor.check_image_size(image):
                image = ImageProcessor.resize_large_image(image)
                st.warning("Imagem redimensionada para prevenir problemas de processamento")
                
            img = image.copy().convert("RGBA")
            draw = ImageDraw.Draw(img)
        
            # Configurações básicas
            text = text_config["texto"]
            font_name = text_config["fonte"]["tipo"]
            font_size = text_config["fonte"]["tamanho"]
            font_color = text_config["fonte"]["cor"]
            position = text_config["posicao"]
            outline = text_config.get("contorno", {})
            
            # Carrega a fonte usando o método auxiliar
            font = TextProcessor._load_font(font_name, font_size)
            
            # Calcula a posição
            text_width, text_height = TextProcessor.get_text_size(draw, text, font)
            x = {
                "Esquerda": 20,
                "Centro": (img.width - text_width) // 2,
                "Direita": img.width - text_width - 20
            }[position["horizontal"]]
            
            y = {
                "Topo": 20,
                "Meio": (img.height - text_height) // 2,
                "Base": img.height - text_height - 20
            }[position["vertical"]]
            
            # Aplica contorno se necessário
            if outline.get("ativo", False):
                outline_width = outline.get("espessura", 1)
                outline_color = outline.get("cor", "#000000")
                
                # Desenha o contorno em várias posições para criar o efeito
                for adj in range(outline_width):
                    for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), 
                                (0,1), (1,-1), (1,0), (1,1)]:
                        draw.text((x+dx*adj, y+dy*adj), text, 
                                fill=outline_color, font=font)
            
            # Desenha o texto principal
            draw.text((x, y), text, fill=font_color, font=font)
            
            return img
            
        except Exception as e:
            st.error(f"Erro ao aplicar texto: {str(e)}")
            return image
    
    @staticmethod
    def get_available_fonts() -> List[str]:
        """Retorna a lista de fontes disponíveis no sistema"""
        try:
            import matplotlib.font_manager
            system_fonts = [f.name for f in matplotlib.font_manager.fontManager.ttflist]
            return sorted(system_fonts)
        except:
            return []
    
    @staticmethod
    def _load_font(font_name: str, font_size: int) -> ImageFont.FreeTypeFont:
        """Carrega uma fonte com fallback para padrão e verificação de disponibilidade"""
        try:
            # 1. Verifica se é uma fonte personalizada carregada
            if font_name == "Personalizado" and "custom_font" in st.session_state:
                try:
                    return ImageFont.truetype(st.session_state.custom_font, font_size)
                except IOError:
                    st.error("Fonte personalizada inválida. Usando fallback.")
            
            # 2. Verifica se a fonte está no banco de dados
            font_info = TextEffectDatabase.FONT_DATABASE.get(font_name, {})
            
            # 3. Tenta carregar a fonte específica se existir
            if font_info.get("file"):
                try:
                    return ImageFont.truetype(font_info["file"], font_size)
                except (IOError, AttributeError):
                    pass
            
            # 4. Tenta carregar do sistema
            try:
                return ImageFont.truetype(font_name, font_size)
            except (IOError, OSError):
                pass
            
            # 5. Fallback final
            return ImageFont.load_default()
            
        except Exception as e:
            st.error(f"Erro ao carregar fonte: {str(e)}")
            return ImageFont.load_default()
    
    @staticmethod
    def generate_text_animation_frames(base_image: Image.Image, 
                                    config: Dict[str, Any], 
                                    animation_config: Dict[str, Any], 
                                    duration: float) -> List[Image.Image]:
        """Gera frames de animação de texto em alta qualidade"""
        frames = []
        
        try:
            # Mantém o tamanho original
            original_size = base_image.size
            
            # Configura número de frames (24fps padrão)
            num_frames = min(60, int(duration * 24))
            
            for frame_num in range(num_frames):
                progress = frame_num / (num_frames - 1) if num_frames > 1 else 0
                
                # Cria cópia em alta qualidade
                frame_img = base_image.copy().convert("RGBA")
                
                # Redimensiona apenas se necessário
                if frame_img.size != original_size:
                    frame_img = frame_img.resize(original_size, Image.LANCZOS)
                
                # Aplica efeitos de animação de texto
                for anim_name, anim_params in animation_config.items():
                    if anim_name not in ["duracao", "repetir"]:
                        frame_img = TextProcessor.apply_text_animation_effect(
                            frame_img, config, anim_name, anim_params, progress, duration
                        )
                
                # Garante o tamanho correto
                if frame_img.size != original_size:
                    frame_img = frame_img.resize(original_size, Image.LANCZOS)
                
                frames.append(frame_img)
            
            return frames
        
        except Exception as e:
            st.error(f"Erro ao gerar animação de texto: {str(e)}")
            return [base_image]  # Fallback
    
    @staticmethod
    def apply_text_animation_effect(img: Image.Image, text_config: Dict[str, Any], 
                                   anim_name: str, anim_params: Dict[str, Any], 
                                   progress: float, duration: float) -> Image.Image:
        """Aplica um único efeito de animação de texto em um frame específico"""
        if anim_name == "Digitação":
            return TextProcessor.apply_typing_effect(img, text_config, anim_params, progress)
        elif anim_name == "Deslizar":
            return TextProcessor.apply_slide_text_effect(img, text_config, anim_params, progress)
        elif anim_name == "Pular":
            return TextProcessor.apply_jump_effect(img, text_config, anim_params, progress)
        elif anim_name == "Girar":
            return TextProcessor.apply_rotate_text_effect(img, text_config, anim_params, progress)
        elif anim_name == "Dissolver":
            return TextProcessor.apply_dissolve_effect(img, text_config, anim_params, progress)
        elif anim_name == "Zoom":
            return TextProcessor.apply_zoom_text_effect(img, text_config, anim_params, progress)
        elif anim_name == "Glitch":
            return TextProcessor.apply_glitch_text_effect(img, text_config, anim_params, progress)
        elif anim_name == "Quebra":
            return TextProcessor.apply_break_effect(img, text_config, anim_params, progress)
        elif anim_name == "Flutuar":
            return TextProcessor.apply_float_effect(img, text_config, anim_params, progress)
        elif anim_name == "Escrever":
            return TextProcessor.apply_writing_effect(img, text_config, anim_params, progress)
        
        return img
    
    @staticmethod
    def apply_typing_effect(img: Image.Image, text_config: Dict[str, Any], 
                           params: Dict[str, Any], progress: float) -> Image.Image:
        """Efeito de digitação simulada"""
        text = text_config["texto"]
        speed = params.get("velocidade", 5)
        show_cursor = params.get("cursor", "Sim") == "Sim"
        
        # Calcula quantos caracteres mostrar
        chars_to_show = int(progress * len(text) * (speed/5))
        partial_text = text[:chars_to_show]
        
        if show_cursor and progress < 0.99:
            partial_text += "|"  # Adiciona cursor piscante
            
        # Atualiza o texto temporário
        temp_config = text_config.copy()
        temp_config["texto"] = partial_text
        
        return TextProcessor.apply_text_effect(img, temp_config)
    
    @staticmethod
    def apply_slide_text_effect(img: Image.Image, text_config: Dict[str, Any], 
                               params: Dict[str, Any], progress: float) -> Image.Image:
        """Efeito de texto deslizando"""
        direction = params.get("direcao", "Esquerda")
        width, height = img.size
        
        # Calcula o deslocamento baseado na direção
        if direction == "Esquerda":
            offset = (int(-width * (1 - progress))), 0
        elif direction == "Direita":
            offset = (int(width * (1 - progress))), 0
        elif direction == "Cima":
            offset = 0, int(-height * (1 - progress))
        else:  # Baixo
            offset = 0, int(height * (1 - progress))
        
        # Cria uma nova imagem com o texto deslocado
        text_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        text_img.paste(TextProcessor.apply_text_effect(img, text_config), offset)
        
        return Image.alpha_composite(img.convert("RGBA"), text_img)
    
    @staticmethod
    def apply_jump_effect(img: Image.Image, text_config: Dict[str, Any], 
                        params: Dict[str, Any], progress: float) -> Image.Image:
        """Efeito de letras pulando"""
        intensity = params.get("intensidade", 5)
        rotate = params.get("rotacao", "Sim") == "Sim"
        text = text_config["texto"]
        
        # Cria uma nova imagem para compor o texto
        text_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)
        
        try:
            # Carrega a fonte usando o método auxiliar
            font = TextProcessor._load_font(text_config["fonte"]["tipo"], text_config["fonte"]["tamanho"])
            
            # CORREÇÃO: Criar um ImageDraw temporário para calcular o tamanho do texto
            temp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
            char_width, char_height = TextProcessor.get_text_size(temp_draw, "A", font)
            
            # Posição inicial do texto
            x = {
                "Esquerda": 20,
                "Centro": (img.width - len(text) * char_width) // 2,
                "Direita": img.width - len(text) * char_width - 20
            }[text_config["posicao"]["horizontal"]]
            
            y_base = {
                "Topo": 20,
                "Meio": (img.height - char_height) // 2,
                "Base": img.height - char_height - 20
            }[text_config["posicao"]["vertical"]]
            
            # Desenha cada caractere com animação individual
            for i, char in enumerate(text):
                # Calcula progresso individual para cada caractere
                char_progress = min(1.0, max(0.0, (progress - i*0.1) * 1.5))
                
                if char_progress > 0:
                    # Calcula posição Y com efeito de salto
                    jump_height = intensity * 10 * math.sin(char_progress * math.pi)
                    y = y_base - int(jump_height)
                    
                    # Rotação se ativada
                    angle = int(char_progress * 360) if rotate else 0
                    
                    # Cria uma imagem para o caractere individual
                    char_img = Image.new("RGBA", (char_width, char_height * 2), (0, 0, 0, 0))
                    char_draw = ImageDraw.Draw(char_img)
                    char_draw.text((0, char_height - jump_height), char, 
                                fill=text_config["fonte"]["cor"], font=font)
                    
                    if angle != 0:
                        char_img = char_img.rotate(angle, expand=True, resample=Image.BILINEAR)
                    
                    # Cola o caractere na posição correta
                    text_img.paste(char_img, (x + i * char_width, y), char_img)
            
            return Image.alpha_composite(img.convert("RGBA"), text_img)
            
        except Exception as e:
            st.error(f"Erro no efeito de pulo: {str(e)}")
            return img
    
    @staticmethod
    def apply_rotate_text_effect(img: Image.Image, text_config: Dict[str, Any], 
                                params: Dict[str, Any], progress: float) -> Image.Image:
        """Efeito de rotação 3D no texto"""
        axis = params.get("eixo", "Y")
        speed = params.get("velocidade", 5)
        angle = 360 * progress * (speed / 5)
        
        # Cria uma imagem apenas com o texto
        text_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        text_img.paste(TextProcessor.apply_text_effect(img, text_config))
        
        # Aplica transformação de perspectiva simulada
        if axis in ["X", "XY", "XZ"]:
            # Distorção vertical para simular rotação X
            width, height = text_img.size
            text_img = text_img.transform(
                (width, height), Image.QUAD,
                (0, height * (0.5 - 0.5 * math.cos(math.radians(angle))),
                 0, height * (0.5 + 0.5 * math.cos(math.radians(angle))),
                 width, height * (0.5 + 0.5 * math.cos(math.radians(angle))),
                 width, height * (0.5 - 0.5 * math.cos(math.radians(angle)))),
                Image.BILINEAR
            )
        
        if axis in ["Y", "XY", "YZ"]:
            # Distorção horizontal para simular rotação Y
            width, height = text_img.size
            text_img = text_img.transform(
                (width, height), Image.QUAD,
                (width * (0.5 - 0.5 * math.cos(math.radians(angle))), 0,
                width * (0.5 + 0.5 * math.cos(math.radians(angle))), 0,
                width * (0.5 + 0.5 * math.cos(math.radians(angle))), height,
                width * (0.5 - 0.5 * math.cos(math.radians(angle))), height),
                Image.BILINEAR
            )
        
        return Image.alpha_composite(img.convert("RGBA"), text_img)
    
    @staticmethod
    def apply_dissolve_effect(img: Image.Image, text_config: Dict[str, Any], 
                            params: Dict[str, Any], progress: float) -> Image.Image:
        """Efeito de dissolução (aparecer/desaparecer)"""
        effect_type = params.get("tipo", "Aparecer")
        duration = params.get("duracao", 1.5)
        
        # Calcula opacidade baseada no tipo de efeito
        if effect_type == "Aparecer":
            alpha = int(255 * progress)
        elif effect_type == "Desaparecer":
            alpha = int(255 * (1 - progress))
        else:  # Ambos
            alpha = int(255 * (1 - abs(progress - 0.5) * 2))
        
        # Cria texto com opacidade variável
        text_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)
        
        try:
            # Carrega a fonte usando o método auxiliar
            font = TextProcessor._load_font(text_config["fonte"]["tipo"], text_config["fonte"]["tamanho"])
            text = text_config["texto"]
            color = (*ImageColor.getrgb(text_config["fonte"]["cor"]), alpha)
            
            # Calcula posição
            text_width, text_height = TextProcessor.get_text_size(draw, text, font)
            x = {
                "Esquerda": 20,
                "Centro": (img.width - text_width) // 2,
                "Direita": img.width - text_width - 20
            }[text_config["posicao"]["horizontal"]]
            
            y = {
                "Topo": 20,
                "Meio": (img.height - text_height) // 2,
                "Base": img.height - text_height - 20
            }[text_config["posicao"]["vertical"]]
            
            draw.text((x, y), text, fill=color, font=font)
            
            return Image.alpha_composite(img.convert("RGBA"), text_img)
            
        except Exception as e:
            st.error(f"Erro no efeito de dissolução: {str(e)}")
            return img
    
    @staticmethod
    def apply_zoom_text_effect(img: Image.Image, text_config: Dict[str, Any], 
                              params: Dict[str, Any], progress: float) -> Image.Image:
        """Efeito de zoom no texto"""
        zoom_type = params.get("tipo", "In")
        intensity = params.get("intensidade", 2)
        
        if zoom_type == "In":
            scale = 1 + (intensity / 5) * progress
        elif zoom_type == "Out":
            scale = 1 + (intensity / 5) * (1 - progress)
        else:  # Pulsar
            scale = 1 + (intensity / 10) * math.sin(progress * math.pi * 2)
        
        # Cria texto em tamanho variável
        temp_config = text_config.copy()
        temp_config["fonte"]["tamanho"] = int(text_config["fonte"]["tamanho"] * scale)
        
        return TextProcessor.apply_text_effect(img, temp_config)
    
    @staticmethod
    def apply_glitch_text_effect(img: Image.Image, text_config: Dict[str, Any], 
                                params: Dict[str, Any], progress: float) -> Image.Image:
        """Efeito glitch no texto"""
        intensity = params.get("intensidade", 5)
        style = params.get("estilo", "Digital")
        
        # Cria imagem com o texto
        text_img = TextProcessor.apply_text_effect(img, text_config).convert("RGBA")
        text_array = np.array(text_img)
        
        # Aplica efeitos baseados no estilo
        if style == "RGB Split":
            # Desloca canais de cor
            shift = intensity * 2
            r = np.roll(text_array[:,:,0], shift, axis=1)
            g = text_array[:,:,1]
            b = np.roll(text_array[:,:,2], -shift, axis=1)
            text_array = np.dstack((r, g, b))
        else:
            # Efeito de deslocamento aleatório
            for i in range(0, text_img.height, random.randint(5, 20)):
                shift = random.randint(-intensity, intensity)
                if shift != 0:
                    text_array[i,:] = np.roll(text_array[i,:], shift, axis=0)
        
        return Image.fromarray(text_array)
    
    @staticmethod
    def apply_break_effect(img: Image.Image, text_config: Dict[str, Any], 
                          params: Dict[str, Any], progress: float) -> Image.Image:
        """Efeito de texto quebrando e se juntando"""
        pieces = params.get("pedacos", 4)
        direction = params.get("direcao", "Horizontal")
        text = text_config["texto"]
        
        # Cria imagem para o texto completo
        text_img = TextProcessor.apply_text_effect(img, text_config).convert("RGBA")
        text_array = np.array(text_img)
        
        # Calcula áreas para quebrar
        height, width = text_array.shape[:2]
        
        if direction == "Horizontal":
            piece_height = height // pieces
            for i in range(pieces):
                offset = int((1 - progress) * 100 * (i % 2 * 2 - 1))
                y_start = i * piece_height
                y_end = (i + 1) * piece_height if i < pieces - 1 else height
                
                # Aplica deslocamento vertical
                text_array[y_start:y_end, :] = np.roll(
                    text_array[y_start:y_end, :], 
                    offset, 
                    axis=0
                )
        elif direction == "Vertical":
            piece_width = width // pieces
            for i in range(pieces):
                offset = int((1 - progress) * 100 * (i % 2 * 2 - 1))
                x_start = i * piece_width
                x_end = (i + 1) * piece_width if i < pieces - 1 else width
                
                # Aplica deslocamento horizontal
                text_array[:, x_start:x_end] = np.roll(
                    text_array[:, x_start:x_end], 
                    offset, 
                    axis=1
                )
        else:  # Diagonal
            for i in range(pieces):
                offset_x = int((1 - progress) * 50 * (i % 2 * 2 - 1))
                offset_y = int((1 - progress) * 50 * (i % 2 * 2 - 1))
                
                # Aplica deslocamento diagonal
                text_array = np.roll(text_array, offset_x, axis=1)
                text_array = np.roll(text_array, offset_y, axis=0)
        
        return Image.fromarray(text_array)
    
    @staticmethod
    def apply_float_effect(img: Image.Image, text_config: Dict[str, Any], 
                        params: Dict[str, Any], progress: float) -> Image.Image:
        """Efeito de letras flutuando suavemente"""
        intensity = params.get("intensidade", 5)
        random_effect = params.get("aleatorio", "Sim") == "Sim"
        text = text_config["texto"]
        
        # Cria uma nova imagem para compor o texto
        text_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)
        
        try:
            # Carrega a fonte usando o método auxiliar
            font = TextProcessor._load_font(text_config["fonte"]["tipo"], text_config["fonte"]["tamanho"])
            
            # CORREÇÃO: Criar um ImageDraw temporário para calcular o tamanho do texto
            temp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
            char_width, char_height = TextProcessor.get_text_size(temp_draw, "A", font)
            
            # Posição inicial do texto
            x = {
                "Esquerda": 20,
                "Centro": (img.width - len(text) * char_width) // 2,
                "Direita": img.width - len(text) * char_width - 20
            }[text_config["posicao"]["horizontal"]]
            
            y_base = {
                "Topo": 20,
                "Meio": (img.height - char_height) // 2,
                "Base": img.height - char_height - 20
            }[text_config["posicao"]["vertical"]]
            
            # Desenha cada caractere com animação individual
            for i, char in enumerate(text):
                # Calcula deslocamento vertical
                if random_effect:
                    random.seed(i)  # Para manter consistente entre frames
                    phase = random.random() * 2 * math.pi
                else:
                    phase = i * 0.5
                
                float_offset = int(intensity * 2 * math.sin(progress * 2 * math.pi + phase))
                
                # Desenha o caractere na posição flutuante
                draw.text((x + i * char_width, y_base + float_offset), 
                        char, fill=text_config["fonte"]["cor"], font=font)
            
            return Image.alpha_composite(img.convert("RGBA"), text_img)
            
        except Exception as e:
            st.error(f"Erro no efeito de flutuação: {str(e)}")
            return img
    
    @staticmethod
    def apply_writing_effect(img: Image.Image, text_config: Dict[str, Any], 
                            params: Dict[str, Any], progress: float) -> Image.Image:
        """Efeito de escrita à mão"""
        speed = params.get("velocidade", 5)
        style = params.get("estilo", "Caneta")
        text = text_config["texto"]
        
        # Cria uma nova imagem para compor o texto
        text_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)
        
        try:
            # Carrega a fonte usando o método auxiliar
            font = TextProcessor._load_font(text_config["fonte"]["tipo"], text_config["fonte"]["tamanho"])
            
            # CORREÇÃO: Criar um ImageDraw temporário para calcular o tamanho do texto
            temp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
            char_width, char_height = TextProcessor.get_text_size(temp_draw, "A", font)
            
            # Posição inicial do texto
            x = {
                "Esquerda": 20,
                "Centro": (img.width - len(text) * char_width) // 2,
                "Direita": img.width - len(text) * char_width - 20
            }[text_config["posicao"]["horizontal"]]
            
            y = {
                "Topo": 20,
                "Meio": (img.height - char_height) // 2,
                "Base": img.height - char_height - 20
            }[text_config["posicao"]["vertical"]]
            
            # Calcula quantos caracteres mostrar completamente
            full_chars = int(progress * len(text) * (speed/5))
            
            # Desenha os caracteres completos
            if full_chars > 0:
                draw.text((x, y), text[:full_chars], 
                        fill=text_config["fonte"]["cor"], font=font)
            
            # Efeito de escrita parcial no próximo caractere
            if full_chars < len(text):
                partial_progress = (progress * len(text) * (speed/5)) % 1
                next_char = text[full_chars]
                
                # Cria máscara para o efeito de escrita
                mask = Image.new("L", (char_width, char_height), 0)
                mask_draw = ImageDraw.Draw(mask)
                
                if style == "Caneta":
                    # Efeito de caneta (linha contínua)
                    mask_draw.line((0, char_height//2, 
                                char_width * partial_progress, char_height//2), 
                                fill=255, width=2)
                elif style == "Pincel":
                    # Efeito de pincel (mais grosso e irregular)
                    for i in range(int(char_width * partial_progress)):
                        y_offset = random.randint(-2, 2)
                        mask_draw.line((i, char_height//2 + y_offset, 
                                    i+1, char_height//2 + y_offset), 
                                    fill=255, width=4)
                else:  # Giz
                    # Efeito de giz (pontilhado)
                    for i in range(int(char_width * partial_progress)):
                        if random.random() < 0.7:
                            y_offset = random.randint(-1, 1)
                            mask_draw.point((i, char_height//2 + y_offset), fill=255)
                
                # Desenha o caractere parcial
                char_img = Image.new("RGBA", (char_width, char_height), (0, 0, 0, 0))
                char_draw = ImageDraw.Draw(char_img)
                char_draw.text((0, 0), next_char, 
                            fill=text_config["fonte"]["cor"], font=font)
                
                # Aplica a máscara
                char_img.putalpha(mask)
                text_img.paste(char_img, (x + full_chars * char_width, y), char_img)
            
            return Image.alpha_composite(img.convert("RGBA"), text_img)
            
        except Exception as e:
            st.error(f"Erro no efeito de escrita: {str(e)}")
            return img
    
# ======================================================================================
# FUNÇÕES DE PROCESSAMENTO DE IMAGEM SUPER OTIMIZADAS
# ======================================================================================

class ImageProcessor:
    """Classe para processamento avançado de imagens"""
    
    @staticmethod
    @st.cache_data(show_spinner=False, max_entries=3)
    def load_sample_image() -> Image.Image:
        """Carrega imagem de exemplo com múltiplos fallbacks e cache"""
        sample_urls = [
            "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0",
            "https://images.unsplash.com/photo-1494253109108-2e30c049369b",
            "https://images.unsplash.com/photo-1519125323398-675f0ddb6308"
        ]
        
        for url in sample_urls:
            try:
                response = requests.get(f"{url}?w=800&h=600&fit=crop", timeout=2)
                response.raise_for_status()
                return Image.open(BytesIO(response.content))
            except:
                continue
        
        # Fallback final
        img = Image.new('RGB', (800, 600), (50, 50, 50))
        draw = ImageDraw.Draw(img)
        draw.text((250, 280), "IMAGEM DE EXEMPLO", fill=(255, 255, 255))
        draw.text((200, 320), "Envie sua própria imagem para testar", fill=(200, 200, 200))
        return img
    
    @staticmethod
    def apply_filters_to_video_frame(frame, filters_config):
        """Aplica filtros a um frame de vídeo (array numpy)"""
        img = Image.fromarray(frame)
        processed = ImageProcessor.apply_filters(img, filters_config)
        return np.array(processed)
    
    @staticmethod
    def check_image_size(img: Image.Image) -> bool:
        """Verifica se a imagem excede o limite de tamanho"""
        return img.width * img.height <= MAX_IMAGE_PIXELS
    
    @staticmethod
    def convert_to_hdr(img: Image.Image) -> Image.Image:
        """Converte imagem para HDR (simulado)"""
        img_array = np.array(img.convert("RGB"), dtype=np.float32) / 255.0
        
        # Aplica curva de tonemapping para HDR
        img_array = np.power(img_array, 0.7)
        img_array = np.clip(img_array * 1.2, 0, 1)
        
        # Converte para 16 bits
        hdr_array = (img_array * 65535).astype(np.uint16)
        return Image.fromarray(hdr_array, mode="RGB;16")
    
    @staticmethod
    def apply_filters_to_transparent(base_image: Image.Image, filters_config: Dict[str, Any]) -> Image.Image:
        """Aplica filtros a uma imagem transparente preservando o canal alpha"""
        # Cria uma cópia para não modificar a original
        img = base_image.copy()
        
        # Separa o canal alpha
        alpha = img.split()[3] if img.mode == 'RGBA' else None
        
        # Converte para RGB para aplicar os filtros (que esperam imagens RGB)
        rgb_img = img.convert('RGB')
        
        # Aplica os filtros
        filtered_img = ImageProcessor.apply_filters(rgb_img, filters_config)
        
        # Se havia transparência, mantém o canal alpha original
        if alpha:
            # Converte a imagem filtrada de volta para RGBA
            filtered_img = filtered_img.convert('RGBA')
            # Coloca o canal alpha original de volta
            filtered_img.putalpha(alpha)
        
        return filtered_img

    @staticmethod
    def resize_large_image(img: Image.Image) -> Image.Image:
        """Redimensiona imagens grandes mantendo a proporção"""
        if not ImageProcessor.check_image_size(img):
            # Calcula o fator de escala para ficar abaixo do limite
            scale_factor = (MAX_IMAGE_PIXELS / (img.width * img.height)) ** 0.5
            new_width = int(img.width * scale_factor)
            new_height = int(img.height * scale_factor)
            
            return img.resize((new_width, new_height), Image.LANCZOS)
        return img
    
    @staticmethod
    def apply_3d_effect_optimized(img: Image.Image, depth: int = 10) -> Image.Image:
        """Versão otimizada do efeito 3D usando numpy"""
        img_array = np.array(img)
        height, width = img_array.shape[:2]
        
        # Cria mapa de profundidade simplificado
        depth_map = np.linspace(0, depth, width).astype(np.float32)
        depth_map = np.tile(depth_map, (height, 1))
        
        # Aplica deslocamento
        shift = (depth_map * 0.1).astype(np.int32)
        shifted = np.zeros_like(img_array)
        
        for y in range(height):
            shifted[y, shift[y]:] = img_array[y, :width-shift[y]]
        
        return Image.fromarray(shifted)
    
    # Exemplo de melhoria na função load_image
    @staticmethod
    def load_image(uploaded_file=None) -> Image.Image:
        """Carrega imagem do upload ou usa exemplo padrão (atualizado)"""
        if uploaded_file is not None:
            try:
                # Verificar tipo MIME além da extensão
                if uploaded_file.type not in ["image/jpeg", "image/png", "image/webp"]:
                    raise ValueError("Tipo de arquivo não suportado")
                    
                # Verificar tamanho do arquivo
                max_size = 50 * 1024 * 1024  # 50MB
                if uploaded_file.size > max_size:
                    raise ValueError("Arquivo muito grande (máximo 50MB)")
                    
                img = Image.open(uploaded_file)
                img = ImageProcessor.resize_large_image(img)
                return img
            except Exception as e:
                st.error(f"Erro ao carregar imagem: {str(e)}")
                return ImageProcessor.load_sample_image()
        return ImageProcessor.load_sample_image()
    
    @staticmethod
    def apply_vintage_effect(img: Image.Image, intensity: int, vignette: int, grain: int) -> Image.Image:
        """Versão super otimizada do efeito vintage com numpy"""
        img_array = np.array(img.convert("RGB"), dtype=np.float32) / 255.0
        intensity_factor = intensity / 100.0
        
        # Efeito Sépia (vetorizado)
        if intensity > 0:
            sepia_matrix = np.array([
                [0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]
            ])
            sepia = np.dot(img_array, sepia_matrix.T)
            img_array = img_array * (1 - intensity_factor) + sepia * intensity_factor
            img_array = np.clip(img_array, 0, 1)
        
        # Efeito de Vinheta (otimizado com numpy)
        if vignette > 0:
            height, width = img_array.shape[:2]
            x = np.linspace(-1, 1, width)
            y = np.linspace(-1, 1, height)
            X, Y = np.meshgrid(x, y)
            vignette_mask = 1 - np.sqrt(X**2 + Y**2) * (vignette / 100.0 * 1.5)
            vignette_mask = np.clip(vignette_mask, 0, 1)[:,:,np.newaxis]
            img_array *= vignette_mask
        
        # Efeito de Granulação (vetorizado)
        if grain > 0:
            noise = np.random.randint(-grain, grain, img_array.shape[:2] + (3,), dtype=np.int16)
            img_array = np.clip((img_array * 255 + noise), 0, 255) / 255.0
        
        return Image.fromarray((img_array * 255).astype(np.uint8))
    
    @staticmethod
    def apply_color_tint(img: Image.Image, tint_color: Tuple[int, int, int], intensity: float) -> Image.Image:
        """Aplica tom de cor de forma otimizada"""
        tint_layer = Image.new('RGB', img.size, tint_color)
        return Image.blend(img.convert("RGB"), tint_layer, intensity)
    
    @staticmethod
    def apply_glow_effect(img: Image.Image, glow_intensity: int, neon_intensity: int, scanlines: int = 0) -> Image.Image:
        """Efeito de brilho e neon com OpenCV para melhor performance"""
        if glow_intensity <= 0 and neon_intensity <= 0 and scanlines <= 0:
            return img
        
        img_array = np.array(img.convert("RGB"), dtype=np.float32)
        
        # Efeito Glow
        if glow_intensity > 0:
            blurred = cv2.GaussianBlur(img_array, (0, 0), glow_intensity/10)
            img_array = cv2.addWeighted(img_array, 1, blurred, glow_intensity/100, 0)
        
        # Efeito Neon
        if neon_intensity > 0:
            edges = cv2.Laplacian(img_array, -1, ksize=3)
            edges = cv2.cvtColor(edges, cv2.COLOR_RGB2GRAY)
            edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            neon_color = np.array([255, 0, 255], dtype=np.float32)  # Magenta
            colored_edges = edges * (neon_color / 255)
            img_array = cv2.addWeighted(img_array, 1, colored_edges, neon_intensity/100, 0)
        
        # Efeito Scanlines
        if scanlines > 0:
            height, width = img_array.shape[:2]
            for y in range(0, height, 2):
                img_array[y:y+1, :] *= 1 - (scanlines/100)
        
        return Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))
    
    @staticmethod
    @st.cache_data(show_spinner=False, max_entries=5, ttl=3600)
    def apply_filters_cached(image: Image.Image, filters_config: Dict[str, Any]) -> Image.Image:
        """Versão em cache da aplicação de filtros"""
        return ImageProcessor.apply_filters(image, filters_config)
    
    @staticmethod
    def remove_artifacts(image: Image.Image, threshold: int = 10) -> Image.Image:
        """Remove artefatos visuais e sujeira da imagem"""
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
            
        # Cria uma máscara para pixels quase transparentes
        alpha = image.split()[3]
        mask = Image.eval(alpha, lambda a: 0 if a < threshold else 255)
        
        # Aplica a máscara para limpar artefatos
        cleaned = image.copy()
        cleaned.putalpha(mask)
        
        return cleaned
    
    @staticmethod
    def apply_filters(image: Image.Image, filters_config: Dict[str, Any]) -> Image.Image:
        """Aplica filtros com limpeza intermediária"""
        img = image.copy().convert("RGB")  # Garantia inicial de RGB

        # 🔴 Novo filtro de sobreposição de cor
        if "Sobreposição" in filters_config:
            params = filters_config["Sobreposição"]
            color = params.get("cor", (255, 0, 0))  # Vermelho padrão
            opacity = params.get("opacidade", 0.5)  # 50% padrão

            # Trabalha em RGBA para permitir transparência
            img_rgba = img.convert("RGBA")
            overlay = Image.new('RGBA', img_rgba.size, color)

            # Ajusta a opacidade
            alpha = overlay.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            overlay.putalpha(alpha)

            # Combina com a imagem base
            img_rgba = Image.alpha_composite(img_rgba, overlay)
            img = img_rgba.convert("RGB")  # Converte de volta para RGB para compatibilidade

        # 🎞️ Preto e Branco
        if "Preto e Branco" in filters_config:
            params = filters_config["Preto e Branco"]
            img = ImageOps.grayscale(img).convert("RGB")
            tons_value = params.get("tons", 50)
            if isinstance(tons_value, str):
                tons_value = {"Mais escuro": 25, "Mais claro": 75}.get(tons_value, 50)

            if tons_value != 50:
                lut = []
                for i in range(256):
                    if tons_value < 50:
                        val = int(i * (tons_value / 50))
                    else:
                        val = int(255 - (255 - i) * ((100 - tons_value) / 50))
                    lut.append(val)
                img = img.point(lut * 3)

            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(params.get("contraste", 1.2))

            if params.get("textura", 0) > 0:
                texture = params["textura"] / 30.0
                img_array = np.array(img, dtype=np.float32)
                noise = np.random.normal(0, texture * 25, img_array.shape)
                img_array = np.clip(img_array + noise, 0, 255)
                img = Image.fromarray(img_array.astype(np.uint8))

        # 🎨 Realça Cores
        if "Realça Cores" in filters_config:
            params = filters_config["Realça Cores"]
            img = ImageEnhance.Color(img).enhance(params.get("intensidade", 1.5))

            if params.get("seletividade", 50) != 50:
                hsv = np.array(img.convert("HSV"))
                sel = params["seletividade"]
                if sel > 50:
                    threshold = 128 * (sel - 50) / 50
                    mask = hsv[:, :, 1] > threshold
                    hsv[:, :, 1][mask] = np.clip(hsv[:, :, 1][mask] * 1.2, 0, 255)
                else:
                    threshold = 128 * (50 - sel) / 50
                    mask = hsv[:, :, 1] < threshold
                    hsv[:, :, 1][mask] = np.clip(hsv[:, :, 1][mask] * 1.5, 0, 255)
                img = Image.fromarray(hsv, mode="HSV").convert("RGB")

        # 💧 Azulado
        if "Azulado" in filters_config:
            params = filters_config["Azulado"]
            img = ImageProcessor.apply_color_tint(img, (135, 206, 250), params.get("intensidade", 50) / 200.0)
            img = ImageEnhance.Brightness(img).enhance(1 + (params.get("brilho", 0) / 100.0))

            if params.get("matiz", 0) != 0:
                hsv = np.array(img.convert("HSV"))
                hsv[:, :, 0] = (hsv[:, :, 0] + params["matiz"]) % 256
                img = Image.fromarray(hsv, mode="HSV").convert("RGB")

        # 🌿 Esverdeado
        if "Esverdeado" in filters_config:
            params = filters_config["Esverdeado"]
            img = ImageProcessor.apply_color_tint(img, (144, 238, 144), params.get("intensidade", 50) / 200.0)
            img = ImageEnhance.Contrast(img).enhance(params.get("contraste", 1.1))

            if params.get("sombra", 0) != 0:
                img_array = np.array(img, dtype=np.float32)
                shadow_mask = img_array.mean(axis=2) < 128
                img_array[shadow_mask] = np.clip(img_array[shadow_mask] + params["sombra"], 0, 255)
                img = Image.fromarray(img_array.astype(np.uint8))

        # 📸 Vintage
        if "Vintage" in filters_config:
            params = filters_config["Vintage"]
            img = ImageProcessor.apply_vintage_effect(
                img,
                intensidade=params.get("intensidade", 70),
                vinheta=params.get("vinheta", 40),
                granulacao=params.get("granulacao", 10),
            )

        # 🌌 Futurístico
        if "Futurístico" in filters_config:
            params = filters_config["Futurístico"]
            img = ImageProcessor.apply_glow_effect(
                img,
                glow=params.get("glow", 30),
                neon=params.get("neon", 20),
                scanlines=params.get("scanlines", 0),
            )

        # 🌈 Infravermelho
        if "Infravermelho" in filters_config:
            params = filters_config["Infravermelho"]
            img_array = np.array(img.convert("RGB"), dtype=np.float32)
            r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]
            img_array[:, :, 0] = np.clip(r * (1 + params["intensidade"] / 100) + g * 0.2 + b * 0.1, 0, 255)
            img_array[:, :, 1] = np.clip(g * 0.5 + b * 0.1, 0, 255)
            img_array[:, :, 2] = np.clip(b * 0.3, 0, 255)
            if params.get("brilho", 0) != 0:
                img_array = np.clip(img_array + params["brilho"], 0, 255)
            img = Image.fromarray(img_array.astype(np.uint8))

        return ImageProcessor.remove_artifacts(img)
    
    @staticmethod
    def create_transparent_layer(size: Tuple[int, int], opacity: float = 0.5) -> Image.Image:
        """Cria uma camada transparente para sobreposição"""
        return Image.new('RGBA', size, (0, 0, 0, int(255 * opacity)))

    @staticmethod
    def apply_transparent_overlay(base_image: Image.Image, overlay: Image.Image, opacity: float = 0.5) -> Image.Image:
        """Aplica uma sobreposição transparente na imagem base"""
        if overlay.mode != 'RGBA':
            overlay = overlay.convert('RGBA')
        
        # Ajusta a opacidade da sobreposição
        overlay_with_opacity = ImageEnhance.Brightness(overlay).enhance(opacity)
        
        # Combina as imagens mantendo a transparência
        return Image.alpha_composite(base_image.convert('RGBA'), overlay_with_opacity)
    
    @staticmethod
    def process_layers(base_image: Image.Image, layers_config: List[Dict[str, Any]]) -> Image.Image:
        """
        Processa múltiplas camadas sobre a imagem base com suporte a transparência
        Args:
            base_image: Imagem base (deve ter canal alpha se for transparente)
            layers_config: Lista de configurações de camadas [
                {
                    "image": Image.Image,  # Imagem da camada
                    "position": (x, y),    # Posição de sobreposição
                    "opacity": 0.5,        # Opacidade (0-1)
                    "blend_mode": "normal" # Modo de mesclagem
                }
            ]
        """
        result = base_image.convert('RGBA')
        
        for layer in layers_config:
            if not layer.get("image"):
                continue
                
            layer_img = layer["image"].convert('RGBA')
            
            # Aplica opacidade
            if layer.get("opacity", 1) < 1:
                alpha = layer_img.split()[3]
                alpha = ImageEnhance.Brightness(alpha).enhance(layer["opacity"])
                layer_img.putalpha(alpha)
            
            # Posiciona a camada
            position = layer.get("position", (0, 0))
            result.paste(layer_img, position, layer_img)
        
        return result

    @staticmethod
    def apply_frame(image: Image.Image, frame_config: Dict[str, Any]) -> Image.Image:
        """Aplica moldura com efeitos mais realistas e otimizados"""
        if frame_config["tipo"] == "Nenhuma":
            return image
        
        img = image.copy().convert("RGBA")
        width, height = img.size
        frame_type = frame_config["tipo"]
        color = frame_config["cor"]
        thickness = frame_config["espessura"]
        style = frame_config.get("estilo", "Simples")
        
        # Cria camada de moldura
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        if frame_type == "Janela":
            # Moldura principal
            draw.rectangle([(0, 0), (width-1, height-1)], 
                          outline=color, width=thickness)
            
            if style == "Clássico":
                # Divisórias
                draw.line([(width//2, 0), (width//2, height)], 
                          fill=color, width=thickness//2)
                draw.line([(0, height//2), (width, height//2)], 
                          fill=color, width=thickness//2)
            elif style == "Vitral":
                # Efeito de vitral
                for i in range(0, width, 30):
                    draw.line([(i, 0), (i, height)], 
                              fill=color, width=1)
                for i in range(0, height, 30):
                    draw.line([(0, i), (width, i)], 
                              fill=color, width=1)
        
        elif frame_type == "Smartphone":
            # Moldura arredondada
            radius = min(width, height) // 8
            draw.rounded_rectangle([(thickness//2, thickness//2), 
                                  (width-thickness//2, height-thickness//2)],
                                 radius=radius, outline=color, width=thickness)
            
            if style in ["iPhone", "Notch"]:
                # Notch superior
                notch_width, notch_height = width//5, thickness*2
                draw.rectangle([(width//2 - notch_width//2, 0),
                              (width//2 + notch_width//2, notch_height)],
                             fill=color)
        
        elif frame_type == "Neon":
            # Efeito neon com brilho
            for i in range(thickness, 0, -1):
                alpha = int(255 * (i/thickness)**0.5)
                neon_color = (*ImageColor.getrgb(color), alpha)
                draw.rectangle([(i, i), (width-i, height-i)], 
                              outline=neon_color, width=1)
            
            if style == "Pulsante":
                # Efeito de pulsação
                for i in range(1, thickness+1, 2):
                    alpha = int(255 * (i/thickness)**2)
                    neon_color = (*ImageColor.getrgb(color), alpha)
                    draw.rectangle([(i, i), (width-i, height-i)], 
                                  outline=neon_color, width=1)
            elif style == "RGB":
                # Efeito RGB alternado
                colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
                for i in range(thickness):
                    rgb_color = colors[i % 3]
                    alpha = int(255 * ((thickness-i)/thickness))
                    neon_color = (*rgb_color, alpha)
                    draw.rectangle([(i, i), (width-i, height-i)], 
                                  outline=neon_color, width=1)
        
        elif frame_type == "Câmera":
            # Moldura de câmera fotográfica
            if style == "Polaroid":
                # Efeito Polaroid (borda branca grossa na parte inferior)
                border_bottom = thickness * 3
                draw.rectangle([(0, 0), (width-1, height-1)], 
                            outline=color, width=thickness)
                draw.rectangle([(0, height-border_bottom), (width, height)], 
                            fill=color)
                
                # Adiciona texto simulado
                draw.text((width//4, height-border_bottom+10), "Foto Polaroid", 
                        fill=(0, 0, 0), font=None)
            
            elif style == "DSLR":
                # Efeito DSLR (borda preta com detalhes)
                draw.rounded_rectangle([(thickness//2, thickness//2), 
                                    (width-thickness//2, height-thickness//2)],
                                    radius=10, outline=color, width=thickness)
                
                # Detalhes da câmera
                lens_radius = min(width, height) // 4
                draw.ellipse([(width//2 - lens_radius, height//4 - lens_radius),
                            (width//2 + lens_radius, height//4 + lens_radius)],
                            outline=color, width=thickness//2)
                
                # Botão simulador
                draw.rectangle([(width - thickness*2, height//2 - thickness),
                            (width - thickness, height//2 + thickness)],
                            fill=color)
            
            elif style == "Vintage":
                # Efeito vintage (borda irregular)
                for i in range(thickness):
                    alpha = int(255 * (i/thickness)**0.5)
                    vintage_color = (*ImageColor.getrgb(color), alpha)
                    offset = random.randint(-2, 2)
                    draw.rectangle([(i+offset, i+offset), 
                                (width-i-offset, height-i-offset)],
                                outline=vintage_color, width=1)
        
        elif frame_type == "Lupa":
            # Efeito de lupa circular
            center_x, center_y = width//2, height//2
            radius = min(width, height)//2 - thickness
            
            # Desenha o círculo principal
            draw.ellipse([(center_x - radius, center_y - radius),
                        (center_x + radius, center_y + radius)],
                        outline=color, width=thickness)
            
            if style == "Científica":
                # Adiciona marcações de lupa científica
                for angle in range(0, 360, 30):
                    rad = math.radians(angle)
                    inner_x = center_x + int((radius - thickness) * math.cos(rad))
                    inner_y = center_y + int((radius - thickness) * math.sin(rad))
                    outer_x = center_x + int((radius + thickness) * math.cos(rad))
                    outer_y = center_y + int((radius + thickness) * math.sin(rad))
                    draw.line([(inner_x, inner_y), (outer_x, outer_y)], 
                            fill=color, width=thickness//3)
                
                # Adiciona alça
                handle_length = height // 3
                draw.rounded_rectangle([(center_x - thickness, center_y + radius),
                                    (center_x + thickness, center_y + radius + handle_length)],
                                    radius=thickness//2, fill=color)
            
            elif style == "Vintage":
                # Adiciona detalhes vintage
                for i in range(1, thickness+1, 2):
                    alpha = int(255 * (i/thickness)**2)
                    vintage_color = (*ImageColor.getrgb(color), alpha)
                    draw.ellipse([(center_x - radius - i, center_y - radius - i),
                                (center_x + radius + i, center_y + radius + i)],
                                outline=vintage_color, width=1)
        
        elif frame_type == "Portal":
            # Efeito de portal futurístico
            center_x, center_y = width//2, height//2
            radius = min(width, height)//2 - thickness
            
            if style == "Sci-fi":
                # Efeito sci-fi com anéis concêntricos
                for i in range(thickness, 0, -1):
                    alpha = int(255 * (i/thickness)**0.5)
                    portal_color = (*ImageColor.getrgb(color), alpha)
                    r = radius + i*2
                    draw.ellipse([(center_x - r, center_y - r),
                                (center_x + r, center_y + r)],
                                outline=portal_color, width=1)
                
                # Linhas diagonais
                for angle in range(0, 360, 45):
                    rad = math.radians(angle)
                    x1 = center_x + int(radius * 0.7 * math.cos(rad))
                    y1 = center_y + int(radius * 0.7 * math.sin(rad))
                    x2 = center_x + int(radius * 1.3 * math.cos(rad))
                    y2 = center_y + int(radius * 1.3 * math.sin(rad))
                    draw.line([(x1, y1), (x2, y2)], 
                            fill=color, width=thickness//2)
            
            elif style == "Mágico":
                # Efeito mágico com runas
                draw.ellipse([(center_x - radius, center_y - radius),
                            (center_x + radius, center_y + radius)],
                            outline=color, width=thickness)
                
                # Símbolos mágicos
                symbols = ["★", "✧", "✦", "✶", "✺"]
                for angle in range(0, 360, 45):
                    rad = math.radians(angle)
                    x = center_x + int(radius * 0.8 * math.cos(rad))
                    y = center_y + int(radius * 0.8 * math.sin(rad))
                    symbol = random.choice(symbols)
                    draw.text((x, y), symbol, fill=color, 
                            font=None, anchor="mm")
            
            elif style == "Glitch":
                # Efeito glitch com distorção
                for i in range(thickness):
                    offset = random.randint(-3, 3)
                    alpha = int(255 * (i/thickness)**0.7)
                    glitch_color = (*ImageColor.getrgb(color), alpha)
                    draw.ellipse([(center_x - radius - i + offset, center_y - radius - i),
                                (center_x + radius + i + offset, center_y + radius + i)],
                                outline=glitch_color, width=1)
        
        # Combina com a imagem original
        return Image.alpha_composite(img, overlay)
    
    @staticmethod
    def apply_glass_break_effect(img: Image.Image, intensity: int, break_type: str, style: str = "Realista") -> Image.Image:
        """Efeito de vidro quebrado otimizado"""
        width, height = img.size
        img_array = np.array(img.convert("RGB"), dtype=np.float32)
        
        # Gera máscara de quebra
        break_mask = np.zeros((height, width), dtype=np.float32)
        
        if break_type == "Radial":
            center_x, center_y = width//2, height//2
            for angle in np.linspace(0, 2*np.pi, intensity*5):
                length = random.randint(width//4, width//2)
                x2 = center_x + int(length * np.cos(angle))
                y2 = center_y + int(length * np.sin(angle))
                
                # Desenha linha na máscara
                cv2.line(break_mask, (center_x, center_y), (x2, y2), 1.0, 2)
        
        elif break_type == "Mosaico":
            tile_size = max(5, width // (intensity*2))
            for y in range(0, height, tile_size):
                for x in range(0, width, tile_size):
                    if random.random() > 0.7:
                        cv2.rectangle(break_mask, (x, y), (x+tile_size, y+tile_size), 1.0, -1)
        
        # Aplica distorção
        if style == "Realista":
            distortion = cv2.GaussianBlur(break_mask, (0,0), intensity)
            dx = distortion * (random.random()*20 - 10)
            dy = distortion * (random.random()*20 - 10)
            
            # Cria mapa de distorção
            map_x = np.tile(np.arange(width), (height, 1)).astype(np.float32)
            map_y = np.tile(np.arange(height), (width, 1)).T.astype(np.float32)
            
            map_x += dx * 5
            map_y += dy * 5
            
            # Aplica remapeamento
            broken_img = cv2.remap(img_array, map_x, map_y, cv2.INTER_LINEAR)
        else:
            # Efeito mais simples
            broken_img = img_array * (1 - break_mask[:,:,np.newaxis]/2)
        
        return Image.fromarray(np.clip(broken_img, 0, 255).astype(np.uint8))
    
    @staticmethod
    def apply_water_drops_effect(img: Image.Image, quantity: int, size: int, drop_type: str = "Água") -> Image.Image:
        """Efeito de gotas d'água otimizado"""
        width, height = img.size
        img_array = np.array(img.convert("RGB"), dtype=np.float32)
        
        # Cores baseadas no tipo de gota
        if drop_type == "Água":
            base_color = np.array([200, 200, 255])
        elif drop_type == "Óleo":
            base_color = np.array([200, 200, 200])
        else:  # Metálico
            base_color = np.array([200, 220, 255])
        
        for _ in range(quantity):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            drop_size = random.randint(size, size*2)
            
            # Cria gota circular
            for dy in range(-drop_size, drop_size):
                for dx in range(-drop_size, drop_size):
                    if 0 <= x+dx < width and 0 <= y+dy < height:
                        dist = np.sqrt(dx**2 + dy**2)
                        if dist < drop_size:
                            # Efeito de refração
                            refr_x = x + int(dx * 0.5)
                            refr_y = y + int(dy * 0.5)
                            if 0 <= refr_x < width and 0 <= refr_y < height:
                                img_array[y+dy, x+dx] = img_array[refr_y, refr_x] * 0.7 + base_color * 0.3
        
        return Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))
    
    @staticmethod
    def apply_effects_to_transparent(base_image: Image.Image, config: Dict[str, Any]) -> Image.Image:
        """Aplica todos os efeitos a uma imagem transparente"""
        # Cria uma cópia para não modificar a original
        img = base_image.copy()
        
        # Aplica filtros (modificados para trabalhar com transparência)
        if config.get("filtros"):
            img = ImageProcessor.apply_filters_with_alpha(img, config["filtros"])
        
        # Aplica moldura
        if config.get("moldura", {}).get("tipo", "Nenhuma") != "Nenhuma":
            img = ImageProcessor.apply_frame(img, config["moldura"])
        
        # Aplica texto
        if config.get("texto"):
            img = TextProcessor.apply_text_effect(img, config)
        
        return img
    
    @staticmethod
    def apply_filters_with_alpha(image: Image.Image, filters_config: Dict[str, Any]) -> Image.Image:
        """Versão modificada dos filtros que preserva transparência"""
        # Cria uma camada temporária para os filtros
        filter_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
        
        # Preenche com branco semi-transparente para aplicar os filtros
        base = Image.new('RGBA', image.size, (255, 255, 255, 128))
        
        # Aplica os filtros normais
        filtered = ImageProcessor.apply_filters(base.convert('RGB'), filters_config).convert('RGBA')
        
        # Ajusta a transparência baseada no alpha original
        r, g, b, a = filtered.split()
        filtered = Image.merge('RGBA', (r, g, b, a))
        
        # Combina com a camada de filtros
        filter_layer = Image.alpha_composite(filter_layer, filtered)
        
        # Combina com a imagem original
        return Image.alpha_composite(image, filter_layer)

# ======================================================================================
# FUNÇÕES DE ANIMAÇÃO E EXPORTAÇÃO
# ======================================================================================

class AnimationExporter:
    """Gerencia a exportação de animações e presets"""
    
    @staticmethod
    def generate_animation_instructions(animation_config: Dict[str, Any]) -> Dict[str, Any]:
        """Gera instruções detalhadas para criar animações"""
        instructions = {
            "clipchamp": ["### Instruções para Clipchamp"],
            "capcut": ["### Instruções para CapCut"],
            "manual": ["### Instruções para Editores Profissionais"]
        }
        
        for anim_name, anim_params in animation_config.items():
            if anim_name == "Girar":
                direction = anim_params.get("direcao", "Horário")
                speed = anim_params.get("velocidade", 5)
                axis = anim_params.get("eixo", "XY")
                
                instructions["clipchamp"].append(
                    f"- Adicione o efeito 'Rotação' e defina:\n"
                    f"  • Direção: {'direita' if direction == 'Horário' else 'esquerda'}\n"
                    f"  • Eixo: {axis}\n"
                    f"  • Velocidade: {speed}/10"
                )
                
                instructions["capcut"].append(
                    f"- Selecione o clipe > Efeitos > Movimento > Rotação\n"
                    f"  • Tipo: {'positiva' if direction == 'Horário' else 'negativa'}\n"
                    f"  • Eixo: {axis}\n"
                    f"  • Duração: {2/speed:.1f}s"
                )
                
                instructions["manual"].append(
                    f"- Keyframes de rotação ({axis}):\n"
                    f"  • 0s: 0°\n"
                    f"  • {2/speed:.1f}s: {360 if direction == 'Horário' else -360}°"
                )
            
            elif anim_name == "Vidro Quebrando":
                intensity = anim_params.get("intensidade", 5)
                break_type = anim_params.get("tipo_quebra", "Radial")
                sound = anim_params.get("som", "Não")
                style = anim_params.get("estilho", "Realista")
                
                instructions["clipchamp"].append(
                    f"- Adicione o efeito 'Glass Break' e ajuste:\n"
                    f"  • Intensidade: {intensity}/10\n"
                    f"  • Tipo: {break_type}\n"
                    f"  • Estilo: {style}"
                )
                
                instructions["manual"].append(
                    f"- Aplique o efeito 'Glass Break' ou 'Shatter' com:\n"
                    f"  • Força: {intensity*10}%\n"
                    f"  • Padrão: {break_type}\n"
                    f"  • Estilo: {style}"
                )
                
                if sound == "Sim":
                    instructions["manual"].append(
                        f"- Sincronize com o som de vidro quebrando no frame chave"
                    )
        
        return instructions
    
    @staticmethod
    def generate_lut_cube(filters_config: Dict[str, Any], size: int = 33) -> str:
        """Gera arquivo LUT 3D baseado nos filtros aplicados"""
        # Cria uma imagem de gradiente que representa todas as cores
        gradient = Image.new('RGB', (size*size, size))
        pixels = gradient.load()
        
        for i in range(size*size):
            for j in range(size):
                r = int((i // size) * 255 / (size-1))
                g = int((i % size) * 255 / (size-1))
                b = int(j * 255 / (size-1))
                pixels[i, j] = (r, g, b)
                
        # Aplica os filtros na imagem de gradiente
        transformed_gradient = ImageProcessor.apply_filters(gradient, filters_config)
        
        # Gera o arquivo .cube
        lines = [
            'TITLE "Filtro Gerado por Filtros Pro"',
            f'LUT_3D_SIZE {size}',
            'DOMAIN_MIN 0.0 0.0 0.0',
            'DOMAIN_MAX 1.0 1.0 1.0',
            ''
        ]
        
        transformed_pixels = transformed_gradient.load()
        for b_idx in range(size):
            for g_idx in range(size):
                for r_idx in range(size):
                    x = r_idx * size + g_idx
                    y = b_idx
                    r, g, b = transformed_pixels[x, y]
                    lines.append(f"{r/255.0:.6f} {g/255.0:.6f} {b/255.0:.6f}")
                    
        return "\n".join(lines)
    
    @staticmethod
    def generate_preset_file(config: Dict[str, Any], platform: str) -> str:
        """Gera um arquivo de preset para plataformas específicas"""
        preset = {
            "metadata": {
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "generator": "Filtros Pro Super Edition",
                "version": "2.1",
                "platform": platform
            },
            "filters": {},
            "frames": {},
            "animations": {}
        }
        
        # Filtros
        for filter_name, params in config.get("filtros", {}).items():
            preset["filters"][filter_name] = {
                "type": filter_name.lower(),
                "params": params
            }
        
        # Molduras
        if config.get("moldura", {}).get("tipo", "Nenhuma") != "Nenhuma":
            preset["frames"] = {
                "type": config["moldura"]["tipo"].lower(),
                "color": config["moldura"]["cor"],
                "thickness": config["moldura"]["espessura"],
                "style": config["moldura"].get("estilo", "simple")
            }
        
        # Animações
        for anim_name, params in config.get("animacao", {}).items():
            if anim_name not in ["duracao", "repetir"]:  # Ignora configurações gerais
                preset["animations"][anim_name] = {
                    "type": anim_name.lower(),
                    "params": params
                }
        
        # Configurações gerais
        if "animacao" in config:
            preset["animation_settings"] = {
                "duration": config["animacao"].get("duracao", 2.0),
                "repeat": config["animacao"].get("repetir", "Nenhuma")
            }
        
        return json.dumps(preset, indent=2, ensure_ascii=False)
    
class AnimationPreviewer:
    """Classe para pré-visualização de animações"""
    
    @staticmethod
    def generate_animation_frames(image: Image.Image, 
                                animation_config: Dict[str, Any], 
                                duration: float) -> List[Image.Image]:
        """Gera frames de animação em alta qualidade"""
        frames = []
        
        try:
            # Mantém o tamanho original da imagem base
            original_size = image.size
            
            # Configura número de frames baseado na duração (24fps padrão)
            num_frames = min(60, int(duration * 24))  # Máximo de 60 frames
            
            for frame_num in range(num_frames):
                progress = frame_num / (num_frames - 1) if num_frames > 1 else 0
                
                # Cria uma cópia em alta qualidade
                frame_img = image.copy().convert("RGBA")
                
                # Redimensiona apenas se necessário, mantendo a qualidade
                if frame_img.size != original_size:
                    frame_img = frame_img.resize(original_size, Image.LANCZOS)
                
                # Aplica efeitos de animação
                for anim_name, anim_params in animation_config.items():
                    if anim_name not in ["duracao", "repetir"]:
                        frame_img = AnimationPreviewer.apply_animation_effect(
                            frame_img, anim_name, anim_params, progress, duration
                        )
                
                # Garante que o frame está no tamanho e qualidade corretos
                if frame_img.size != original_size:
                    frame_img = frame_img.resize(original_size, Image.LANCZOS)
                
                frames.append(frame_img)
            
            return frames
        
        except Exception as e:
            st.error(f"Erro ao gerar frames em alta qualidade: {str(e)}")
            return [image]  # Fallback
    
    @staticmethod
    def apply_animation_effect(img: Image.Image, anim_name: str, anim_params: Dict[str, Any], progress: float, duration: float) -> Image.Image:
        """Aplica um único efeito de animação em um frame específico"""
        if anim_name == "Girar":
            return AnimationPreviewer.apply_rotation_effect(img, anim_params, progress)
        elif anim_name == "Zoom":
            return AnimationPreviewer.apply_zoom_effect(img, anim_params, progress)
        elif anim_name == "Deslizar":
            return AnimationPreviewer.apply_slide_effect(img, anim_params, progress)
        elif anim_name == "Piscar":
            return AnimationPreviewer.apply_blink_effect(img, anim_params, progress)
        elif anim_name == "Pixelar":
            return AnimationPreviewer.apply_pixelate_effect(img, anim_params, progress)
        elif anim_name == "Vidro Quebrando":
            return ImageProcessor.apply_glass_break_effect(img, 
                anim_params.get("intensidade", 5),
                anim_params.get("tipo_quebra", "Radial"),
                anim_params.get("estilho", "Realista")
            )
        elif anim_name == "Gotas d'Água":
            return ImageProcessor.apply_water_drops_effect(img,
                anim_params.get("quantidade", 8),
                anim_params.get("tamanho", 2),
                anim_params.get("tipo", "Água")
            )
        elif anim_name == "Glitch":
            return AnimationPreviewer.apply_glitch_effect(img, anim_params, progress)
        
        return img
    
    @staticmethod
    def apply_rotation_effect(img: Image.Image, params: Dict[str, Any], progress: float) -> Image.Image:
        """Aplica efeito de rotação"""
        direction = 1 if params.get("direcao", "Horário") == "Horário" else -1
        speed = params.get("velocidade", 5)
        angle = 360 * progress * direction * (speed / 5)
        
        # Rotaciona a imagem
        return img.rotate(angle, expand=True, resample=Image.BILINEAR)
    
    @staticmethod
    def apply_zoom_effect(img: Image.Image, params: Dict[str, Any], progress: float) -> Image.Image:
        """Aplica efeito de zoom"""
        zoom_type = params.get("tipo", "In")
        intensity = params.get("intensidade", 2)
        
        if zoom_type == "In":
            scale = 1 + (intensity / 5) * progress
        elif zoom_type == "Out":
            scale = 1 + (intensity / 5) * (1 - progress)
        else:  # Pulsar ou Aleatório
            scale = 1 + (intensity / 10) * math.sin(progress * math.pi * 2)
        
        # Redimensiona a imagem
        width, height = img.size
        new_size = (int(width * scale), int(height * scale))
        return img.resize(new_size, Image.LANCZOS)
    
    @staticmethod
    def apply_slide_effect(img: Image.Image, params: Dict[str, Any], progress: float) -> Image.Image:
        """Aplica efeito de deslize"""
        direction = params.get("direcao", "Esquerda")
        width, height = img.size
        
        # Calcula o deslocamento baseado na direção
        if direction == "Esquerda":
            offset = (int(-width * progress), 0)
        elif direction == "Direita":
            offset = (int(width * progress), 0)
        elif direction == "Cima":
            offset = (0, int(-height * progress))
        elif direction == "Baixo":
            offset = (0, int(height * progress))
        else:  # Diagonal
            offset = (int(width * progress), int(height * progress))
        
        # Cria uma nova imagem com o deslocamento
        new_img = Image.new("RGBA", (width, height))
        new_img.paste(img, offset)
        return new_img
    
    @staticmethod
    def apply_blink_effect(img: Image.Image, params: Dict[str, Any], progress: float) -> Image.Image:
        """Aplica efeito de piscar"""
        times = params.get("vezes", 3)
        intensity = params.get("intensidade", 50) / 100
        
        # Calcula o estado atual (piscando ou não)
        blink_progress = (progress * times) % 1
        if blink_progress < 0.2:  # 20% do tempo piscando
            alpha = int(255 * (1 - intensity))
            overlay = Image.new("RGBA", img.size, (0, 0, 0, alpha))
            return Image.alpha_composite(img.convert("RGBA"), overlay)
        
        return img
    
    @staticmethod
    def apply_pixelate_effect(img: Image.Image, params: Dict[str, Any], progress: float) -> Image.Image:
        """Aplica efeito de pixelização"""
        size = params.get("tamanho", 10)
        direction = params.get("direcao", "In")
        
        if direction == "In":
            pixel_size = int(size * (1 - progress))
        elif direction == "Out":
            pixel_size = int(size * progress)
        else:  # Aleatório
            pixel_size = random.randint(1, size)
        
        if pixel_size <= 1:
            return img
        
        # Redimensiona para menor e volta para criar o efeito pixelado
        small = img.resize(
            (img.width // pixel_size, img.height // pixel_size),
            resample=Image.NEAREST
        )
        return small.resize(img.size, Image.NEAREST)
    
    @staticmethod
    def apply_glitch_effect(img: Image.Image, params: Dict[str, Any], progress: float) -> Image.Image:
        """Aplica efeito glitch"""
        intensity = params.get("intensidade", 5)
        img_array = np.array(img)
        
        # Aplica deslocamento aleatório em algumas linhas
        for i in range(0, img.height, random.randint(5, 20)):
            shift = random.randint(-intensity, intensity)
            if shift != 0:
                img_array[i,:] = np.roll(img_array[i,:], shift, axis=0)
        
        return Image.fromarray(img_array)
    
# ======================================================================================
# NOVAS FUNÇÕES DE EXPORTAÇÃO MODULAR
# ======================================================================================

class ModularExporter:
    """Classe para exportação modular de configurações"""
    
    @staticmethod
    def export_module(module_type: str, config: Dict[str, Any], export_format: str) -> Tuple[bytes, str, str]:
        """Exporta um módulo específico com limpeza"""
        # Adicione esta linha no início da função:
        config["clean_settings"] = {
            "active": True,
            "level": 5
        }
        """Exporta um módulo específico no formato selecionado - ATUALIZADA"""
        if module_type == "moldura" and config.get("moldura", {}).get("tipo", "Nenhuma") == "Nenhuma":
            return None, None, None
            
        if module_type == "filtros" and not config.get("filtros"):
            return None, None, None
            
        if module_type == "animacao" and not any(k not in ["duracao", "repetir"] for k in config.get("animacao", {}).keys()):
            return None, None, None
            
        if module_type == "texto" and not config.get("texto"):
            return None, None, None
        
        # Cria imagem transparente para exportação de efeitos
        transparent_img = Image.new('RGBA', (1024, 1024), (0, 0, 0, 0))
        
        if module_type == "moldura":
            # Exporta apenas a moldura sobre fundo transparente
            frame_img = ImageProcessor.apply_frame(transparent_img, config["moldura"])
            img_byte_arr = io.BytesIO()
            frame_img.save(img_byte_arr, format='PNG')
            return img_byte_arr.getvalue(), "moldura.png", "image/png"
            
        elif module_type == "filtros":
            if export_format == "LUT":
                # Exporta LUT 3D
                lut_data = AnimationExporter.generate_lut_cube(config["filtros"])
                return lut_data.encode('utf-8'), "filtros_lut.cube", "text/plain"
            else:
                # Exporta filtros sobre fundo transparente
                # Cria uma imagem RGB simples (não transparente) para os filtros
                color_img = Image.new('RGB', (1024, 1024), (255, 255, 255))
                filtered_img = ImageProcessor.apply_filters(color_img, config["filtros"])
                
                # Se queremos transparente, convertemos para RGBA e tornamos branco transparente
                if export_format == "PNG":
                    filtered_img = filtered_img.convert('RGBA')
                    data = filtered_img.getdata()
                    new_data = []
                    for item in data:
                        # Torna pixels brancos totalmente transparentes
                        if item[:3] == (255, 255, 255):
                            new_data.append((255, 255, 255, 0))
                        else:
                            new_data.append(item)
                    filtered_img.putdata(new_data)
                
                img_byte_arr = io.BytesIO()
                if export_format == "PNG":
                    filtered_img.save(img_byte_arr, format='PNG')
                else:
                    # Para JPEG, garantimos que a imagem está em modo RGB
                    if filtered_img.mode == 'RGBA':
                        # Cria fundo branco para imagens com transparência
                        background = Image.new('RGB', filtered_img.size, (255, 255, 255))
                        background.paste(filtered_img, mask=filtered_img.split()[3])
                        filtered_img = background
                    filtered_img.save(img_byte_arr, format='JPEG', quality=95)
                    
                return img_byte_arr.getvalue(), f"filtros.{'png' if export_format == 'PNG' else 'jpg'}", f"image/{'png' if export_format == 'PNG' else 'jpeg'}"
                
        elif module_type == "animacao":
            # Exporta animação sobre fundo transparente
            frames = AnimationPreviewer.generate_animation_frames(
                transparent_img,
                config["animacao"],
                config["animacao"].get("duracao", 2.0)
            )
            gif_bytes = io.BytesIO()
            frames[0].save(
                gif_bytes,
                format='GIF',
                append_images=frames[1:],
                save_all=True,
                duration=int(config["animacao"].get("duracao", 2.0) * 1000 / len(frames)),
                loop=0,
                transparency=0
            )
            return gif_bytes.getvalue(), "animacao.gif", "image/gif"
            
        elif module_type == "texto":
            # Verifica se há animações de texto para exportar como GIF/MP4
            if export_format in ["GIF", "MP4"] and config.get("animacao_texto"):
                if export_format == "GIF":
                    frames = TextProcessor.generate_text_animation_frames(
                        transparent_img,
                        config,
                        config["animacao_texto"],
                        config["animacao_texto"].get("duracao", 2.0)
                    )
                    gif_bytes = io.BytesIO()
                    frames[0].save(
                        gif_bytes,
                        format='GIF',
                        append_images=frames[1:],
                        save_all=True,
                        duration=int(config["animacao_texto"].get("duracao", 2.0) * 1000 / len(frames)),
                        loop=0,
                        transparency=0
                    )
                    return gif_bytes.getvalue(), "texto_animado.gif", "image/gif"
                else:  # MP4
                    temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
                    temp_file.close()
                    
                    frames = TextProcessor.generate_text_animation_frames(
                        transparent_img,
                        config,
                        config["animacao_texto"],
                        config["animacao_texto"].get("duracao", 2.0)
                    )
                    
                    # Salva como GIF primeiro
                    gif_file = tempfile.NamedTemporaryFile(suffix=".gif", delete=False)
                    frames[0].save(
                        gif_file.name,
                        format='GIF',
                        append_images=frames[1:],
                        save_all=True,
                        duration=int(config["animacao_texto"].get("duracao", 2.0) * 1000 / len(frames)),
                        loop=0
                    )
                    
                    # Converte para MP4
                    subprocess.run([
                        'ffmpeg', '-y', '-i', gif_file.name,
                        '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                        temp_file.name
                    ], check=True)
                    
                    with open(temp_file.name, 'rb') as f:
                        video_data = f.read()
                    
                    return video_data, "texto_animado.mp4", "video/mp4"
            else:
                # Exporta texto estático sobre fundo transparente
                text_img = TextProcessor.apply_text_effect(transparent_img, {
                    "texto": config["texto"],
                    "fonte": config.get("fonte", {}),
                    "posicao": config.get("posicao", {}),
                    "contorno": config.get("contorno", {})
                })
                img_byte_arr = io.BytesIO()
                text_img.save(img_byte_arr, format='PNG')
                return img_byte_arr.getvalue(), "texto.png", "image/png"
            
        return None, None, None
    
    @staticmethod
    def export_video_preset(config: Dict[str, Any], platform: str) -> str:
        """Gera preset para vídeo com instruções específicas"""
        preset = {
            "metadata": {
                "type": "video_preset",
                "platform": platform,
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "filters": config.get("filtros", {}),
            "frame": config.get("moldura", {}),
            "instructions": VideoProcessor.generate_platform_instructions(platform)
        }
        return json.dumps(preset, indent=2)
    
    @staticmethod
    def export_all(config: Dict[str, Any], 
                 format: str,
                 quality_settings: Dict[str, str] = None) -> Tuple[bytes, str, str]:
        """Exporta todos os efeitos com controle de qualidade"""
        if quality_settings is None:
            quality_settings = {"quality_level": "Alta", "output_size": "Original"}
            
        # Cria imagem base transparente
        size = {
            "Original": (1920, 1080),
            "HD (1280x720)": (1280, 720),
            "Full HD (1920x1080)": (1920, 1080)
        }[quality_settings["output_size"]]
        
        transparent_img = Image.new('RGBA', size, (0, 0, 0, 0))
        
        # Aplica efeitos
        processed_img = transparent_img.copy()
        if config.get("filtros"):
            processed_img = ImageProcessor.apply_filters_to_transparent(processed_img, config["filtros"])
        if config.get("moldura", {}).get("tipo", "Nenhuma") != "Nenhuma":
            processed_img = ImageProcessor.apply_frame(processed_img, config["moldura"])
        if config.get("texto"):
            processed_img = TextProcessor.apply_text_effect(processed_img, config)
        
        # Exporta no formato selecionado
        if format in ["PNG", "JPG"]:
            img_byte_arr = io.BytesIO()
            processed_img.save(
                img_byte_arr,
                format='PNG' if format == "PNG" else 'JPEG',
                quality=QualitySettings.get_preset(quality_settings["quality_level"])["quality"],
                subsampling=QualitySettings.get_preset(quality_settings["quality_level"])["subsampling"]
            )
            return img_byte_arr.getvalue(), f"all_effects.{format.lower()}", f"image/{format.lower()}"
        else:  # GIF ou MP4
            return AdvancedExporter.export_with_quality(
                processed_img,
                config,
                format.lower(),
                quality_settings["quality_level"],
                quality_settings["output_size"]
            ) + (f"image/{format.lower()}",)

# ======================================================================================
# ATUALIZAÇÃO DA INTERFACE DO USUÁRIO PARA INCLUIR A NOVA ABA DE TEXTO
# ======================================================================================

class FiltrosProUI:
    """Classe principal da interface do usuário (atualizada)"""
    
    @staticmethod
    def render_text_tab(config: Dict[str, Any]):
        """Renderiza a nova aba de texto e animações de texto"""
        with st.expander("✍️ CONFIGURAÇÕES DE TEXTO", expanded=True):
            # Configurações básicas de texto
            config["texto"] = st.text_area(
                "Digite seu texto aqui:",
                value="Texto de Exemplo",
                max_chars=100,
                help="Máximo de 100 caracteres"
            )
            
            # Configurações de fonte
            with st.expander("🔠 Configurações de Fonte"):
                col1, col2 = st.columns(2)
                
                with col1:
                    # Upload de fonte personalizada
                    uploaded_font = st.file_uploader(
                        "📤 Enviar Fonte Personalizada (TTF/OTF)",
                        type=["ttf", "otf"],
                        key="font_uploader"
                    )
                    
                    if uploaded_font:
                        # Salva a fonte temporariamente
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as tmp_file:
                            tmp_file.write(uploaded_font.read())
                            st.session_state.custom_font = tmp_file.name
                    
                    # Seleção do tipo de fonte
                    font_options = [
                        f"{TextEffectDatabase.FONT_DATABASE[name]['icon']} {name}" 
                        for name in TextEffectDatabase.FONT_DATABASE
                    ]
                    
                    # Adiciona fontes do sistema disponíveis
                    system_fonts = TextProcessor.get_available_fonts()
                    if system_fonts:
                        font_options.extend([f"📀 {font}" for font in system_fonts])
                    
                    selected_font = st.selectbox(
                        "Estilo da Fonte",
                        options=list(TextEffectDatabase.FONT_DATABASE.keys()) + system_fonts,
                        format_func=lambda x: (
                            f"{TextEffectDatabase.FONT_DATABASE[x]['icon']} {x}" 
                            if x in TextEffectDatabase.FONT_DATABASE 
                            else f"📀 {x}"
                        ),
                        index=0,
                        key="text_font_type"
                    )
                    
                    config["fonte"] = {
                        "tipo": selected_font,
                        "tamanho": st.slider(
                            "Tamanho da Fonte",
                            10, 72, 32,
                            help="Tamanho em pixels"
                        ),
                        "cor": st.color_picker(
                            "Cor do Texto",
                            "#FFFFFF",
                            key="text_color"
                        )
                    }
                    
                    # Configurações específicas da fonte
                    if selected_font in TextEffectDatabase.FONT_DATABASE:
                        font_info = TextEffectDatabase.FONT_DATABASE[selected_font]
                        for param_name, param_config in font_info["params"].items():
                            if isinstance(param_config, list):
                                config["fonte"][param_name] = st.radio(
                                    param_name.capitalize(),
                                    param_config,
                                    horizontal=True,
                                    key=f"font_{param_name}"
                                )
                            else:
                                config["fonte"][param_name] = st.slider(
                                    param_name.capitalize(),
                                    param_config["min"],
                                    param_config["max"],
                                    param_config["default"],
                                    param_config.get("step", 1),
                                    key=f"font_{param_name}"
                                )
                
                with col2:
                    # Visualização da fonte
                    preview_img = Image.new('RGB', (400, 150), (50, 50, 50))
                    preview_img = TextProcessor.apply_text_effect(preview_img, {
                        "texto": "AaBbCc123",
                        "fonte": config["fonte"],
                        "posicao": {"horizontal": "Centro", "vertical": "Meio"}
                    })
                    
                    st.image(
                        preview_img,
                        caption=f"Visualização: {selected_font}",
                        use_container_width=True
                    )
                    
                    # Descrição e dicas
                    if selected_font in TextEffectDatabase.FONT_DATABASE:
                        font_info = TextEffectDatabase.FONT_DATABASE[selected_font]
                        st.markdown(f"**{font_info['icon']} {selected_font}**")
                        st.markdown(font_info["desc"])
                    else:
                        st.markdown(f"**📀 {selected_font}**")
                        st.markdown("Fonte do sistema")
            
            # Configurações de posição
            with st.expander("📍 Posicionamento do Texto"):
                col1, col2 = st.columns(2)
                
                with col1:
                    config["posicao"] = {
                        "horizontal": st.radio(
                            "Posição Horizontal",
                            ["Esquerda", "Centro", "Direita"],
                            index=1,
                            horizontal=True
                        )
                    }
                
                with col2:
                    config["posicao"]["vertical"] = st.radio(
                        "Posição Vertical",
                        ["Topo", "Meio", "Base"],
                        index=1,
                        horizontal=True
                    )
            
            # Configurações de contorno
            with st.expander("🖍️ Contorno do Texto"):
                config["contorno"] = {
                    "ativo": st.checkbox("Adicionar contorno", value=False),
                    "cor": st.color_picker(
                        "Cor do Contorno",
                        "#000000",
                        key="outline_color"
                    ),
                    "espessura": st.slider(
                        "Espessura do Contorno",
                        1, 5, 1,
                        help="Espessura em pixels"
                    )
                }
                
        with st.expander("🔍 Pré-visualização de Fonte em Tempo Real", expanded=True):
            sample_text = st.text_input(
                "Texto de exemplo para pré-visualização:",
                value="AaBbCc123",
                key="font_preview_text"
            )
            
            # Atualização em tempo real
            preview_img = Image.new('RGB', (600, 200), (40, 40, 40))
            try:
                preview_img = TextProcessor.apply_text_effect(preview_img, {
                    "texto": sample_text,
                    "fonte": config["fonte"],
                    "posicao": {"horizontal": "Centro", "vertical": "Meio"}
                })
                st.image(preview_img, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao renderizar fonte: {str(e)}")
        
        # Animação de texto
        with st.expander("🎬 ANIMAÇÕES DE TEXTO", expanded=True):
            # Lista de animações de texto formatadas com ícones e complexidade
            animation_options = [
                f"{TextEffectDatabase.TEXT_ANIMATION_DATABASE[name]['icon']} {name} "
                f"({'⭐' * TextEffectDatabase.TEXT_ANIMATION_DATABASE[name]['complexity']})" 
                for name in TextEffectDatabase.TEXT_ANIMATION_DATABASE
            ]
            
            selected_text_animations = st.multiselect(
                "Selecione as animações de texto:",
                options=list(TextEffectDatabase.TEXT_ANIMATION_DATABASE.keys()),
                default=[],
                format_func=lambda x: (
                    f"{TextEffectDatabase.TEXT_ANIMATION_DATABASE[x]['icon']} {x} "
                    f"({'⭐' * TextEffectDatabase.TEXT_ANIMATION_DATABASE[x]['complexity']})"
                ),
                help="Selecione uma ou mais animações para aplicar ao texto"
            )
            
            # Configurações para cada animação de texto selecionada
            for anim_name in selected_text_animations:
                anim_info = TextEffectDatabase.TEXT_ANIMATION_DATABASE[anim_name]
                
                with st.expander(f"{anim_info['icon']} {anim_name}"):
                    config["animacao_texto"][anim_name] = {}
                    
                    for param_name, param_config in anim_info["params"].items():
                        # Controles diferentes baseados no tipo de parâmetro
                        if isinstance(param_config, list):
                            config["animacao_texto"][anim_name][param_name] = st.radio(
                                param_name.capitalize(),
                                param_config,
                                horizontal=True,
                                key=f"text_anim_{anim_name}_{param_name}"
                            )
                        else:
                            config["animacao_texto"][anim_name][param_name] = st.slider(
                                param_name.capitalize(),
                                param_config["min"],
                                param_config["max"],
                                param_config["default"],
                                param_config.get("step", 1),
                                key=f"text_anim_{anim_name}_{param_name}"
                            )
            
            # Configurações gerais de animação de texto
            if selected_text_animations:
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    config["animacao_texto"]["duracao"] = st.slider(
                        "Duração da Animação (segundos)",
                        0.5, 5.0, 2.0, 0.1,
                        key="text_anim_duration",
                        help="Duração total da animação de texto"
                    )
                
                with col2:
                    config["animacao_texto"]["repetir"] = st.selectbox(
                        "Repetição da Animação",
                        ["Nenhuma", "2 vezes", "Continuamente"],
                        key="text_anim_repeat",
                        help="Quantas vezes a animação deve repetir"
                    )
    
    @staticmethod
    def render_text_preview(config: Dict[str, Any]):
        """Renderiza a pré-visualização do texto e animações (atualizado)"""
        if not config.get("texto"):
            return
            
        st.divider()
        st.subheader("👁️ PRÉ-VISUALIZAÇÃO DE TEXTO")
        
        try:
            # Processa a imagem com texto
            with st.spinner("Aplicando texto..."):
                start_time = time.time()
                
                # Aplica texto à imagem processada
                if st.session_state.processed_image:
                    base_image = st.session_state.processed_image.copy()
                else:
                    base_image = st.session_state.base_image.copy()
                
                # Verifica o tamanho da imagem (nova funcionalidade)
                if not ImageProcessor.check_image_size(base_image):
                    base_image = ImageProcessor.resize_large_image(base_image)
                    st.warning("Imagem redimensionada para prevenir problemas de processamento")
                
                text_image = TextProcessor.apply_text_effect(base_image, config)
                st.session_state.text_image = text_image
                processing_time = time.time() - start_time
            
            # Mostra antes/depois
            col1, col2 = st.columns(2)
            
            with col1:
                st.image(
                    base_image,
                    caption="Sem Texto",
                    use_container_width=True
                )
            
            with col2:
                st.image(
                    st.session_state.text_image,
                    caption=f"Com Texto ({processing_time:.2f}s)",
                    use_container_width=True
                )

            # Mostra pré-visualização de animação de texto se houver animações selecionadas
            if config.get("animacao_texto") and any(k not in ["duracao", "repetir"] for k in config["animacao_texto"].keys()):
                st.subheader("🎬 PRÉ-VISUALIZAÇÃO DA ANIMAÇÃO DE TEXTO")

                # Gera frames da animação de texto
                duration = config["animacao_texto"].get("duracao", 2.0)
                frames = TextProcessor.generate_text_animation_frames(
                    base_image,
                    config,
                    config["animacao_texto"],
                    duration
                )

                # Mostra a animação
                if frames:
                    with st.spinner("Gerando pré-visualização..."):
                        # Redimensiona os frames se necessário para o GIF (nova funcionalidade)
                        resized_frames = []
                        for frame in frames:
                            if frame.width > 800 or frame.height > 600:
                                resized_frames.append(frame.resize((800, 600), Image.LANCZOS))
                            else:
                                resized_frames.append(frame)
                        
                        gif_bytes = io.BytesIO()
                        resized_frames[0].save(
                            gif_bytes,
                            format='GIF',
                            append_images=resized_frames[1:],
                            save_all=True,
                            duration=int(duration * 1000 / len(resized_frames)),
                            loop=0
                        )
                        gif_bytes.seek(0)

                    # Container com borda para a pré-visualização
                    with st.container(border=True):
                        st.markdown("**Pré-visualização da Animação de Texto**")

                        # Exibe o GIF animado com largura fixa via HTML
                        gif_b64 = base64.b64encode(gif_bytes.getvalue()).decode("utf-8")
                        st.markdown(
                            f'<img src="data:image/gif;base64,{gif_b64}" width="500"/>',
                            unsafe_allow_html=True
                        )

                        st.markdown(f"**Duração:** {duration:.1f}s | **Frames:** {len(frames)}")
                
                # Mostra instruções de animação de texto
                st.subheader("📝 Instruções para Animações de Texto")
                
                anim_instructions = AnimationExporter.generate_animation_instructions(config["animacao_texto"])
                
                tab_clip, tab_cap, tab_man = st.tabs(["Clipchamp", "CapCut", "Editores Profissionais"])
                
                with tab_clip:
                    for instruction in anim_instructions["clipchamp"]:
                        st.markdown(instruction)
                
                with tab_cap:
                    for instruction in anim_instructions["capcut"]:
                        st.markdown(instruction)
                
                with tab_man:
                    for instruction in anim_instructions["manual"]:
                        st.code(instruction, language="text")
                        
        except Exception as e:  # Nova funcionalidade: tratamento de erros
            st.error(f"Erro ao processar texto: {str(e)}")
    
    @staticmethod
    def render_sidebar():
        """Renderiza a barra lateral sem os avisos de vídeo indesejados"""
        with st.sidebar:
            st.title("🛠️ Configurações")

            # Seletor de Tema
            st.radio(
                "Tema",
                ["Claro", "Escuro"],
                key="theme_selector",
                on_change=update_theme
            )

            # Status de vídeo discreto
            with st.expander("🔍 Status do Sistema", expanded=False):
                status_col, help_col = st.columns([3, 1])
                
                with status_col:
                    st.caption(VideoProcessor.get_video_status())
                
                with help_col:
                    if not VIDEO_SUPPORT:
                        if st.button("ℹ️", help="Como ativar suporte a vídeo"):
                            VideoProcessor.show_video_help()

            # Upload de Mídia
            file_types = ["jpg", "jpeg", "png", "webp"]
            if VIDEO_SUPPORT:
                file_types.extend(["mp4", "mov", "avi", "mkv", "webm"])
                
            uploaded_file = st.file_uploader(
                "📤 Envie sua mídia",
                type=file_types,
                help=f"Formatos suportados: {', '.join(file_types).upper()}"
            )

            # Configurações de Vídeo
            video_expander = st.expander("🎥 Configurações de Vídeo", expanded=False)
            with video_expander:
                if VIDEO_SUPPORT:
                    ffmpeg_path = st.text_input(
                        "Caminho do FFmpeg (opcional)",
                        value=os.environ.get("IMAGEIO_FFMPEG_EXE", ""),
                        help="Especifique manualmente se necessário"
                    )
                    
                    if ffmpeg_path:
                        if os.path.exists(ffmpeg_path):
                            os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
                            if st.button("Aplicar configuração"):
                                st.rerun()
                        else:
                            st.warning("Caminho inválido")
                    
                    st.info(f"FFmpeg: {os.environ.get('IMAGEIO_FFMPEG_EXE', 'auto-detectado')}")
                else:
                    st.info("Recursos de vídeo não disponíveis")
                    if st.button("Mostrar instruções de instalação"):
                        VideoProcessor.show_video_help()

            # Processamento da Mídia
            if uploaded_file and uploaded_file.file_id != st.session_state.get('uploaded_file_id'):
                st.session_state.base_image = None
                st.session_state.video_clip = None
                st.session_state.processed_video_clip = None

                with st.spinner("Analisando sua mídia..."):
                    try:
                        if uploaded_file.type.startswith('video/'):
                            if VIDEO_SUPPORT:
                                st.session_state.video_clip = VideoProcessor.load_video(uploaded_file)
                                if st.session_state.video_clip:
                                    st.success("Vídeo carregado!")
                        else:
                            st.session_state.base_image = ImageProcessor.load_image(uploaded_file)
                            st.success("Imagem carregada!")

                        st.session_state.uploaded_file_id = uploaded_file.file_id
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro: {str(e)}")

            # Pré-visualização
            if st.session_state.get('video_clip'):
                st.video(st.session_state.video_clip.filename)
            elif st.session_state.get('base_image'):
                st.image(st.session_state.base_image, caption="Pré-visualização", use_container_width=True)

            # Configurações Avançadas
            with st.expander("⚙️ Configurações", expanded=False):
                st.checkbox(
                    "Modo Performance",
                    value=True,
                    key="performance_mode",
                    help="Reduz qualidade para maior velocidade"
                )
                
                # CORREÇÃO: Usar o valor numérico da qualidade
                quality_preset = st.select_slider(
                    "Qualidade de Exportação",
                    options=["Baixa", "Média", "Alta", "Máxima"],
                    value="Alta",
                    key="export_quality_preset"
                )
                
                # Armazena os valores numéricos correspondentes
                st.session_state.export_quality = QualitySettings.get_preset(quality_preset)["quality"]
                
                if st.button("🔄 Redefinir Tudo"):
                    for key in list(st.session_state.keys()):
                        if key not in DEFAULT_STATE:
                            del st.session_state[key]
                    st.rerun()

            # Dicas
            st.markdown("---")
            st.markdown("""
                **💡 Dicas:**
                - Combine filtros para efeitos únicos
                - Vídeos podem demorar para processar
            """)
            
    @staticmethod
    def _render_animation_preview(processed_image, config):
        """Renderiza a pré-visualização de animação para imagens."""
        st.subheader("🎬 PRÉ-VISUALIZAÇÃO DA ANIMAÇÃO")
        
        # Gera frames da animação
        duration = config["animacao"].get("duracao", 2.0)
        frames = AnimationPreviewer.generate_animation_frames(
            processed_image,
            config["animacao"],
            duration
        )

        # Mostra a animação
        if frames:
            with st.spinner("Gerando pré-visualização..."):
                # Redimensiona os frames se necessário para o GIF
                resized_frames = []
                for frame in frames:
                    if frame.width > 800 or frame.height > 600:
                        resized_frames.append(frame.resize((800, 600), Image.LANCZOS))
                    else:
                        resized_frames.append(frame)
                
                gif_bytes = io.BytesIO()
                resized_frames[0].save(
                    gif_bytes,
                    format='GIF',
                    append_images=resized_frames[1:],
                    save_all=True,
                    duration=int(duration * 1000 / len(resized_frames)),
                    loop=0
                )
                gif_bytes.seek(0)

            # Container com borda para a pré-visualização
            with st.container(border=True):
                st.markdown("**Pré-visualização da Animação**")

                # Exibe o GIF animado com largura fixa via HTML
                gif_b64 = base64.b64encode(gif_bytes.getvalue()).decode("utf-8")
                st.markdown(
                    f'<img src="data:image/gif;base64,{gif_b64}" width="500"/>',
                    unsafe_allow_html=True
                )

                st.markdown(f"**Duração:** {duration:.1f}s | **Frames:** {len(frames)}")
        
        # Mostra instruções de animação
        st.subheader("📝 Instruções para Animações")
        
        anim_instructions = AnimationExporter.generate_animation_instructions(config["animacao"])
        
        tab_clip, tab_cap, tab_man = st.tabs(["Clipchamp", "CapCut", "Editores Profissionais"])
        
        with tab_clip:
            for instruction in anim_instructions["clipchamp"]:
                st.markdown(instruction)
        
        with tab_cap:
            for instruction in anim_instructions["capcut"]:
                st.markdown(instruction)
        
        with tab_man:
            for instruction in anim_instructions["manual"]:
                st.code(instruction, language="text")
    
    @staticmethod
    def render_frame_tab(config: Dict[str, Any]):
        """Renderiza a aba de molduras"""
        with st.expander("🖼️ CONFIGURAÇÕES DE MOLDURA", expanded=True):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Seleção do tipo de moldura
                frame_options = [
                    f"{EffectDatabase.FRAME_DATABASE[name]['icon']} {name}" 
                    for name in EffectDatabase.FRAME_DATABASE
                ]
                
                selected_frame = st.selectbox(
                    "Tipo de Moldura",
                    options=list(EffectDatabase.FRAME_DATABASE.keys()),
                    format_func=lambda x: f"{EffectDatabase.FRAME_DATABASE[x]['icon']} {x}",
                    index=0,
                    key="frame_type"
                )
                
                config["moldura"]["tipo"] = selected_frame
                
                # Configurações específicas da moldura
                if selected_frame != "Nenhuma":
                    frame_info = EffectDatabase.FRAME_DATABASE[selected_frame]
                    
                    config["moldura"]["cor"] = st.color_picker(
                        "Cor da Moldura",
                        frame_info["params"]["cor_padrao"],
                        key="frame_color"
                    )
                    
                    config["moldura"]["espessura"] = st.slider(
                        "Espessura",
                        frame_info["params"]["min_espessura"],
                        frame_info["params"]["max_espessura"],
                        (frame_info["params"]["min_espessura"] + frame_info["params"]["max_espessura"]) // 2,
                        key="frame_thickness"
                    )
                    
                    if "estilo" in frame_info["params"]:
                        config["moldura"]["estilo"] = st.radio(
                            "Estilo",
                            frame_info["params"]["estilo"],
                            horizontal=True,
                            key="frame_style"
                        )
            
            with col2:
                if selected_frame != "Nenhuma":
                    frame_info = EffectDatabase.FRAME_DATABASE[selected_frame]
                    
                    # Exemplo visual
                    example_img = Image.new('RGB', (400, 300), (50, 50, 50))
                    example_img = ImageProcessor.apply_frame(example_img, config["moldura"])
                    
                    st.image(
                        example_img,
                        caption=f"Exemplo: {selected_frame}",
                        use_container_width=True
                    )
                    
                    # Descrição e dicas
                    st.markdown(f"**{frame_info['icon']} {selected_frame}**")
                    st.markdown(frame_info["desc"])
                    
                    if "dica" in frame_info["params"]:
                        st.info(frame_info["params"]["dica"])
    
    @staticmethod
    def render_filters_tab(config: Dict[str, Any]):
        """Renderiza a aba de filtros de cor"""
        with st.expander("🌈 CONFIGURAÇÕES DE FILTRO", expanded=True):
            # Seleção de filtros com ícones
            filter_options = [
                f"{EffectDatabase.FILTER_DATABASE[name]['icon']} {name}" 
                for name in EffectDatabase.FILTER_DATABASE
            ]
            
            selected_filters = st.multiselect(
                "Selecione os filtros:",
                options=list(EffectDatabase.FILTER_DATABASE.keys()),
                default=["Vintage"],
                format_func=lambda x: f"{EffectDatabase.FILTER_DATABASE[x]['icon']} {x}",
                help="Segure Ctrl/Cmd para selecionar múltiplos filtros"
            )
            
            # Configurações para cada filtro selecionado
            for filter_name in selected_filters:
                filter_info = EffectDatabase.FILTER_DATABASE[filter_name]
                
                with st.expander(f"{filter_info['icon']} {filter_name}"):
                    config["filtros"][filter_name] = {}
                    
                    for param_name, param_config in filter_info["params"].items():
                        # Controles especiais para parâmetros específicos
                        if param_name == "tons" and filter_name == "Preto e Branco":
                            config["filtros"][filter_name][param_name] = st.select_slider(
                                "Balanço de Tons",
                                options=["Mais escuro", "Padrão", "Mais claro"],
                                value="Padrão",
                                key=f"{filter_name}_{param_name}"
                            )
                        else:
                            # Slider padrão para outros parâmetros
                            config["filtros"][filter_name][param_name] = st.slider(
                                param_name.capitalize(),
                                param_config["min"],
                                param_config["max"],
                                param_config["default"],
                                param_config.get("step", 1),
                                key=f"{filter_name}_{param_name}"
                            )
            
            # Recomendações de combinação
            if len(selected_filters) > 1:
                st.markdown("---")
                with st.expander("💡 Combinações Recomendadas e Exemplos"):
                    for filter_name in selected_filters:
                        if "combinations" in EffectDatabase.FILTER_DATABASE[filter_name]:
                            st.markdown(f"### {filter_name}")
                            st.markdown(f"**Combina bem com:** {', '.join(EffectDatabase.FILTER_DATABASE[filter_name]['combinations'])}")
                            
                            # Mostrar exemplo visual da combinação
                            combo_example = EffectDatabase.FILTER_DATABASE[filter_name].get("combo_example")
                            if combo_example:
                                st.image(combo_example, caption=f"Exemplo de combinação com {filter_name}", width=400)
    
    @staticmethod
    def render_animation_tab(config: Dict[str, Any]):
        """Renderiza a aba de animações"""
        with st.expander("🎬 CONFIGURAÇÕES DE ANIMAÇÃO", expanded=True):
            # Lista de animações formatadas com ícones e complexidade
            animation_options = [
                f"{EffectDatabase.ANIMATION_DATABASE[name]['icon']} {name} "
                f"({'⭐' * EffectDatabase.ANIMATION_DATABASE[name]['complexity']})" 
                for name in EffectDatabase.ANIMATION_DATABASE
            ]
            
            selected_animations = st.multiselect(
                "Selecione as animações:",
                options=list(EffectDatabase.ANIMATION_DATABASE.keys()),
                default=[],  # Alterado para lista vazia para não iniciar com animações
                format_func=lambda x: (
                    f"{EffectDatabase.ANIMATION_DATABASE[x]['icon']} {x} "
                    f"({'⭐' * EffectDatabase.ANIMATION_DATABASE[x]['complexity']})"
                ),
                help="Selecione uma ou mais animações para aplicar"
            )
            
            # Configurações para cada animação selecionada
            for anim_name in selected_animations:
                anim_info = EffectDatabase.ANIMATION_DATABASE[anim_name]
                
                with st.expander(f"{anim_info['icon']} {anim_name}"):
                    config["animacao"][anim_name] = {}
                    
                    for param_name, param_config in anim_info["params"].items():
                        # Controles diferentes baseados no tipo de parâmetro
                        if isinstance(param_config, list):
                            config["animacao"][anim_name][param_name] = st.radio(
                                param_name.capitalize(),
                                param_config,
                                horizontal=True,
                                key=f"{anim_name}_{param_name}"
                            )
                        else:
                            config["animacao"][anim_name][param_name] = st.slider(
                                param_name.capitalize(),
                                param_config["min"],
                                param_config["max"],
                                param_config["default"],
                                param_config.get("step", 1),
                                key=f"{anim_name}_{param_name}"
                            )
            
            # Configurações gerais de animação
            if selected_animations:
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    config["animacao"]["duracao"] = st.slider(
                        "Duração Total (segundos)",
                        0.5, 5.0, 2.0, 0.1,
                        help="Duração total da animação combinada"
                    )
                
                with col2:
                    config["animacao"]["repetir"] = st.selectbox(
                        "Repetição",
                        ["Nenhuma", "2 vezes", "Continuamente"],
                        help="Quantas vezes a animação deve repetir"
                    )
                    
    @staticmethod
    def render_layers_tab(config: Dict[str, Any]):
        """Renderiza a aba de gerenciamento de camadas"""
        with st.expander("🖼️ GERENCIAMENTO DE CAMADAS", expanded=True):
            st.markdown("Configure camadas transparentes para sobrepor na imagem")
            
            if 'layers' not in config:
                config['layers'] = []
                
            # Controles para adicionar novas camadas
            with st.form("add_layer_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    layer_opacity = st.slider(
                        "Opacidade da Camada",
                        0.0, 1.0, 0.5, 0.1,
                        key="layer_opacity"
                    )
                    
                    layer_position_x = st.number_input(
                        "Posição X",
                        min_value=0,
                        max_value=1000,
                        value=0,
                        key="layer_pos_x"
                    )
                    
                with col2:
                    layer_file = st.file_uploader(
                        "Imagem da Camada",
                        type=["png", "webp"],
                        key="layer_upload"
                    )
                    
                    layer_position_y = st.number_input(
                        "Posição Y",
                        min_value=0,
                        max_value=1000,
                        value=0,
                        key="layer_pos_y"
                    )
                
                if st.form_submit_button("➕ Adicionar Camada"):
                    if layer_file:
                        layer_img = Image.open(layer_file)
                        config['layers'].append({
                            "image": layer_img,
                            "position": (layer_position_x, layer_position_y),
                            "opacity": layer_opacity
                        })
                        st.success("Camada adicionada!")
                    else:
                        st.warning("Selecione uma imagem para a camada")
            
            # Lista de camadas existentes
            st.markdown("### Camadas Ativas")
            for i, layer in enumerate(config['layers']):
                with st.expander(f"Camada {i+1}"):
                    col1, col2 = st.columns([2, 3])
                    
                    with col1:
                        st.image(
                            layer['image'],
                            caption=f"Opacidade: {layer['opacity']}",
                            width=150
                        )
                        
                        if st.button(f"❌ Remover Camada {i+1}"):
                            config['layers'].pop(i)
                            st.rerun()
                    
                    with col2:
                        new_opacity = st.slider(
                            "Opacidade",
                            0.0, 1.0, layer['opacity'], 0.1,
                            key=f"layer_{i}_opacity"
                        )
                        
                        new_x = st.number_input(
                            "Posição X",
                            min_value=0,
                            max_value=1000,
                            value=layer['position'][0],
                            key=f"layer_{i}_pos_x"
                        )
                        
                        new_y = st.number_input(
                            "Posição Y",
                            min_value=0,
                            max_value=1000,
                            value=layer['position'][1],
                            key=f"layer_{i}_pos_y"
                        )
                        
                        layer['opacity'] = new_opacity
                        layer['position'] = (new_x, new_y)
    
# ======================================================================================
# SEÇÕES DE PREVIEW E EXPORTAÇÃO - VERSÃO FINAL E CORRIGIDA
# ======================================================================================

    @staticmethod
    def render_preview(config: Dict[str, Any]):
        """
        Função principal de pré-visualização.
        Verifica se a mídia carregada é um vídeo ou imagem e chama a função correta.
        """
        # Roteador: decide qual preview renderizar
        if st.session_state.get('video_clip'):
            # Passa o clipe de preview para a função de renderização de vídeo
            FiltrosProUI._render_video_preview(st.session_state.video_clip, config)
        elif st.session_state.get('base_image'):
            # Passa a imagem base para a função de renderização de imagem
            FiltrosProUI._render_image_preview(st.session_state.base_image, config)
            
            # A lógica de animação GIF faz sentido apenas para imagens, então fica aqui
            if config.get("animacao") and any(k not in ["duracao", "repetir"] for k in config["animacao"].keys()):
                if hasattr(FiltrosProUI, '_render_animation_preview'):
                    FiltrosProUI._render_animation_preview(st.session_state.processed_image, config)

    @staticmethod
    def _render_image_preview(base_image, config):
        """Renderiza a pré-visualização APENAS para imagens."""
        st.divider()
        st.subheader("👁️ PRÉ-VISUALIZAÇÃO AO VIVO (IMAGEM)")
        
        with st.spinner("Aplicando efeitos na imagem..."):
            # Lógica de processamento de imagem que você já tinha...
            # (seu código de apply_filters, apply_frame, etc.)
            processed_image = base_image.copy() # Começa com a original
            if config.get("filtros"):
                processed_image = ImageProcessor.apply_filters(processed_image, config["filtros"])
            if config.get("moldura", {}).get("tipo", "Nenhuma") != "Nenhuma":
                processed_image = ImageProcessor.apply_frame(processed_image, config["moldura"])
            st.session_state.processed_image = processed_image

        # Mostra antes/depois
        col1, col2 = st.columns(2)
        with col1:
            st.image(base_image, caption="Original", use_container_width=True)
        with col2:
            st.image(st.session_state.processed_image, caption="Com Efeitos", use_container_width=True)


    @staticmethod
    def _render_video_preview(video_clip, config):
        """Renderiza a pré-visualização APENAS para vídeos."""
        st.divider()
        st.subheader("🎥 PRÉ-VISUALIZAÇÃO AO VIVO (VÍDEO)")

        # Aplica os filtros e molduras ao clipe de vídeo em memória
        # Isso é rápido porque moviepy só processa quando precisa (lazy evaluation)
        processed_clip = video_clip
        if config.get("filtros"):
            processed_clip = processed_clip.fl_image(
                lambda f: np.array(ImageProcessor.apply_filters(Image.fromarray(f), config["filtros"]))
            )
        if config.get("moldura", {}).get("tipo", "Nenhuma") != "Nenhuma":
            processed_clip = processed_clip.fl_image(
                lambda f: np.array(ImageProcessor.apply_frame(Image.fromarray(f), config["moldura"]))
            )
        
        # Salva o clipe processado no estado da sessão para ser usado na exportação
        st.session_state.processed_video_clip = processed_clip

        # Mostra o preview
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Original**")
            st.video(video_clip.filename) # Mostra o vídeo original (de preview)
        with col2:
            st.markdown("**Com Efeitos**")
            # Para evitar re-renderizar o vídeo a cada ajuste, mostramos apenas o primeiro frame processado.
            # Adicionamos um botão para renderizar um clipe de preview sob demanda.
            preview_frame = processed_clip.get_frame(0)
            st.image(preview_frame, caption="Preview do primeiro frame com efeitos", use_container_width=True)
            
            if st.button("▶️ Gerar Preview em Vídeo (5s)"):
                with st.spinner("Renderizando preview..."):
                    preview_clip_5s = processed_clip.subclip(0, min(5, processed_clip.duration))
                    video_bytes = VideoProcessor.export_video(preview_clip_5s)
                    st.session_state.preview_video_bytes = video_bytes
            
            if 'preview_video_bytes' in st.session_state and st.session_state.preview_video_bytes:
                st.video(st.session_state.preview_video_bytes)


    @staticmethod
    def render_export_section(config: Dict[str, Any]):
        """Renderiza a seção de exportação completa - ATUALIZADA"""
        st.divider()
        st.subheader("📤 EXPORTAR CONFIGURAÇÕES E ARQUIVOS")
        
        # Seção de limpeza - NOVO
        with st.expander("🧹 OPÇÕES DE LIMPEZA", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                clean_artifacts = st.checkbox(
                    "Remover artefatos visuais",
                    value=True,
                    help="Remove pixels semi-transparentes e sujeira"
                )
                
            with col2:
                clean_level = st.slider(
                    "Nível de limpeza",
                    1, 10, 5,
                    help="Ajusta a intensidade da limpeza (1=suave, 10=agressivo)"
                )
        
        # Adiciona as configurações de limpeza ao config
        config["clean_settings"] = {
            "active": clean_artifacts,
            "level": clean_level
        }
        
        tab_modular, tab_completo = st.tabs(["🔧 Exportação Modular", "📦 Exportação Completa"])
        
        with tab_modular:
            st.markdown("### 🧩 Selecione os Módulos para Exportar")
            
            col1, col2 = st.columns([3, 2])
            
            with col1:
                module_options = {
                    "moldura": "🖼️ Molduras",
                    "filtros": "🌈 Filtros de Cor",
                    "animacao": "🎬 Animações",
                    "texto": "✍️ Texto e Animações de Texto"
                }
                
                modules_to_export = st.multiselect(
                    "Módulos disponíveis:",
                    options=list(module_options.keys()),
                    default=["moldura", "filtros"],
                    format_func=lambda x: module_options[x],
                    help="Selecione quais módulos deseja exportar"
                )
                
                if "filtros" in modules_to_export:
                    filter_export_type = st.radio(
                        "Formato para filtros de cor:",
                        options=["PNG (Transparente)", "LUT .cube (Para editores)"],
                        index=0,
                        horizontal=True,
                        key="filter_export_type"
                    )
                
                if "texto" in modules_to_export and config.get("animacao_texto"):
                    text_export_type = st.radio(
                        "Formato para animação de texto:",
                        options=["GIF (Animação)", "MP4 (Vídeo)"],
                        index=0,
                        horizontal=True,
                        key="text_export_type"
                    )
                
                export_format = st.radio(
                    "Formato de exportação:",
                    options=["PNG", "GIF", "MP4"],
                    index=0,
                    horizontal=True,
                    key="modular_export_format"
                )
            
            with col2:
                st.markdown("### ⚙️ Gerar Arquivos")
                
                if st.button("🛠️ Gerar Arquivos Modulares", use_container_width=True):
                    export_files = []
                    
                    for module in modules_to_export:
                        format_type = "LUT" if module == "filtros" and filter_export_type == "LUT .cube (Para editores)" else export_format
                        
                        if module == "texto" and config.get("animacao_texto"):
                            format_type = "GIF" if text_export_type == "GIF (Animação)" else "MP4"
                        
                        data, filename, mime = ModularExporter.export_module(
                            module, 
                            config,  # Já contém as configurações de limpeza
                            format_type
                        )
                        
                        if data:
                            export_files.append((data, filename, mime))
                    
                    if export_files:
                        st.session_state.modular_exports = export_files
                        st.success(f"Gerados {len(export_files)} arquivo(s) para exportação!")
                    else:
                        st.warning("Nenhum módulo válido selecionado para exportação")
                
                if "modular_exports" in st.session_state and st.session_state.modular_exports:
                    st.markdown("### 📥 Downloads Modulares")
                    for i, (data, filename, mime) in enumerate(st.session_state.modular_exports):
                        st.download_button(
                            label=f"⬇️ Baixar {filename}",
                            data=data,
                            file_name=filename,
                            mime=mime,
                            key=f"modular_download_{i}",
                            use_container_width=True
                        )
        
        with tab_completo:
            st.markdown("### 📦 Exportar Todos os Efeitos Ativos")
            
            col1, col2 = st.columns([3, 2])
            
            with col1:
                active_modules = []
                if config.get("moldura", {}).get("tipo", "Nenhuma") != "Nenhuma":
                    active_modules.append("🖼️ Moldura")
                if config.get("filtros"):
                    active_modules.append("🌈 Filtros")
                if config.get("animacao"):
                    active_modules.append("🎬 Animações")
                if config.get("texto"):
                    active_modules.append("✍️ Texto")
                
                if active_modules:
                    st.markdown("**Efeitos ativos detectados:**")
                    for module in active_modules:
                        st.markdown(f"- {module}")
                    
                    export_format = st.selectbox(
                        "Formato de exportação:",
                        options=["PNG (Transparente)", "GIF (Animação)", "MP4 (Vídeo HQ)", "JPG (Com fundo branco)"],
                        index=0
                    )
                    
                    if export_format in ["GIF (Animação)", "MP4 (Vídeo HQ)"]:
                        quality_level = st.select_slider(
                            "Qualidade de Exportação:",
                            options=["Baixa", "Média", "Alta", "Máxima"],
                            value="Alta"
                        )
                        # Armazena o valor numérico correspondente
                        st.session_state.export_quality = QualitySettings.get_preset(quality_level)["quality"]
                    
                    output_size = st.radio(
                        "Tamanho de Saída:",
                        options=["Original", "HD (1280x720)", "Full HD (1920x1080)"],
                        index=0,
                        horizontal=True
                    )
            
            with col2:
                st.markdown("### ⚙️ Gerar Arquivo")
                
                if st.button("🛠️ Gerar Arquivo Completo", use_container_width=True, disabled=not active_modules):
                    format_map = {
                        "PNG (Transparente)": "PNG",
                        "GIF (Animação)": "GIF",
                        "MP4 (Vídeo HQ)": "MP4",
                        "JPG (Com fundo branco)": "JPG"
                    }
                    
                    quality_settings = {
                        "quality_level": quality_level if export_format in ["GIF (Animação)", "MP4 (Vídeo HQ)"] else "Alta",
                        "output_size": output_size,
                        "clean_settings": config["clean_settings"]  # Adiciona as configurações de limpeza
                    }
                    
                    export_data, filename, mime = ModularExporter.export_all(
                        config, 
                        format_map[export_format],
                        quality_settings
                    )
                    
                    if export_data:
                        st.session_state.full_export_data = export_data
                        st.session_state.full_export_filename = filename
                        st.session_state.full_export_mime = mime
                        st.success("Arquivo completo gerado com sucesso!")
                    else:
                        st.error("Erro ao gerar arquivo completo")
                
                if st.session_state.get('full_export_data'):
                    st.download_button(
                        label=f"💾 Baixar {st.session_state.full_export_filename}",
                        data=st.session_state.full_export_data,
                        file_name=st.session_state.full_export_filename,
                        mime=st.session_state.full_export_mime,
                        use_container_width=True
                    )
    
    @staticmethod
    def render_footer():
        """Renderiza o rodapé da aplicação"""
        st.divider()
        st.markdown("""
            <div style="text-align: center; color: #666;">
                <p><strong>🎬 Criador de Filtros Pro - Super Edition v2.1</strong></p>
                <p>Ferramenta profissional para criadores de conteúdo • 
                <a href="#" target="_blank">Documentação</a> • 
                <a href="#" target="_blank">Reportar Bug</a></p>
            </div>
        """, unsafe_allow_html=True)
    
    def main():
        # Verificar suporte a vídeo (usando a constante VIDEO_SUPPORT)
        if not VIDEO_SUPPORT:
            VideoProcessor.show_video_requirements_warning()
            
        """Função principal que renderiza toda a UI (atualizada)"""
        # Configuração inicial
        config = {
            "moldura": {"tipo": "Nenhuma"},
            "filtros": {},
            "animacao": {},
            "texto": "",
            "fonte": {"tipo": "Padrão", "tamanho": 32, "cor": "#FFFFFF"},
            "posicao": {"horizontal": "Centro", "vertical": "Meio"},
            "contorno": {"ativo": False, "cor": "#000000", "espessura": 1},
            "animacao_texto": {}
        }
        
        # Inicializa configurações de qualidade se não existirem
        if 'export_quality' not in st.session_state:
            st.session_state.export_quality = "Alta"
        if 'output_size' not in st.session_state:
            st.session_state.output_size = "Original"
        
        # Renderiza a sidebar
        FiltrosProUI.render_sidebar()
        
        # Abas principais (atualizadas com a nova aba de texto)
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🖼️ MOLDURAS", 
            "🌈 FILTROS", 
            "🎬 ANIMAÇÕES", 
            "✍️ TEXTO",
            "➕ CAMADAS"
        ])
        
        with tab1:
            FiltrosProUI.render_frame_tab(config)
        
        with tab2:
            FiltrosProUI.render_filters_tab(config)
        
        with tab3:
            FiltrosProUI.render_animation_tab(config)
        
        with tab4:
            FiltrosProUI.render_text_tab(config)
            
        with tab5:
            FiltrosProUI.render_layers_tab(config)
        
        # Pré-visualização (se houver imagem processada)
        if st.session_state.base_image:
            if any(config["filtros"]) or config["moldura"]["tipo"] != "Nenhuma":
                FiltrosProUI.render_preview(config)
            
            # Pré-visualização de texto (se houver texto definido)
            if config.get("texto"):
                FiltrosProUI.render_text_preview(config)
        
        # Exportação (agora com sistema modular)
        FiltrosProUI.render_export_section(config)
        
        # Rodapé
        FiltrosProUI.render_footer()

# ======================================================================================
# ATUALIZAÇÃO DA EXECUÇÃO PRINCIPAL
# ======================================================================================

if __name__ == "__main__":
    # Verifica e inicializa o session state
    for key, value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Adiciona estados específicos para texto
    if 'text_image' not in st.session_state:
        st.session_state.text_image = None
    
    # Executa a aplicação
    FiltrosProUI.main()