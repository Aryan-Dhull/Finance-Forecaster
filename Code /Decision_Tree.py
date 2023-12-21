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
