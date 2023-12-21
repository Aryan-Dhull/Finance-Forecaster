from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

# Your feature and target variables
features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days', 'Daily Return', 'Close1', 'Close_2', 'Close_3']
target = 'Next_Day_Closing_Price'

# Create lists to store errors and sample sizes
train_errors_lr = []
test_errors_lr = []
train_errors_ridge = []
test_errors_ridge = []
sample_sizes = []

X_test_data=MSFT_standardized[features][2601:]
Y_test_data=MSFT[target][2601:]

X_train_data=MSFT_standardized[features][:2601]
Y_train_data=MSFT[target][:2601]


for sample_size in range(750, len(MSFT_standardized), 1):
    sample_sizes.append(sample_size)
    X_train = X_train_data[:sample_size]
    y_train = Y_train_data[:sample_size]


    # Linear Regression model
    linear_regression_model = LinearRegression()
    linear_regression_model.fit(X_train, y_train)
    predictions_lr_train = linear_regression_model.predict(X_train)
    predictions_lr_test = linear_regression_model.predict(X_test_data)

    # Ridge Regression model
    ridge_reg = Lasso(alpha=1.5)
    ridge_reg.fit(X_train, y_train)
    predictions_ridge_train = ridge_reg.predict(X_train)
    predictions_ridge_test = ridge_reg.predict(X_test_data)

    # Calculate errors and append to lists
    train_errors_lr.append(mean_squared_error(y_train, predictions_lr_train))
    test_errors_lr.append(mean_squared_error(Y_test_data, predictions_lr_test))
    train_errors_ridge.append(mean_squared_error(y_train, predictions_ridge_train))
    test_errors_ridge.append(mean_squared_error(Y_test_data, predictions_ridge_test))

# Plotting the errors as a function of sample size
plt.figure(figsize=(10, 6))
plt.plot(sample_sizes, train_errors_lr, label='Linear Regression Train', color='blue')
plt.plot(sample_sizes, test_errors_lr, label='Linear Regression Test', color='orange')

plt.xlabel('Number of Samples')
plt.ylabel('Mean Squared Error')
plt.title('Training and Testing Errors vs. Number of Samples')
plt.legend()
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))
plt.plot(sample_sizes, train_errors_ridge, label='Ridge Regression Train', color='green')
plt.plot(sample_sizes, test_errors_ridge, label='Ridge Regression Test', color='red')
plt.xlabel('Number of Samples')
plt.ylabel('Mean Squared Error')
plt.title('Training and Testing Errors vs. Number of Samples')
plt.legend()
plt.grid(True)
plt.show()

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Your feature and target variables
features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days', 'Daily Return', 'Close1', 'Close_2', 'Close_3']
target = 'Next_Day_Closing_Price'

# Splitting the data into training and testing sets
train_size = int(0.7 * len(MSFT_standardized))
X_train = MSFT_standardized[features][:train_size]
X_test = MSFT_standardized[features][train_size:]
y_train = MSFT[target][:train_size]
y_test = MSFT[target][train_size:]

# Linear Regression model
linear_regression_model = LinearRegression()
linear_regression_model.fit(X_train, y_train)
predictions_lr_train = linear_regression_model.predict(X_train)
predictions_lr_test = linear_regression_model.predict(X_test)

# Ridge Regression model
ridge_reg = Ridge(alpha=1.5)
ridge_reg.fit(X_train, y_train)
predictions_ridge_train = ridge_reg.predict(X_train)
predictions_ridge_test = ridge_reg.predict(X_test)

# Calculate errors
mse_lr_train = mean_squared_error(y_train, predictions_lr_train)
r2_lr_train = r2_score(y_train, predictions_lr_train)
mse_lr_test = mean_squared_error(y_test, predictions_lr_test)
r2_lr_test = r2_score(y_test, predictions_lr_test)

mse_ridge_train = mean_squared_error(y_train, predictions_ridge_train)
r2_ridge_train = r2_score(y_train, predictions_ridge_train)
mse_ridge_test = mean_squared_error(y_test, predictions_ridge_test)
r2_ridge_test = r2_score(y_test, predictions_ridge_test)

# Print the results
print('Linear Regression:')
print(f'Training Mean Squared Error: {mse_lr_train:.2f}, R-squared: {r2_lr_train:.2f}')
print(f'Testing Mean Squared Error: {mse_lr_test:.2f}, R-squared: {r2_lr_test:.2f}')

print('\nRidge Regression:')
print(f'Training Mean Squared Error: {mse_ridge_train:.2f}, R-squared: {r2_ridge_train:.2f}')
print(f'Testing Mean Squared Error: {mse_ridge_test:.2f}, R-squared: {r2_ridge_test:.2f}')

# Plotting the errors
plt.figure(figsize=(10, 6))
models = ['Linear Regression Train', 'Linear Regression Test', 'Ridge Regression Train', 'Ridge Regression Test']
errors = [mse_lr_train, mse_lr_test, mse_ridge_train, mse_ridge_test]
plt.bar(models, errors, color=['blue', 'orange', 'green', 'red'])
plt.ylabel('Mean Squared Error')
plt.title('Model Performance Comparison')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import Ridge , Lasso


features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days', 'Daily Return', 'Close1', 'Close_2', 'Close_3']
target = 'Next_Day_Closing_Price'

X = MSFT_standardized[features]
y = MSFT[target]

train_size = int(0.7 * len(X))

X_train = X.iloc[:train_size]
X_test = X.iloc[train_size:]

y_train = y.iloc[:train_size]
y_test = y.iloc[train_size:]

linear_regression_model = LinearRegression()
linear_regression_model.fit(X_train, y_train)

predictions = linear_regression_model.predict(X_test)

mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print('Linear Regression:')
print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared Score: {r2:.2f}")


predictions = linear_regression_model.predict(X_train)

mse = mean_squared_error(y_train, predictions)
r2 = r2_score(y_train, predictions)


print(f"Mean Squared Error: {mse:.2f}")
print(f"R-squared Score: {r2:.2f}")
print()

ridge_reg = Ridge(alpha=1.5)

# Train the Ridge Regression model on the training data
ridge_reg.fit(X_train, y_train)

y_pred_ridge = ridge_reg.predict(X_train)

# Evaluate the Ridge Regression model's performance
mse_ridge = mean_squared_error(y_train, y_pred_ridge)
r2_ridge = r2_score(y_train, y_pred_ridge)

print('Ridge Regression:')
print(f'Mean Squared Error (MSE): {mse_ridge:.2f}')
print(f'R-squared (R2): {r2_ridge:.2f}')

# Make predictions on the test data
y_pred_ridge = ridge_reg.predict(X_test)

# Evaluate the Ridge Regression model's performance
mse_ridge = mean_squared_error(y_test, y_pred_ridge)
r2_ridge = r2_score(y_test, y_pred_ridge)

print(f'Mean Squared Error (MSE): {mse_ridge:.2f}')
print(f'R-squared (R2): {r2_ridge:.2f}')
