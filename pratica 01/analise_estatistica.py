import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy import stats

#Caminho do arquivo
file_path = "pratica 01/dados_digitalizados.xlsx"
#Lendo o arquivo
df = pd.read_excel(file_path)
#transformando em um numpy
df_numpy = df.to_numpy()

#Variáveis de armazenamento
data = np.empty(5, dtype=object)
estatistica = np.empty((5, 11), dtype=object)
dist_normal = np.empty(4, dtype=object)
colors = np.array(["#0000ff55", "#0000ffaa", "#00ff0055", "#00ff00aa"])
tracado = np.array(["r--", "r-", "m--", "m-"])

#Pegando os dados dos resistores (0->AzulLCR, 1->AzulMultimetro, 2->VerdeLCR, 3->VerdeMultimetro)
data[0] = np.array(["Resistores AZUIS - LCR (kΩ)", "Resistores AZUIS - Multímetro (kΩ)", "Resistores VERDES - LCR (Ω)", "Resistores VERDES - Multímetro (Ω)"]).astype(str)
data[1] = df_numpy[2:70, 2].astype(float)
data[2] = df_numpy[2:70, 3].astype(float)
data[3] = df_numpy[2:96, 6].astype(float)
data[4] = df_numpy[2:96, 7].astype(float)

#Cabeçalho da variável de armazenamento de dados de estatística
estatistica[0] = ["Média", "Mediana", "Moda", "Frequência Moda", "Desv. Pad. Pop.", "Variância", "Coef. Variação (%)", "Minimo", "Máximo", "Amplitude", "Nº Classes"]

#Criando figura com subplots para exibir os gráficos
fig, axes = plt.subplots(2, 2, figsize = (12, 8))
axes = axes.flatten()

for i, dados in enumerate(data):
    #Se estiver no cabeçalho, pule para a próxima linha
    if i == 0:
        continue

    #Pegando a MÉDIA dos resistores
    media = np.average(dados)
    #Pegando a MEDIANA dos resistores
    mediana = np.median(dados)
    #Pegando a MODA dos resistores
    moda = stats.mode(dados, keepdims=True).mode[0]
    #Pegando a FREQUÊNCIA DA MODA
    moda_frequence = stats.mode(dados, keepdims=True).count[0]
    #Pegando o DESVIO PADRÃO POPULACIONAL dos resistores. Populacional ddof=0, amostral ddof=1.
    std = np.std(dados, ddof=0)
    #Pegando a VARIÂNCIA
    var = std**2
    #Pegando o COEFICIENTE DE VARIAÇÃO
    cv = 100 * std / media
    #Pegando o MÍNIMO
    minimo = np.min(dados)
    #Pegando o MÁXIMO
    maximo = np.max(dados)
    #Pegando a AMPLITUDE
    amplitude = maximo - minimo
    #Pegando o Nº DE CLASSES para o Histograma
    n_classes_hist = int(np.sqrt(len(dados)))

    #Distribuição normal dos dados
    x = np.linspace(minimo, maximo, 100)
    pdf = norm.pdf(x, media, std)
    dist_normal[i - 1] = np.array([x, pdf])

    #Armazenando
    estatistica[i] = [round(media, 4), round(mediana, 4), round(moda, 4), moda_frequence, round(std, 4), round(var, 4), round(cv, 4), round(minimo, 4), round(maximo, 4), round(amplitude, 4), n_classes_hist]

    #Plotando o histograma
    contagem, limites_bins, patches = axes[i-1].hist(dados, density=True, bins=n_classes_hist, label="Observações")
    axes[i-1].set_title(data[0][i-1])
    axes[i-1].set_xlabel("Intervalos")
    axes[i-1].set_ylabel("Frequência")
    axes[i-1].set_xticks(limites_bins)
    #Colocando hachura
    if (i-1)%2 == 0: #se par
        for rect in patches:
            rect.set_facecolor(colors[i - 1])   # fundo
            rect.set_edgecolor('black')         # cor da hachura
            rect.set_hatch('/')                 # padrão
            rect.set_linewidth(1.5)             # espessura da hachura
    else:
        for rect in patches:
            rect.set_facecolor(colors[i - 1])   # fundo
            rect.set_edgecolor('black')          # cor da hachura
            rect.set_hatch('.')                 # padrão
            rect.set_linewidth(1.5)             # espessura da hachura

    # Plotando a distribuição normal
    axes[i-1].plot(x, pdf, tracado[i - 1], linewidth = 2, label = f"Normal ajustada\nμ={round(media, 4)}, σ={round(std, 4)}")

    #Habilitando legenda dos dados
    axes[i-1].legend()

# Convertendo a tabela estatística em DataFrame
estat_df = pd.DataFrame(estatistica[1:], columns=estatistica[0], index=data[0])
#Salvando resultados em um arquivo xlsx
estat_df.to_excel("pratica 01/estatisticas_resistores.xlsx", sheet_name="Estatísticas", index=True)


plt.tight_layout()
plt.show()
