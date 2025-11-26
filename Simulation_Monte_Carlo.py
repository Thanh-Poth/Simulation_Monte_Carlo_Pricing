import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

class StockSimulator :
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.data = yf.download(ticker, start = start_date, end = end_date)
        self.data["Log_return"] = np.log(self.data['Close'] / self.data['Close'].shift(1))

    def calculate_params(self) :
        self.mu = self.data['Log_return'].mean() * 252
        self.sigma = self.data['Log_return'].std() * np.sqrt(252)
        self.last_price = self.data['Close'].iloc[-1].item()

        print(f'Paramètres pour {self.ticker}, prix initiale = {self.last_price}, mu = {self.mu}, sigma = {self.sigma}')

    def simulation(self, horizon = 1, simulations = 100):
        dt = 1 / 252
        step = int(horizon * 252)
        self.simulations = simulations
        random_perturbations = np.random.normal(0, 1, (step, self.simulations))
        
        daily_price = np.exp((self.mu - 0.5 * self.sigma**2) * dt + self.sigma * np.sqrt(dt) * random_perturbations)

        price_points = np.vstack([np.ones((1, self.simulations)), daily_price])

        self.simulated_prices = self.last_price * price_points.cumprod(axis = 0)
        self.final_price = self.simulated_prices[-1, :]

    def plot_results(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.simulated_prices[:, :], alpha=0.5, linewidth=1)

        plt.title(f"Simulation de Monte Carlo ({self.simulations} tirages)")
        plt.xlabel("Jours de trading")
        plt.ylabel("Prix de l'actif")
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.hist(self.final_price, bins=100, rwidth=0.8, color='skyblue', edgecolor='black')
        mean_price = np.mean(self.final_price)
        plt.axvline(mean_price, color='r', linestyle='dashed', linewidth=1, label=f'Moyenne: {mean_price:.2f}')
        plt.title("Répartition des prix finaux")
        plt.xlabel("Prix de l'actif")
        plt.ylabel("Fréquence")
        plt.legend()
        plt.show()

sim = StockSimulator("NVDA", "2020-01-01", "2023-01-01") # Apple, de 2020 à 2023
sim.calculate_params()
sim.simulation(horizon=1, simulations=5000) # Prévision sur 1 an
sim.plot_results()