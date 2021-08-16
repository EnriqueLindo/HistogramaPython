from math import sqrt
import matplotlib.pyplot as plt
import estatistica

full = str(input("Deseja uma resposta completa? (S/N)")).upper()

f = open("ajuste.txt", "r")


#Variables
n = int(f.readline())

x = []
sigma_x = []
y = []
sigma_y = []

xSquared = []

xy = []

xSum = 0
ySum = 0
xSquaredSum = 0
xySum = 0
sigmaSum = 0

#Reading values from file
for c in range(n):
    k = list(f.readline())
    k = k[:len(k)-1]
    k = ''.join(k)

    k = k.split(";")


    x.append(float(k[0]))
    sigma_x.append(float(k[1]))

    xSquared.append(float(k[0])**2)

for c in range(n):
    k = list(f.readline())
    k = k[:len(k)-1]
    k = ''.join(k)

    k = k.split(";")

    y.append(float(k[0]))
    sigma_y.append(float(k[1]))

    xy.append(x[c] * float(k[0]))

def sum(array):
    sum = 0
    for c in range(len(array)):
        sum += array[c] / (sigma_y[c]**2)

    return sum

def mod(x):
    if x < 0:
        return x * (-1)
    
    return x

#Calculating the sum
xSum = sum(x)
ySum = sum(y)
xSquaredSum = sum(xSquared)
xySum = sum(xy)
sigmaSum = sum([1]*n)

#Calculating the coeficients
linearCoef = (ySum * xSquaredSum - xSum * xySum) / (sigmaSum * xSquaredSum - xSum**2)
angularCoef = (sigmaSum * xySum - xSum * ySum) / (sigmaSum * xSquaredSum - xSum**2)


#Calculating sigmaY (for delta and deltasquared, might delete later...)
delta = []
deltaSquared = []
for c in range(n):
    delta.append((y[c] - linearCoef - angularCoef * x[c]))
    deltaSquared.append( (y[c] - linearCoef - angularCoef * x[c])**2 )

sigmaY = sqrt(sum(deltaSquared)/(n-2))


#Calculating sigmaA and sigmaB
#sigmaLinear = sigmaY * sqrt(mod(xSquaredSum / (sigmaSum * xSquaredSum - xSum**2)))
#sigmaAngular = sigmaY * sqrt(mod(sigmaSum / (sigmaSum * xSquaredSum - xSum**2)))

sigmaLinear = (mod(xSquaredSum / (sigmaSum * xSquaredSum - xSum**2)))
sigmaAngular = (mod(sigmaSum / (sigmaSum * xSquaredSum - xSum**2)))

#Rouding to 2 significant algarisms
def myRound(z):
    k = str(z).split(".")
    k = list(k[1])

    sigAlg = 0
    for c in k:
        if c == '0':
            sigAlg += 1
        else:
            break

    return round(z, 2 + sigAlg)

#Printing the results
a = myRound(angularCoef)
b = myRound(linearCoef)

sigmaA = myRound(sigmaAngular)
sigmaB = myRound(sigmaLinear)

print("Coef Angular= " + str(a) + " +- " + str(sigmaA))
print("Coef Linear= " + str(b) + " +- " + str(sigmaB))

#Calculating the remainders
remainders = []
rem_percentage = []
for c in range(len(y)):
    expectedY = linearCoef + angularCoef * x[c]

    r = (y[c] - (expectedY)) / sigma_y[c]
    remainders.append(r)

    p = r/expectedY * 100
    rem_percentage.append(p)


if full == "S":
    print("======IMPRIMINDO RESPOSTA COMPLETA======")

    print("x = ", x)
    print("Σx = ", xSum)
    print()

    print("y = ", y)
    print("Σy = ", ySum)
    print()

    print("x² = ", xSquared)
    print("Σx² = ", xSquaredSum)
    print()

    print("xy = ", xy)
    print("Σxy = ", xySum)
    print()

    print("Δ = ", delta)
    print("ΣΔ = ", sum(delta))
    print()

    print("Δ² = ", deltaSquared)
    print("ΣΔ² = ", sum(deltaSquared))
    print()


def constructGraph():
    plt.style.use('bmh')

    plt.plot(x, y, 'ro')

    plt.axline((x[0], x[0]*angularCoef + linearCoef), (x[1], x[1]*angularCoef + linearCoef))
    
    for c in range(len(x)):
        x1, y1 = [x[c], x[c]], [y[c] - sigma_y[c], y[c] + sigma_y[c]]
        plt.plot(x1, y1, marker='_', color='black')

        x2, y2 = [x[c] - sigma_x[c], x[c] + sigma_x[c]], [y[c] ,y[c]]
        plt.plot(x2, y2, marker="_", color='black')

    plt.show()

def construcRemG():
    xaxis = []
    for c in range(len(rem_percentage)):
        xaxis.append(c+1)

    plt.axline((0, 0), (len(xaxis), 0))

    plt.plot(xaxis, rem_percentage, 'ro')

    plt.ylabel("Resíduos (%)")
    plt.xlabel("Ordem de Coleta")

    plt.show()

#Constructing the graph with de adjust line
constructGraph()
#Constructing the graph of remainders
construcRemG()

#Constructing the histogram of remainders
f = open("hist.txt", "w")
for c in remainders:
    f.write(str(c))

    if c != remainders[len(remainders) - 1]:
        f.write("\n")

f.close()

estatistica.execute("hist.txt", [])
