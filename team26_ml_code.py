# -*- coding: utf-8 -*-
"""TEAM26_ML_Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1r0MJYT3WdUaWdUZuDpZfJuzMaN1rGT6U
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from numpy import log
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.tree import DecisionTreeRegressor

!pip install -q yfinance

from pandas_datareader.data import DataReader
import yfinance as yf
from pandas_datareader import data as pdr
yf.pdr_override()
from datetime import datetime

tech_list = ['AAPL', 'GOOG', 'MSFT', 'AMZN']

end = datetime.now()
start = datetime(end.year - 13, end.month, end.day)
for stock in tech_list:
    globals()[stock] = yf.download(stock, start, end)


company_list = [AAPL, GOOG, MSFT, AMZN]
company_name = ["APPLE", "GOOGLE", "MICROSOFT", "AMAZON"]


for company, com_name in zip(company_list, company_name):
    company["company_name"] = com_name

df = pd.concat(company_list, axis=0)

df

"""**DESCRIPTIVE ANALYSIS**"""

AAPL.describe()

GOOG.describe()

MSFT.describe()

AMZN.describe()

"""**INFO ABOUT THE DATASET**"""

AAPL.info()

GOOG.info()

MSFT.info()

AMZN.info()

"""**ADDING MORE FEATURES LIKE MOVING AVERGAE AND DAILY RETURN**"""

ma_day = [10, 20, 50]

for ma in ma_day:
    for company in company_list:
        column_name = f"MA for {ma} days"
        company[column_name] = company['Adj Close'].rolling(ma).mean()

for company in company_list:
    company['Daily Return'] = company['Adj Close'].pct_change()

"""**PLOT**"""

plt.figure(figsize=(15, 10))
plt.subplots_adjust(top=1.25, bottom=1.2)
for i, company in enumerate(company_list, 1):
    plt.subplot(2, 2, i)
    company['Adj Close'].plot(color='red')
    plt.ylabel('Adj Close')
    plt.xlabel(None)
    plt.title(f"Closing Price of {company_name[i - 1]}")
plt.tight_layout()

plt.figure(figsize=(15, 10))
plt.subplots_adjust(top=1.25, bottom=1.2)

for i, company in enumerate(company_list, 1):
    plt.subplot(2, 2, i)
    company['Volume'].plot(color='red')
    plt.ylabel('Volume')
    plt.xlabel(None)
    plt.title(f"Sales Volume for {tech_list[i - 1]}")
plt.tight_layout()

fig, axes = plt.subplots(nrows=2, ncols=2)
fig.set_figheight(10)
fig.set_figwidth(15)
AAPL[['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot(ax=axes[0,0])
axes[0,0].set_title('APPLE')
GOOG[['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot(ax=axes[0,1])
axes[0,1].set_title('GOOGLE')
MSFT[['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot(ax=axes[1,0])
axes[1,0].set_title('MICROSOFT')
AMZN[['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot(ax=axes[1,1])
axes[1,1].set_title('AMAZON')
fig.tight_layout()

fig, axes = plt.subplots(nrows=2, ncols=2)
fig.set_figheight(10)
fig.set_figwidth(15)
AAPL['Daily Return'].plot(ax=axes[0,0], legend=True, linestyle='--', marker='o')
axes[0,0].set_title('APPLE')
GOOG['Daily Return'].plot(ax=axes[0,1], legend=True, linestyle='--', marker='o')
axes[0,1].set_title('GOOGLE')
MSFT['Daily Return'].plot(ax=axes[1,0], legend=True, linestyle='--', marker='o')
axes[1,0].set_title('MICROSOFT')
AMZN['Daily Return'].plot(ax=axes[1,1], legend=True, linestyle='--', marker='o')
axes[1,1].set_title('AMAZON')
fig.tight_layout()

plt.figure(figsize=(12, 9))
for i, company in enumerate(company_list, 1):
    plt.subplot(2, 2, i)
    company['Daily Return'].hist(bins=50,color='red')
    plt.xlabel('Daily Return')
    plt.ylabel('Counts')
    plt.title(f'{company_name[i - 1]}')
plt.tight_layout()

# Grab all the closing prices for the tech stock list into one DataFrame
closing_df = pdr.get_data_yahoo(tech_list, start=start, end=end)['Adj Close']
# Make a new tech returns DataFrame
tech_rets = closing_df.pct_change()
tech_rets.head()

plt.figure(figsize=(12, 12))
plt.subplot(2, 2, 1)
sns.heatmap(tech_rets.corr(), annot=True, cmap='viridis')
plt.title('Correlation of stock return')
plt.subplot(2, 2, 2)
sns.heatmap(closing_df.corr(), annot=True, cmap='viridis')
plt.title('Correlation of stock closing price')

"""**ANALYZING THE RISK ASSOCIATED WITH EACH STOCK**"""

rets = tech_rets.dropna()
area = np.pi * 20
plt.figure(figsize=(10, 8))
plt.scatter(rets.mean(), rets.std(), s=area)
plt.xlabel('Expected return')
plt.ylabel('Risk')
for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
    plt.annotate(label, xy=(x, y), xytext=(50, 50), textcoords='offset points', ha='right', va='bottom',
                 arrowprops=dict(arrowstyle='-', color='red', connectionstyle='arc3,rad=-0.3'))

"""**ADDING MORE FEATURES LIKE THE PREVIOUS 3 CLOSING PRICES**"""

MSFT['Close1'] = MSFT['Close']
MSFT['Close_2'] = MSFT['Close'].shift(1)
MSFT['Close_3'] = MSFT['Close'].shift(2)
MSFT['Next_Day_Closing_Price'] = MSFT['Close'].shift(-1)
MSFT = MSFT.drop(columns = ['company_name'])
MSFT = MSFT.dropna()
MSFT

MSFT.describe()

"""**CORRELATION HEATMAP FOR MICROSOFT STOCKS**"""

correlation_matrix = MSFT.corr()
plt.figure(figsize=(10, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Correlation Matrix')
plt.show()

"""**STANDARDIZING THE DATASET AND APPLYING K MEANS CLUSTERING**"""

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

columns_to_standardize = ['Open', 'High', 'Low', 'Close', 'Volume','Daily Return','Adj Close', 'MA for 10 days','MA for 20 days','MA for 50 days', 'Close1', 'Close_2', 'Close_3']
MSFT_standardized=MSFT[columns_to_standardize]
y = MSFT['Next_Day_Closing_Price']

scaler = StandardScaler()
MSFT_standardized[columns_to_standardize] = scaler.fit_transform(MSFT_standardized[columns_to_standardize])
MSFT_standardized

columns_for_kmeans =['Open', 'High', 'Low', 'Close','Adj Close', 'MA for 10 days','MA for 20 days','MA for 50 days', 'Close1', 'Close_2', 'Close_3']
Dataset=MSFT[columns_for_kmeans]
scaler = StandardScaler()
Dataset[columns_for_kmeans] = scaler.fit_transform(Dataset[columns_for_kmeans])

num_clusters = 4
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(Dataset[columns_for_kmeans])

cluster_labels = kmeans.labels_
Dataset['Cluster'] = cluster_labels

print("Data points in each cluster:")
print(Dataset['Cluster'].value_counts())

feature1 = 'Low'
feature2 = 'High'

plt.figure(figsize=(8, 6))

for cluster_label in range(num_clusters):
    cluster_data = Dataset[Dataset['Cluster'] == cluster_label]
    plt.scatter(cluster_data[feature1], cluster_data[feature2], label=f'Cluster {cluster_label}', alpha=0.6)

cluster_centers = kmeans.cluster_centers_
plt.scatter(cluster_centers[:, columns_to_standardize.index(feature1)],
            cluster_centers[:, columns_to_standardize.index(feature2)],
            marker='x', s=200, linewidths=3, color='k', label='Cluster Centers')

plt.xlabel(feature1)
plt.ylabel(feature2)
plt.title('K-means Clustering')
plt.legend()
plt.show()

"""**OUTLIER DETECTION USING BOX PLOTS**"""

columns = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'MA for 10 days','MA for 20 days','MA for 50 days','Daily Return', 'Close1', 'Close_2', 'Close_3']

for column_name in columns:
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 6))

    sns.boxplot(x=MSFT[f'{column_name}'])

    Q1 = MSFT[f'{column_name}'].quantile(0.25)
    Q3 = MSFT[f'{column_name}'].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = MSFT[(MSFT[f'{column_name}'] < lower_bound) | (MSFT[f'{column_name}'] > upper_bound)]

    print(f'{column_name}')
    print("Number of outliers:", len(outliers))
    print(outliers)

    plt.show()

"""**NAIVE-BAYES**"""

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report
MSFT_standardized

features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days', 'Daily Return', 'Close1', 'Close_2', 'Close_3']
target = 'Cluster'

X = MSFT_standardized[features]
y2 = Dataset[target]
X_train, X_test, y2_train, y2_test = train_test_split(X, y2, test_size=0.2, random_state=42)

naive_bayes_classifier = GaussianNB()

naive_bayes_classifier.fit(X_train, y2_train)

predictions = naive_bayes_classifier.predict(X_test)

accuracy = accuracy_score(y2_test, predictions)
print(f"Accuracy: {accuracy:.2f}")

print("Classification Report:")
print(classification_report(y2_test, predictions))

"""**LINEAR REGRESSION**"""

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

"""**SVR**"""

from sklearn.svm import SVC
features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days', 'Daily Return', 'Close1', 'Close_2', 'Close_3']
target = 'Next_Day_Closing_Price'

X = MSFT_standardized[features]
y = np.where(MSFT['Next_Day_Closing_Price'].shift(-1) > MSFT['Next_Day_Closing_Price'], 1, 0)
X_train = X.iloc[:train_size]
X_test = X.iloc[train_size:]

y_train = y[:train_size]
y_test = y[train_size:]
regressor = SVC(kernel='linear')
regressor.fit(X_train,y_train)

print(accuracy_score(regressor.predict(X_test),y_test))

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

"""ARIMA"""

df = MSFT_standardized.asfreq('D')

cols=['Close']
df1=df.loc[:,cols]
df1

df1.plot()

fig, axes = plt.subplots(3, 2, figsize=(19, 11))
axes[0, 0].plot(df1)
axes[0, 0].set_title('Original Series')
plot_acf(df1, ax=axes[0, 1])
# 1st Differencing
axes[1, 0].plot(df1.diff())
axes[1, 0].set_title('1st Order Differencing')
plot_acf(df1.diff().dropna(), ax=axes[1, 1])

# 2nd Differencing
axes[2, 0].plot(df1.diff().diff()); axes[2, 0].set_title('2nd Order Differencing')
plot_acf(df1.diff().diff().dropna(), ax=axes[2, 1])

plt.show()

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
data_diff = df1['Close'].diff().dropna()
plot_acf(data_diff)
plot_pacf(data_diff)
plt.show()

p, d, q = 0, 1, 1

model = ARIMA(df1['Close'], order=(p, d, q))
result = model.fit()
print(result.summary())

plt.figure(figsize=(30, 9))
X=result.predict()
plt.plot(X,label='predicted')
plt.plot(df1,label='original')

plt.show()

forecast_steps = 1000
forecast = result.get_forecast(steps=forecast_steps)
forecast_index = pd.date_range(start=df1.index[-1], periods=forecast_steps+1, freq='B')[1:]
forecast_values = forecast.predicted_mean

# Plot the original data and the forecast
plt.plot(df1['Close'], label='Original Data')
plt.plot(forecast_index, forecast_values, color='red', label='Forecast')
plt.legend()
plt.show()

"""ARTIFICIAL NEURAL NETWORK"""

features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days', 'Daily Return', 'Close1', 'Close_2', 'Close_3']
target = 'Next_Day_Closing_Price'

X = MSFT_standardized[features]
y = MSFT[target]

X_train = X.iloc[:train_size]
X_test = X.iloc[train_size:]

y_train = y[:train_size]
y_test = y[train_size:]

model = Sequential()
model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1, activation='linear'))

model.compile(loss='mean_squared_error', optimizer='adam')

model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=1)

loss = model.evaluate(X_train, y_train)
print(f'Mean Squared Error on Train Set: {loss}')

loss = model.evaluate(X_test, y_test)
print(f'Mean Squared Error on Test Set: {loss}')

predictions = model.predict(X_test)

from sklearn.metrics import mean_squared_error, mean_absolute_error
mse = mean_squared_error(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)
acc = r2_score(y_test ,predictions)
print(f'Mean Squared Error: {mse}')
print(f'Mean Absolute Error: {mae}')
print(f'R2_score: {acc}')

plt.scatter(y_test, predictions, color='blue', label='Predicted Values')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', linewidth=2, label='Ideal Line')

plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs. Predicted Values')
plt.legend()
plt.show()

plt.plot(y_test.index, y_test, label='Actual')
plt.plot(y_test.index, predictions, label='Predicted')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Time Series: Actual vs. Predicted')
plt.legend()
plt.show()

"""EXPONENTIAL SMOOTHING"""

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

"""RANDOM FOREST REGRESSOR"""

X = smoothed_data[features]
y = MSFT[target]

X_train = X.iloc[:train_size]
X_test = X.iloc[train_size:]

y_train = y[:train_size]
y_test = y[train_size:]

from sklearn.ensemble import RandomForestRegressor

regressor = RandomForestRegressor(n_estimators = 100, random_state = 0 , max_depth = 5)
regressor.fit(X_train, y_train)

train_predict=regressor.predict(X_train)
test_predict=regressor.predict(X_test)

train_predict = train_predict.reshape(-1,1)
test_predict = test_predict.reshape(-1,1)

import math

print("Train data RMSE: ", math.sqrt(mean_squared_error(y_train,train_predict)))
print("Train data MSE: ", mean_squared_error(y_train,train_predict))
print("Test data MAE: ", mean_absolute_error(y_train,train_predict))
print("-------------------------------------------------------------------------------------")
print("Test data RMSE: ", math.sqrt(mean_squared_error(y_test,test_predict)))
print("Test data MSE: ", mean_squared_error(y_test,test_predict))
print("Test data MAE: ", mean_absolute_error(y_test,test_predict))

print("Train data R2 score:", r2_score(y_train, train_predict))
print("Test data R2 score:", r2_score(y_test, test_predict))

plt.plot(y_test.index, y_test, label='Actual')
plt.plot(y_test.index, test_predict, label='Predicted')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Time Series: Actual vs. Predicted')
plt.legend()
plt.show()

"""DECISION TREE"""

from sklearn.model_selection import train_test_split, GridSearchCV
# Build the Decision Tree model
dt_model = DecisionTreeRegressor()

# Define the hyperparameters to search
param_grid = {
    'max_depth': [None, 5, 10, 15],
    'min_samples_split': [20, 50, 100],
    'min_samples_leaf': [5, 10, 15],
    'max_features': [ 'sqrt', 'log2']
}

# Create the GridSearchCV object
grid_search = GridSearchCV(estimator=dt_model, param_grid=param_grid, cv=3)
grid_result = grid_search.fit(X_train, y_train)

# Print the best parameters and corresponding mean squared error
print(f'Best Hyperparameters: {grid_result.best_params_}')

# Use the best model for predictions
best_dt_model = grid_result.best_estimator_
predictions = best_dt_model.predict(X_test)

mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error on Test Set: {mse}')

feature_importance = best_dt_model.feature_importances_
feature_names = MSFT_standardized.columns

# Print or plot feature importance
for feature, importance in zip(feature_names, feature_importance):
    print(f'{feature}: {importance}')

plt.scatter(y_test, predictions)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', linewidth=2, label='Ideal Line')
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs. Predicted Values (Decision Tree)')
plt.show()

plt.plot(y_test.index, y_test, label='Actual')
plt.plot(y_test.index, predictions, label='Predicted')
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Time Series: Actual vs. Predicted')
plt.legend()
plt.show()