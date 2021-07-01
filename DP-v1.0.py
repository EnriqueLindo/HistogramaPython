import math
import matplotlib.pyplot as graph
from matplotlib.ticker import FormatStrFormatter

#Array do tipo [ValorDaAmostra, Frequencia]
valores = []
#Lista com todas as amostras, usada para construir o histograma
histograma = []

#Input da precisao a ser considerada nos calculos e nos round()
precisao = int(input("Digite o numero de casas decimais: "))

#Lendo os valores das amostras
modo = int(input("Ler de um arquivo(0) ou digitar manualmente(1)? "))

    ##Através de um arquivo
if(modo == 0):
    arq = open("valores.txt", "r")
    lendo = True
    while lendo:
        y = arq.readline()

        if(y == ""):
            lendo = False
        else:
            y = float(y)

            histograma.append(y)

            f = 0

            if(len(valores) != 0):
                for c in valores:
                    if c[0] == y:
                        c[1] += 1
                        f = 1
                        break

            if (f == 0):
                valores.append([y, 1])
    ##Atraves do input manual
else:
    running = True
    while running:
        x = float(input("Digite um valor: "))
        
        if(x > 0):
            histograma.append(x)

            f = 0

            if(len(valores) != 0):
                for c in valores:
                    if c[0] == x:
                        c[1] += 1
                        f = 1
                        break

            if (f == 0):
                valores.append([x, 1])

        else: 
            running = False

valores.sort()

print("=================================")

#Calculando a média e printando as frequencias
media = 0
n = 0
for c in valores:
    media += c[0] * c[1]
    n += c[1]

    print("Valor = {}   //   Frequencia = {}".format(c[0], c[1]))

media = round(media/n, precisao)

#Calculando o desvio padrão
sum = 0
for c in valores:
    for d in range(c[1]):
        sum += (c[0] - media) ** 2

sum = sum/(n-1)

sum = round(math.sqrt(sum), precisao)

#Calculo do numero de bins (ta no local errado)
nBins = int(math.sqrt(n))

#Printando os resultados
print()
print("A média é: ", media)
print("O desvio padrão é: ", sum)
print("O menor valor é: ", valores[0][0])
print("O maior valor é: ", valores[len(valores)-1][0])
print("O numero de bins é: ", nBins)

#Calculando o tamanho do intervalo e os intervalos em si

intervalo = round((valores[len(valores)-1][0] - valores[0][0])/nBins, 3)

intervalos = []
for c in range(nBins+2):
    i = round(valores[0][0] + c * intervalo, 3)
    intervalos.append(i)

#Configurando o histogrma

titulo = str(input("Digite um titulo para o histograma: "))
tituloX = str(input("Digite um titulo para o eixo X: "))
tituloY = str(input("Digite um titulo para o eixo Y: "))

fPoint = '%.' + str(precisao) + 'f'

graph.style.use('seaborn-darkgrid')

fig, ax = graph.subplots()

ax.xaxis.set_major_formatter(FormatStrFormatter(fPoint))

#graph.hist(x=histograma, bins=nBins)
graph.hist(x=histograma, bins=intervalos)

graph.title(titulo)
graph.xlabel(tituloX)
graph.ylabel(tituloY)
graph.show()
