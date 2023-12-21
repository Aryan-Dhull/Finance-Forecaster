X = smoothed_data[features]
y = MSFT[target]
X_train = X.iloc[:train_size]
X_test = X.iloc[train_size:]
y_train = y[:train_size]
y_test = y[train_size:]

from sklearn.ensemble import RandomForestRegressor
import math

regressor = RandomForestRegressor(n_estimators = 100, random_state = 0 , max_depth = 5)
regressor.fit(X_train, y_train)

train_predict=regressor.predict(X_train)
test_predict=regressor.predict(X_test)

train_predict = train_predict.reshape(-1,1)
test_predict = test_predict.reshape(-1,1)

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
