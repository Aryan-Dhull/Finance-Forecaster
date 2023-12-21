from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt

# Your feature and target variables
features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days', 'Daily Return', 'Close1', 'Close_2', 'Close_3']
target = 'Next_Day_Closing_Price'

# Create lists to store errors and sample sizes
train_errors_svm = []
test_errors_svm = []
sample_sizes = []

X_test_data=MSFT_standardized[features][2601:]
Y_test_data=MSFT[target][2601:]

X_train_data=MSFT_standardized[features][:2601]
Y_train_data=MSFT[target][:2601]


for sample_size in range(750, len(MSFT_standardized), 1):
    sample_sizes.append(sample_size)
    X_train = X_train_data[:sample_size]
    y_train = Y_train_data[:sample_size]

    # SVM regressor model
    svm_regressor = SVR(kernel='linear')
    svm_regressor.fit(X_train, y_train)
    predictions_svm_train = svm_regressor.predict(X_train)
    predictions_svm_test = svm_regressor.predict(X_test_data)

    # Calculate errors and append to lists
    train_errors_svm.append(mean_squared_error(y_train, predictions_svm_train))
    test_errors_svm.append(mean_squared_error(Y_test_data, predictions_svm_test))

# Plotting the errors as a function of sample size
plt.figure(figsize=(10, 6))
plt.plot(sample_sizes, train_errors_svm, label='SVM Train', color='blue')
plt.plot(sample_sizes, test_errors_svm, label='SVM Test', color='orange')

plt.xlabel('Number of Samples')
plt.ylabel('Mean Squared Error')
plt.title('SVM Training and Testing Errors vs. Number of Samples')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days', 'Daily Return', 'Close1', 'Close_2', 'Close_3']
target = 'Next_Day_Closing_Price'

X = MSFT_standardized[features]
y = MSFT[target]

X_train = X.iloc[:train_size]
X_test = X.iloc[train_size:]

y_train = y[:train_size]
y_test = y[train_size:]
svm_regressor = SVR(kernel = 'linear')
svm_regressor.fit(X_train, y_train)
predictions = svm_regressor.predict(X_test)
r2_accuracy = r2_score(y_test, predictions)

print(f'R^2 Accuracy: {r2_accuracy:.2f}')

mse = mean_squared_error(y_test, predictions)

print(f'Mean Squared Error: {mse:.2f}')

predictions = svm_regressor.predict(X_train)
r2_accuracy = r2_score(y_train, predictions)

print(f'R^2 Accuracy: {r2_accuracy:.2f}')

mse = mean_squared_error(y_train, predictions)

print(f'Mean Squared Error: {mse:.2f}')
