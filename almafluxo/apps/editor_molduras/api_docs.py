"""
API do Criador de Filtros Pro

Endpoints:
- /api/v1/apply_filters (POST)
  Aplica filtros a uma imagem
  Parâmetros:
    - image: Arquivo de imagem
    - filters: Configuração de filtros em JSON
  Retorno:
    - Imagem processada em base64

- /api/v1/generate_animation (POST)
  Gera uma animação a partir de uma imagem
  Parâmetros:
    - image: Arquivo de imagem
    - animation_config: Configuração de animação em JSON
  Retorno:
    - GIF animado em base64

Exemplo de uso:
import requests

url = "http://localhost:8501/api/v1/apply_filters"
files = {'image': open('test.jpg', 'rb')}
data = {'filters': '{"Vintage": {"intensidade": 70}}'}
response = requests.post(url, files=files, data=data)
"""