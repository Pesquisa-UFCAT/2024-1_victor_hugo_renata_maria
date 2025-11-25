import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor  
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

#1. Exemplo de dados
dates = pd.date_range(start='2020-01-01', periods=100)
values = np.linspace(0, 10, 100) + np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.1, 100)
df = pd.DataFrame({'date': dates, 'value': values}).set_index('date')

#2. Eng de Features
def create_lags(data, n_lags):
    df_lags = data.copy()
    for lag in range(1, n_lags + 1):
        df_lags[f'lag_{lag}'] = df_lags['value'].shift(lag) 
    return df_lags.dropna()

df_prepared = create_lags(df, n_lags=3)

# Separar X e y
X = df_prepared.drop('value', axis=1)
y = df_prepared['value']

#4. Divisão treino
train_size = int(len(X) * 0.8)
X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

#5. Treinamento do modelo
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

#6. Previsões
predicoes = rf.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, predicoes))

print(f"RMSE: {rmse:.4f}")

#7. Visualização dos resultados
plt.figure(figsize=(12, 6))
plt.plot(y_train.index, y_train, label='Treino')
plt.plot(y_test.index, y_test, label='Teste')
plt.plot(y_test.index, predicoes, label='Previsões', linestyle='--')
plt.legend()
plt.title('Previsões de Série Temporal com Random Forest')
plt.show()
