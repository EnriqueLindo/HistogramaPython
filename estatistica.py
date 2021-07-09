import math
import matplotlib.pyplot as graph
from matplotlib.ticker import FormatStrFormatter

#Array do tipo [ValorDaAmostra, Frequencia]
frequency = []
#Lista com todas as amostras, usada para construir o histograma
histogram = []
precision = 2
fModa = 0

numData = 0
media = 0
moda = 0
mediana = 0
dp = 0
dpMedia = 0
nBins = 0

def calcMMM():
    global media, mediana, moda, numData, fModa
    #Calculando a média    
    for c in frequency:
        media += c[0] * c[1]
        numData += c[1]
        #Calculando a moda
        if(c[1] > fModa):
            moda, fModa = c[0], c[1]

    media = round(media/numData, precision)
    #Calculando a mediana
    if(len(histogram) % 2 == 0):
        mediana = histogram[len(histogram) // 2]
    else:
        mediana = (histogram[len(histogram)//2] + histogram[len(histogram)//2 + 1]) / 2

def calcDp():
    global dp, dpMedia, numData
    #Calculando o desvio padrão
    for c in frequency:
        for d in range(c[1]):
            dp += (c[0] - media) ** 2

    dp = dp/(numData-1)

    dp = round(math.sqrt(dp), precision)

    dpMedia = dp/math.sqrt(numData)

def constructHist():
    global nBins, media
    nBins = int(math.sqrt(numData))
    interSz = round((frequency[len(frequency)-1][0] - frequency[0][0])/nBins, 3)

    intervalos = []
    for c in range(nBins+2):
        i = round(frequency[0][0] + c * interSz, 3)
        intervalos.append(i)

    #Configurando o histograma

    interMedia = []
    alturaMedia = 0

    for c in range(1, len(intervalos)-1):
        if intervalos[c] > media >= intervalos[c-1]:
            interMedia.append(intervalos[c-1])
            interMedia.append(intervalos[c])
            break
    for c in frequency:
        if interMedia[1] > c[0] >= interMedia[0]:
            alturaMedia += c[1]

    titulo = str(input("Digite um titulo para o histograma: "))
    tituloX = str(input("Digite um titulo para o eixo X: "))
    tituloY = str(input("Digite um titulo para o eixo Y: "))

    fPoint = '%.' + str(precision) + 'f'

    graph.style.use('seaborn-darkgrid')

    fig, ax = graph.subplots()

    ax.xaxis.set_major_formatter(FormatStrFormatter(fPoint))

    #graph.hist(x=histograma, bins=nBins)
    graph.hist(x=histogram, bins=intervalos)

    x1, y1 = [media, media], [0, alturaMedia]

    graph.plot(x1, y1, color='red', marker='o', linestyle='dashed', linewidth=1)

    graph.title(titulo)
    graph.xlabel(tituloX)
    graph.ylabel(tituloY)
    graph.show()


def execute(sourceFile, options):
    arq = open(sourceFile, "r")
    reading = True
    while reading:
        y = arq.readline()

        if(y == ""):
            reading = False
        else:
            y = float(y)

            histogram.append(y)

            f = 0
            if(len(frequency) != 0):
                for c in frequency:
                    if c[0] == y:
                        c[1] += 1
                        f = 1
                        break
            if (f == 0):
                frequency.append([y, 1])

    frequency.sort()
    histogram.sort()
    calcMMM()
    calcDp()
    constructHist()

    print('===============================')
    print("O numero de dados é: ", numData)
    print("A média é: ", media)
    print("A moda é: ", moda)
    print("A mediana é: ", mediana)
    print("O desvio padrão é: ", dp)
    print("O desvio padrão da média é: ", dpMedia)
    print("O menor valor é: ", frequency[0][0])
    print("O maior valor é: ", frequency[len(frequency)-1][0])
    print("O numero de bins é: ", nBins)

    for c in frequency:
        print(c)