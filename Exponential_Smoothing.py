import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days', 'Daily Return', 'Close1', 'Close_2', 'Close_3']
target = 'Next_Day_Closing_Price'

X = MSFT_standardized[features]
y = MSFT[target]
X_train = X.iloc[:train_size]
X_test = X.iloc[train_size:]
y_train = y[:train_size]
y_test = y[train_size:]

alpha = 0.2  # Adjust as needed

# Apply Simple Exponential Smoothing without forecasting for each feature
smoothed_data = pd.DataFrame(index=MSFT_standardized.index)

for feature in features:
    smoothed_values = [MSFT_standardized[feature].iloc[0]]  # Initial value is the first data point

    # Apply the exponential smoothing formula to smooth the data
    for i in range(1, len(MSFT_standardized)):
        smoothed_values.append(alpha * MSFT_standardized[feature].iloc[i-1] + (1 - alpha) * smoothed_values[i-1])

    # Store the smoothed values in the DataFrame
    smoothed_data[feature] = smoothed_values

# Visualize the smoothed data for each feature
plt.figure(figsize=(15, 8))
for feature in features:
    plt.plot(MSFT_standardized[feature], label=f'Original {feature}')
    plt.plot(smoothed_data[feature], label=f'Smoothed {feature}', linestyle='dashed')
    plt.title('Exponential Smoothing for Data Smoothing (No Forecasting) - 11 Features')
    plt.legend()
    plt.show()
