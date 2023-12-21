from sklearn.preprocessing import StandardScaler

columns_to_standardize = ['Open', 'High', 'Low', 'Close', 'Volume','Daily Return','Adj Close', 'MA for 10 days','MA for 20 days','MA for 50 days', 'Close1', 'Close_2', 'Close_3']
MSFT_standardized=MSFT[columns_to_standardize]
y = MSFT['Next_Day_Closing_Price']

scaler = StandardScaler()
MSFT_standardized[columns_to_standardize] = scaler.fit_transform(MSFT_standardized[columns_to_standardize])

columns_for_kmeans =['Open', 'High', 'Low', 'Close','Adj Close', 'MA for 10 days','MA for 20 days','MA for 50 days', 'Close1', 'Close_2', 'Close_3']
Dataset=MSFT[columns_for_kmeans]
scaler = StandardScaler()
Dataset[columns_for_kmeans] = scaler.fit_transform(Dataset[columns_for_kmeans])
