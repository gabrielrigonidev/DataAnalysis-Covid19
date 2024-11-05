import json
import folium
import matplotlib.pyplot as plt
import os

DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_DADOS = os.path.join(DIRETORIO_BASE, '../data')
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_BASE, '../images')

os.makedirs(DIRETORIO_IMAGENS, exist_ok=True)
ARQUIVO_DADOS = os.path.join(DIRETORIO_DADOS, 'cases-brazil-cities.json')

COORDENADAS_CIDADES_SUDESTE = {
    "Campinas": [-22.90556, -47.06083],
    "Praia Grande": [-24.0323, -46.5111],
    "Ribeirão Preto": [-21.1775, -47.81028],
    "Vitória": [-20.3155, -40.3128],
    "Guarulhos": [-23.46278, -46.53333]
}

COORDENADAS_REGIOES = {
    "Norte": [-3.4168, -65.8561],
    "Nordeste": [-7.1195, -36.8241],
    "Centro-Oeste": [-15.7801, -47.9292],
    "Sudeste": [-22.9068, -43.1729],
    "Sul": [-27.5954, -48.5480]
}

def carregar_dados(caminho_arquivo=ARQUIVO_DADOS):
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        dados = json.load(file)
    return dados

def agregar_dados_por_regiao(dados):
    dados_regioes = {
        "Norte": {"casos": 0, "obitos": 0},
        "Nordeste": {"casos": 0, "obitos": 0},
        "Centro-Oeste": {"casos": 0, "obitos": 0},
        "Sudeste": {"casos": 0, "obitos": 0},
        "Sul": {"casos": 0, "obitos": 0}
    }
    regioes_estados = {
        "Norte": ["AC", "AM", "AP", "PA", "RO", "RR", "TO"],
        "Nordeste": ["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"],
        "Centro-Oeste": ["GO", "MT", "MS", "DF"],
        "Sudeste": ["ES", "MG", "RJ", "SP"],
        "Sul": ["PR", "RS", "SC"]
    }
    
    for registro in dados:
        estado = registro["state"]
        for regiao, estados in regioes_estados.items():
            if estado in estados:
                dados_regioes[regiao]["casos"] += int(registro.get("totalCases", 0))
                dados_regioes[regiao]["obitos"] += int(registro.get("deaths", 0))
    
    return dados_regioes

def gerar_grafico_casos_por_regiao(dados_regioes):
    regioes = list(dados_regioes.keys())
    total_casos = [dados["casos"] for dados in dados_regioes.values()]

    plt.figure(figsize=(10, 6))
    plt.bar(regioes, total_casos, color='blue')
    plt.xlabel('Região')
    plt.ylabel('Total de Casos')
    plt.title('Total de Casos de COVID-19 por Região')
    plt.savefig(os.path.join(DIRETORIO_IMAGENS, 'total_casos_por_regiao.png'))
    plt.close()

def criar_mapa_por_regiao(dados_regioes):
    mapa_brasil = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)
    for regiao, coords in COORDENADAS_REGIOES.items():
        folium.Marker(
            location=coords,
            popup=f"{regiao}: {dados_regioes[regiao]['casos']} casos, {dados_regioes[regiao]['obitos']} óbitos",
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(mapa_brasil)
    mapa_brasil.save(os.path.join(DIRETORIO_IMAGENS, 'mapa_regioes.html'))

def criar_mapa_por_cidade(dados):
    mapa_sudeste = folium.Map(location=[-23.55052, -46.633308], zoom_start=6)
    for registro in dados:
        cidade_info = registro["city"].split("/")[0]
        if cidade_info in COORDENADAS_CIDADES_SUDESTE:
            casos = int(registro.get("totalCases", 0))
            obitos = int(registro.get("deaths", 0))
            coords = COORDENADAS_CIDADES_SUDESTE[cidade_info]
            folium.Marker(
                location=coords,
                popup=f"{cidade_info}: {casos} casos, {obitos} óbitos",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(mapa_sudeste)
    mapa_sudeste.save(os.path.join(DIRETORIO_IMAGENS, 'mapa_sudeste.html'))
