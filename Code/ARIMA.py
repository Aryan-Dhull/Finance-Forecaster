df = MSFT_standardized.asfreq('D')
cols=['Close']
df1=df.loc[:,cols]
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
