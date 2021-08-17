from math import sqrt
import matplotlib.pyplot as plt
import estatistica

plt.style.use('bmh')

#Variables
n = 0

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

remainders = []
rem_percentage = []

#Auxiliar func
def sum(array):
    global sigma_y

    sum = 0
    for c in range(len(array)):
        sum += array[c] / (sigma_y[c]**2)

    return sum

def mod(x):
    if x < 0:
        return x * (-1)
    
    return x

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

def calcSum():
    global xSum, ySum, xSquaredSum, xySum, sigmaSum, x, y, xSquared, xy, n

    xSum = sum(x)
    ySum = sum(y)
    xSquaredSum = sum(xSquared)
    xySum = sum(xy)
    sigmaSum = sum([1]*n)

def countSigAlg(x):
    x = str(x).split(".")

    return len(x[1])

def resetVariables():
    global n, x, sigma_x, y, sigma_y, xSquared, xy, xSum, ySum, xSquaredSum, xySum, sigmaSum, remainders, rem_percentage

    n = 0
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
    remainders = []
    rem_percentage = []


#Actual func
def readFile(sourceFile):
    global n, x, sigma_x, y, sigma_y, xSquared, xy

    f = open(sourceFile, "r")
    while True:
        if f.readline() != "":
            n += 1
        else:
            break
    f.close()

    n = n//2

    f = open(sourceFile, "r")

    values = f.readlines()
    xValues = values[0:n]
    yValues = values[n:]

    for c in range(n):
        k = list(xValues[c])

        if c != n-1:
            k = k[:len(k)-1]

        k = ''.join(k)
        k = k.split(";")

        x.append(float(k[0]))
        if len(k) > 1:            
            sigma_x.append(float(k[1]))
        else:
            sigma_x.append(1.0)            

        xSquared.append(float(k[0])**2)

    for c in range(n):
        k = list(yValues[c])

        if c != n-1:
            k = k[:len(k)-1]

        k = ''.join(k)
        k = k.split(";")

        y.append(float(k[0]))
        if len(k) > 1:            
            sigma_y.append(float(k[1]))
        else:
            sigma_y.append(1.0)  

        xy.append(x[c] * float(k[0]))

    f.close()

def calcCoef():
    global ySum, xSquaredSum, xSum, xySum, sigmaSum

    linearCoef = (ySum * xSquaredSum - xSum * xySum) / (sigmaSum * xSquaredSum - xSum**2)
    angularCoef = (sigmaSum * xySum - xSum * ySum) / (sigmaSum * xSquaredSum - xSum**2)

    sigmaLinear = (mod(xSquaredSum / (sigmaSum * xSquaredSum - xSum**2)))
    sigmaAngular = (mod(sigmaSum / (sigmaSum * xSquaredSum - xSum**2)))

    return [linearCoef, sigmaLinear], [angularCoef, sigmaAngular]

def calcRemainders(linearCoef, angularCoef):
    global y, remainders, rem_percentage, sigma_y, x
    for c in range(len(y)):
        expectedY = linearCoef + angularCoef * x[c]

        r = (y[c] - expectedY) / sigma_y[c]
        remainders.append(r)

        p = r/expectedY * 100
        rem_percentage.append(p)

def constructHistRem():
    global remainders

    f = open("hist.txt", "w")
    for c in remainders:
        f.write(str(c))

        if c != remainders[len(remainders) - 1]:
            f.write("\n")

    f.close()

    estatistica.execute("hist.txt", {"hist": True})

def constructGraph(linearCoef, angularCoef):
    global x, y, sigma_x, sigma_y

    plt.plot(x, y, 'ro')

    plt.axline((x[0], x[0]*angularCoef + linearCoef), (x[1], x[1]*angularCoef + linearCoef))
    
    for c in range(len(x)):
        x1, y1 = [x[c], x[c]], [y[c] - sigma_y[c], y[c] + sigma_y[c]]
        plt.plot(x1, y1, marker='_', color='black')

        x2, y2 = [x[c] - sigma_x[c], x[c] + sigma_x[c]], [y[c] ,y[c]]
        plt.plot(x2, y2, marker="_", color='black')

    plt.show()

def construcRemG():
    global rem_percentage

    xaxis = []
    for c in range(len(rem_percentage)):
        xaxis.append(c+1)

    plt.axline((0, 0), (len(xaxis), 0))

    plt.plot(xaxis, rem_percentage, 'ro')

    plt.ylabel("Resíduos (%)")
    plt.xlabel("Ordem de Coleta")

    plt.show()

#Main func
def execute(sourceFile, opts):
    readFile(sourceFile)
    calcSum()

    linearCoef, angCoef = calcCoef()

    ang = myRound(angCoef[0])
    lin = myRound(linearCoef[0])

    sigmaAng = round(angCoef[1], countSigAlg(ang))
    sigmaLin = round(linearCoef[1], countSigAlg(lin))

    #Constructing the graph with de adjust line
    if opts["ajuste"]:
        constructGraph(lin, ang)
    #Constructing the graph of remainders
    if opts["grafResi"]:
        calcRemainders(lin, ang)
        construcRemG()
    #Constructing the histogram of remainders
    if opts["grafResi"]:
        constructHistRem()

    #Reseting the variables
    resetVariables()

    return ang, lin, sigmaAng, sigmaLin

#Calculating sigmaY (for delta and deltasquared, might delete later...)
'''
delta = []
deltaSquared = []
for c in range(n):
    delta.append((y[c] - linearCoef - angularCoef * x[c]))
    deltaSquared.append( (y[c] - linearCoef - angularCoef * x[c])**2 )

sigmaY = sqrt(sum(deltaSquared)/(n-2))
'''
