from analysis import (
    carregar_dados,
    agregar_dados_por_regiao,
    gerar_grafico_casos_por_regiao,
    criar_mapa_por_regiao,
    criar_mapa_por_cidade
)

def main():
    dados = carregar_dados()
    dados_regioes = agregar_dados_por_regiao(dados)
    gerar_grafico_casos_por_regiao(dados_regioes)

    criar_mapa_por_regiao(dados_regioes)
    criar_mapa_por_cidade(dados)

if __name__ == "__main__":
    main()
