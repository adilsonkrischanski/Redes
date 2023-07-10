import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Função para calcular média e desvio padrão dos valores de cwnd
def calcular_estatisticas(cwnd_dict):
    estatisticas = {}
    for arquivo, cwnd_list in cwnd_dict.items():
        media = np.mean(cwnd_list)
        desvio_padrao = np.std(cwnd_list)
        estatisticas[arquivo] = {'Média': media, 'Desvio Padrão': desvio_padrao}
    return estatisticas

# Diretórios com os arquivos
for i in range(1, 6):
    diretorio_cubic = f"./Resultados/cubic/exp{i}/"
    diretorio_reno = f"./Resultados/reno/exp{i}/"

    # Função para processar os arquivos e retornar os valores de cwnd
    def processar_arquivos(diretorio):
        cwnd_dict = {}

        # Percorre todos os arquivos no diretório
        for nome_arquivo in os.listdir(diretorio):
            if nome_arquivo.endswith("5000.txt"):
                caminho_arquivo = os.path.join(diretorio, nome_arquivo)

                # Abrir o arquivo e ler as linhas
                with open(caminho_arquivo, 'r') as file:
                    lines = file.readlines()

                # Lista para armazenar os valores de cwnd
                cwnd_list = []

                # Procurar pelas linhas contendo informações de cwnd e extrair os valores
                for line in lines:
                    match = re.search(r'cwnd:(\d+)', line)
                    if match:
                        cwnd = int(match.group(1))
                        cwnd_list.append(cwnd)

                # Armazena a lista de valores de cwnd no dicionário, usando o nome do arquivo como chave
                cwnd_dict[nome_arquivo] = cwnd_list

        return cwnd_dict

    # Processa os arquivos do diretório "cubic"
    cwnd_dict_cubic = processar_arquivos(diretorio_cubic)
    estatisticas_cubic = calcular_estatisticas(cwnd_dict_cubic)

    # Processa os arquivos do diretório "reno"
    cwnd_dict_reno = processar_arquivos(diretorio_reno)
    estatisticas_reno = calcular_estatisticas(cwnd_dict_reno)

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

    # Plota os gráficos de variação do cwnd por tempo para cada diretório
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
    for nome_arquivo, cwnd_list in cwnd_dict_cubic.items():
        tempo = range(len(cwnd_list))
        label = f'{nome_arquivo.split(" ")[1]} processo(s)'
        plt.plot(tempo, cwnd_list, label=label)
    plt.xlabel("Tempo")
    plt.ylabel("Valor de cwnd")
    plt.title("Variação do cwnd por Tempo - Cubic")
    plt.legend()

    plt.subplot(1, 2, 2)
    for nome_arquivo, cwnd_list in cwnd_dict_reno.items():
        tempo = range(len(cwnd_list))
        label = f'{nome_arquivo.split(" ")[1]} processo(s)'
        plt.plot(tempo, cwnd_list, label=label)
    plt.xlabel("Tempo")
    plt.ylabel("Valor de cwnd")
    plt.title("Variação do cwnd por Tempo - Reno")
    plt.legend()

    plt.tight_layout()
    plt.show()
