import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import mean_squared_error

# Cargar el dataset
df = pd.read_csv("used_car_dataset.csv")

# Limpieza de la columna AskPrice
df["AskPrice"] = df["AskPrice"].str.replace("\u20b9", "", regex=False)  # Eliminar símbolo ₹
df["AskPrice"] = df["AskPrice"].str.replace(",", "", regex=False)  # Eliminar comas
df["AskPrice"] = pd.to_numeric(df["AskPrice"], errors="coerce")  # Convertir a numérico

# Limpieza de la columna kmDriven
df["kmDriven"] = df["kmDriven"].str.replace(" km", "", regex=False)  # Eliminar texto ' km'
df["kmDriven"] = df["kmDriven"].str.replace(",", "", regex=False)  # Eliminar comas
df["kmDriven"] = pd.to_numeric(df["kmDriven"], errors="coerce")  # Convertir a numérico

# Aplicar Ordinal Encoding a Brand y model
ordinal_encoder = OrdinalEncoder()
df[["Brand", "model"]] = ordinal_encoder.fit_transform(df[["Brand", "model"]])

# Aplicar One Hot Encoding a Transmission, Owner y FuelType
df = pd.get_dummies(df, columns=["Transmission", "Owner", "FuelType"], drop_first=True)

# Eliminar filas con valores nulos después de la conversión
df = df.dropna()

# Dividir en entrenamiento y test (80% entrenamiento, 20% test)
train_size = int(len(df) * 0.8)
df_train = df.iloc[:train_size]
df_test = df.iloc[train_size:]

# Seleccionar todas las variables predictoras
columnas_predictoras = [col for col in df.columns if col != "AskPrice"]

X_train = df_train[columnas_predictoras]
y_train = df_train["AskPrice"]
X_test = df_test[columnas_predictoras]
y_test = df_test["AskPrice"]

# Modelo de Regresión Lasso
modelo_lasso = Lasso(alpha=1.0)
modelo_lasso.fit(X_train, y_train)

# Predicción
y_pred = modelo_lasso.predict(X_test)

# Evaluación del error
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
print(f'RMSE con Regresión Lasso: {rmse:.2f}')

# Identificar variables eliminadas por Lasso
coeficientes = pd.Series(modelo_lasso.coef_, index=columnas_predictoras)
variables_seleccionadas = coeficientes[coeficientes != 0].index.tolist()
variables_eliminadas = coeficientes[coeficientes == 0].index.tolist()
print("\nVariables seleccionadas por Lasso:")
print(variables_seleccionadas)
print("\nVariables eliminadas por Lasso:")
print(variables_eliminadas)

# Gráfica de predicción vs datos reales
plt.figure(figsize=(10, 5))
plt.scatter(y_test, y_pred, color='blue', label='Predicción vs Real', alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.title('Regresión Lasso: Predicción vs Valor Real')
plt.xlabel('Precio Real')
plt.ylabel('Predicción')
plt.grid(True)
plt.legend()
plt.show()