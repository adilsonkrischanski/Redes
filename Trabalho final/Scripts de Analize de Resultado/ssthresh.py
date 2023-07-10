import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Função para calcular média e desvio padrão dos valores de ssthresh
def calcular_estatisticas(ssthresh_dict):
    estatisticas = {}
    for arquivo, ssthresh_list in ssthresh_dict.items():
        media = np.mean(ssthresh_list)
        desvio_padrao = np.std(ssthresh_list)
        estatisticas[arquivo] = {'Média': media, 'Desvio Padrão': desvio_padrao}
    return estatisticas

# Diretórios com os arquivos
for i in range(1, 6):
    diretorio_cubic = f"./Resultados/cubic/exp{i}/"
    diretorio_reno = f"./Resultados/reno/exp{i}/"

    # Função para processar os arquivos e retornar os valores de ssthresh
    def processar_arquivos(diretorio):
        ssthresh_dict = {}

        # Percorre todos os arquivos no diretório
        for nome_arquivo in os.listdir(diretorio):
            if nome_arquivo.endswith("5000.txt"):
                caminho_arquivo = os.path.join(diretorio, nome_arquivo)

                # Abrir o arquivo e ler as linhas
                with open(caminho_arquivo, 'r') as file:
                    lines = file.readlines()

                # Lista para armazenar os valores de ssthresh
                ssthresh_list = []

                # Procurar pelas linhas contendo informações de ssthresh e extrair os valores
                for line in lines:
                    match = re.search(r'ssthresh:(\d+)', line)
                    if match:
                        ssthresh = int(match.group(1))
                        ssthresh_list.append(ssthresh)

                # Armazena a lista de valores de ssthresh no dicionário, usando o nome do arquivo como chave
                ssthresh_dict[nome_arquivo] = ssthresh_list

        return ssthresh_dict

    # Processa os arquivos do diretório "cubic"
    ssthresh_dict_cubic = processar_arquivos(diretorio_cubic)
    estatisticas_cubic = calcular_estatisticas(ssthresh_dict_cubic)

    # Processa os arquivos do diretório "reno"
    ssthresh_dict_reno = processar_arquivos(diretorio_reno)
    estatisticas_reno = calcular_estatisticas(ssthresh_dict_reno)

    # Cria um DataFrame com as estatísticas para o diretório "cubic"
    df_cubic = pd.DataFrame(estatisticas_cubic).T
    df_cubic.index.name = 'Arquivo'
    df_cubic.rename(columns={'Média': 'Cubic Média', 'Desvio Padrão': 'Cubic Desvio Padrão'}, inplace=True)

    # Cria um DataFrame com as estatísticas para o diretório "reno"
    df_reno = pd.DataFrame(estatisticas_reno).T
    df_reno.index.name = 'Arquivo'
    df_reno.rename(columns={'Média': 'Reno Média', 'Desvio Padrão': 'Reno Desvio Padrão'}, inplace=True)

    # Concatena os DataFrames em uma única tabela
    df_resultado = pd.concat([df_cubic, df_reno], axis=1)

    print(f"Resultados para Exp {i}:")
    print(df_resultado)
    print('\n')

    # Plota os gráficos de variação do ssthresh por tempo para cada diretório
    plt.figure(figsize=(12, 4))
    if i == 1:
        plt.suptitle("SEM LIMITE DE BANDA")
    if i == 2:
        plt.suptitle("20Mbps")
    if i == 3:
        plt.suptitle("10Mbps")
    if i == 4:
        plt.suptitle("5Mbps")
    if i == 5:
        plt.suptitle("1Mbps")

    plt.subplot(1, 2, 1)
    for nome_arquivo, ssthresh_list in ssthresh_dict_cubic.items():
        tempo = range(len(ssthresh_list))
        label = f'{nome_arquivo.split(" ")[1]} processo(s)'
        plt.plot(tempo, ssthresh_list, label=label)
    plt.xlabel("Tempo")
    plt.ylabel("Valor de ssthresh")
    plt.title("Variação do ssthresh por Tempo - Cubic")
    plt.legend()

    plt.subplot(1, 2, 2)
    for nome_arquivo, ssthresh_list in ssthresh_dict_reno.items():
        tempo = range(len(ssthresh_list))
        label = f'{nome_arquivo.split(" ")[1]} processo(s)'
        plt.plot(tempo, ssthresh_list, label=label)
    plt.xlabel("Tempo")
    plt.ylabel("Valor de ssthresh")
    plt.title("Variação do ssthresh por Tempo - Reno")
    plt.legend()

    plt.tight_layout()
    plt.show()
