import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

donnee = pd.read_csv("liste_de_données_initiales.csv", encoding = "utf-16")
print(donnee)
donnee.drop('0', axis = 1, inplace = True)
donnee.drop('303', axis = 1, inplace = True)
donnee.columns = ["Date", "Open", "High", "Low", "Close"]
donnee['Date'] = pd.to_datetime(donnee['Date'], format="%Y.%m.%d")
donnee['Annee'] = donnee['Date'].dt.year

array_max = []
array_min = []
current_year = donnee['Annee'][0]
current_max = donnee['High'][0]
current_min = donnee['Low'][0]
# Boucle pour déterminer les max et min de chaque années
for i in range(1, len(donnee)):
    if donnee['Annee'][i] == current_year:
        if donnee['High'][i] > current_max:
            current_max = donnee['High'][i]
        if donnee['Low'][i] < current_min:
            current_min = donnee['Low'][i]     
    else:
        array_max.append(current_max)
        array_min.append(current_min)
        current_year = donnee['Annee'][i]
        current_max = donnee['High'][i]
        current_min = donnee['Low'][i]
array_max.append(current_max)
array_min.append(current_min)  
np_array_max = np.array(array_max)
np_array_min = np.array(array_min)
print(np_array_max)
print(np_array_min)

array_max2 = []
array_min2 = []
current_year2 = donnee['Annee'][0]
current_max2 = donnee['Open'][0]
current_min2 = donnee['Close'][0]
# Boucle pour déterminer les max et min de chaque années
for i in range(1, len(donnee)):
    if donnee['Annee'][i] == current_year2:
        if donnee['Open'][i] > current_max2:
            current_max2 = donnee['Open'][i]
        if donnee['Close'][i] < current_min2:
            current_min2 = donnee['Close'][i]     
    else:
        array_max2.append(current_max2)
        array_min2.append(current_min2)
        current_year2 = donnee['Annee'][i]
        current_max2 = donnee['Open'][i]
        current_min2 = donnee['Close'][i]
array_max2.append(current_max2)
array_min2.append(current_min2)  
np_array_max2 = np.array(array_max2)
np_array_min2 = np.array(array_min2)
# Parametres selon la version discrétisée du Mouvement Brownien Géométrique
initial_price = donnee['Close'].iloc[-1]   # Prix initial de l'actif.
mu = ((np_array_max2 - np_array_min2)/np_array_min2).mean()    # Rendement annuel attendue
print(mu)
sigma = ((np_array_max - np_array_min)/np_array_min).mean()  # Volatilité annuelle attendue
print(sigma)  
T = 1    # Temps en année de la simulation
N = 365   # Nombre de pas par an
dt = T / N
nb_simulation = 10000

# Simulation 
y_repartition = []
for i in range (nb_simulation):
    prices = [initial_price]
    for j in range(N):
        # calcul du choc aléatoire
        choc = np.random.normal(loc = mu * dt, scale = sigma * np.sqrt(dt))
        prices.append(prices[-1]*np.exp(choc))
    y_repartition.append(prices[-1])
    plt.plot(prices)

plt.title("Simulation de Monte Carlo")
plt.xlabel("Nombre de pas")
plt.ylabel("Prix de l'actif")
plt.show()
plt.hist(y_repartition, bins = 100, rwidth = 0.8)
plt.title("Répartition des résultats")
plt.xlabel("Simulation")
plt.ylabel("Prix de l'actif")
plt.show()