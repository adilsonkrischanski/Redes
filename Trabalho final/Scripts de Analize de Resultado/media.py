import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Função para calcular média e desvio padrão dos valores de vazão total
def calcular_estatisticas(vazao_dict):
    estatisticas = {}
    for arquivo, vazao_list in vazao_dict.items():
        media = np.mean(vazao_list)
        desvio_padrao = np.std(vazao_list)
        estatisticas[arquivo] = {'Média': media, 'Desvio Padrão': desvio_padrao}
    return estatisticas

# Função para calcular a vazão total
def calcular_vazao_total(bytes_acked, bytes_recebidos, busy):
    bytes_entregues = bytes_acked + bytes_recebidos
    tempo_decorrido = busy / 1000
    vazao = bytes_entregues / tempo_decorrido
    return vazao

# Diretórios com os arquivos
for i in range(1, 6):
    diretorio_cubic = f"./Resultados/cubic/exp{i}/"
    diretorio_reno = f"./Resultados/reno/exp{i}/"

    # Função para processar os arquivos e retornar os valores de vazão total
    def processar_arquivos(diretorio):
        vazao_dict = {}

        # Percorre todos os arquivos no diretório
        for nome_arquivo in os.listdir(diretorio):
            if nome_arquivo.endswith("5000.txt"):
                caminho_arquivo = os.path.join(diretorio, nome_arquivo)

                # Abrir o arquivo e ler as linhas
                with open(caminho_arquivo, 'r') as file:
                    lines = file.readlines()

                # Listas para armazenar os valores de vazão total
                vazao_total_list = []

                # Procurar pelas linhas contendo informações de vazão total e extrair os valores
                for line in lines:
                    match = re.search(r'acked:(\d+)', line)
                    if match:
                        bytes_acked = int(match.group(1))

                    match = re.search(r'received:(\d+)', line)
                    if match:
                        bytes_recebidos = int(match.group(1))

                    match = re.search(r'busy:(\d+)', line)
                    if match:
                        busy = int(match.group(1))
                        vazao_total = calcular_vazao_total(bytes_acked, bytes_recebidos, busy)
                        vazao_total_list.append(vazao_total)

                # Armazena a lista de valores de vazão total no dicionário, usando o nome do arquivo como chave
                vazao_dict[nome_arquivo] = vazao_total_list

        return vazao_dict

    # Processa os arquivos do diretório "cubic"
    vazao_dict_cubic = processar_arquivos(diretorio_cubic)
    estatisticas_cubic = calcular_estatisticas(vazao_dict_cubic)

    # Processa os arquivos do diretório "reno"
    vazao_dict_reno = processar_arquivos(diretorio_reno)
    estatisticas_reno = calcular_estatisticas(vazao_dict_reno)

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

    # Plota os gráficos de vazão total por tempo para cada diretório
    plt.figure(figsize=(12, 6))
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
    for nome_arquivo, vazao_total_list in vazao_dict_cubic.items():
        tempo = range(len(vazao_total_list))
        label = f'{nome_arquivo.split(" ")[1]} processo(s)'
        plt.plot(tempo, vazao_total_list, label=label)
    plt.xlabel("Tempo")
    plt.ylabel("Vazão Total (Mbps)")
    plt.title("Variação da Vazão Total por Tempo - Cubic")
    plt.legend()

    plt.subplot(1, 2, 2)
    for nome_arquivo, vazao_total_list in vazao_dict_reno.items():
        tempo = range(len(vazao_total_list))
        label = f'{nome_arquivo.split(" ")[1]} processo(s)'
        plt.plot(tempo, vazao_total_list, label=label)
    plt.xlabel("Tempo")
    plt.ylabel("Vazão Total (Mbps)")
    plt.title("Variação da Vazão Total por Tempo - Reno")
    plt.legend()

    plt.tight_layout()
    plt.show()
