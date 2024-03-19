import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import yfinance as yf

# Define the ticker symbol and data range for historical data
ticker_symbol = "AAPL"
ticker_symbol_2 = "GOOG"
start_date = "2023-01-01"
end_date = "2023-12-31"

# Fetch historical data
stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
stock_data_2 = yf.download(ticker_symbol_2, start=start_date, end=end_date)

# Extract the 'Close' prices for both stocks
print(stock_data.head())
print(stock_data_2.head())

closing_prices = np.array(stock_data['Close'])
closing_prices_2 = np.array(stock_data_2['Close'])

# Reshape the 1D arrays to 2D arrays
closing_prices = closing_prices.reshape(-1, 1)
closing_prices_2 = closing_prices_2.reshape(-1, 1)

# Perform linear regression
model = LinearRegression()
model.fit(closing_prices, closing_prices_2)

# Predict closing prices using the linear model
predicted_prices = model.predict(closing_prices)

# Plot the actual closing prices and the linear regression line
plt.figure(figsize=(10, 6))
plt.scatter(closing_prices, closing_prices_2, color='blue', label='Actual Closing Prices')
plt.plot(closing_prices, predicted_prices, color='red', linewidth=2, label='Linear Regression')
plt.title('Linear Regression on Closing Prices of ' + ticker_symbol)
plt.xlabel('Closing Price ' + ticker_symbol)
plt.ylabel('Closing Price ' + ticker_symbol_2)
plt.legend()
plt.grid(True)
plt.show()

# Print the coefficients of the linear model
print("Intercept:", model.intercept_)
print("Coefficient:", model.coef_[0])

# Define the closing price of the first ticker for which you want to predict the price of the second ticker
price_of_first_ticker = 120

# Reshape the price of the first ticker to a 2D array
price_of_first_ticker_2d = np.array([[price_of_first_ticker]])

# Predict the closing price of the second ticker based on the price of the first ticker
predicted_price_of_second_ticker = model.predict(price_of_first_ticker_2d)

print("Predicted closing price of", ticker_symbol_2, "when", ticker_symbol, "has a closing price of", price_of_first_ticker, ":", predicted_price_of_second_ticker)
