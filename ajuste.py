from math import sqrt

full = str(input("Deseja uma resposta completa? (S/N)")).upper()

f = open("ajuste.txt", "r")


#Variables
n = int(f.readline())

x = []
y = []

xSquared = []

xy = []

xSum = 0
ySum = 0
xSquaredSum = 0
xySum = 0

#Reading values from file
for c in range(n):
    k = list(f.readline())
    k = k[:len(k)-1]
    k = ''.join(k)

    x.append(float(k))

    xSquared.append(float(k)**2)

for c in range(n):
    k = list(f.readline())
    k = k[:len(k)-1]
    k = ''.join(k)

    y.append(float(k))

    xy.append(x[c] * float(k))

def sum(array):
    sum = 0
    for c in array:
        sum += c

    return sum

#Calculating the sum
xSum = sum(x)
ySum = sum(y)
xSquaredSum = sum(xSquared)
xySum = sum(xy)

#Calculating the coeficients
linearCoef = (ySum * xSquaredSum - xSum * xySum) / (n * xSquaredSum - xSum**2)
angularCoef = (n * xySum - xSum * ySum) / (n * xSquaredSum - xSum**2)


#Calculating sigmaY
delta = []
deltaSquared = []
for c in range(n):
    delta.append((y[c] - linearCoef - angularCoef * x[c]))
    deltaSquared.append( (y[c] - linearCoef - angularCoef * x[c])**2 )

sigmaY = sqrt(sum(deltaSquared)/(n-2))


#Calculating sigmaA and sigmaB
sigmaLinear = sigmaY * sqrt(xSquaredSum / (n * xSquaredSum - xSum**2))
sigmaAngular = sigmaY * sqrt(n / (n * xSquaredSum - xSum**2))

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

print("A= " + str(a) + " +- " + str(sigmaA))
print("B= " + str(b) + " +- " + str(sigmaB))    

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
    