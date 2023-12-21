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
