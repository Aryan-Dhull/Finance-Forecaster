MSFT['Close1'] = MSFT['Close']
MSFT['Close_2'] = MSFT['Close'].shift(1)
MSFT['Close_3'] = MSFT['Close'].shift(2)
MSFT['Next_Day_Closing_Price'] = MSFT['Close'].shift(-1)
MSFT = MSFT.drop(columns = ['company_name'])
MSFT = MSFT.dropna()

correlation_matrix = MSFT.corr()
plt.figure(figsize=(10, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Correlation Matrix')
plt.show()
