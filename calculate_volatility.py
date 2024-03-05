import numpy as np

# Generate 20 random close prices (~U[5,12])
close_prices = np.random.uniform(5, 12, 20)

# Calculate log returns
log_returns = np.diff(np.log(close_prices))

# Calculate volatility
volatility = np.std(log_returns)

# Annualize the volatility, because the log returns are daily
annualized_volatility = volatility * np.sqrt(252)

# Print the annualized volatility
print(annualized_volatility)
