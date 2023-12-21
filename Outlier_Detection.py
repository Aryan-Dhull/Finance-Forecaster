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
