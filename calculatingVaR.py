import numpy as np
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
from scipy.stats import norm

tickers = ['AAPL', 'META', 'C', 'DIS', 'F', 'MSFT', 'MS', 'GME', 'TSLA', 'AMZN']
weights = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])

start = dt.datetime(2019,1,1)
end = dt.datetime.now()

df = yf.download(tickers, start, end)['Adj Close']

returns = df.pct_change()

cov_matrix = returns.cov()

avg_returns = returns.mean()
count = returns.count()[0]

port_mean = avg_returns @ weights
port_std = np.sqrt(weights.T @ cov_matrix @ weights)

x = np.arange(-0.05, 0.055, 0.001)
norm_dist = norm.pdf(x, port_mean, port_std)

plt.plot(x, norm_dist, color = 'r')
plt.show()

confidence_level = 0.05

VaR = norm.ppf(confidence_level, port_mean, port_std)
print(VaR)

# I have 95% confidence that my portfolio will not lose more than %3.3 in one day.
# That is for the end date: July 2nd 2023.

