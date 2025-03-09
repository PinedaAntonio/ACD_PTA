import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Cargar el dataset
df = pd.read_csv("used_car_dataset.csv")

# Limpieza de la columna AskPrice
df["AskPrice"] = df["AskPrice"].str.replace("₹", "", regex=False)  # Eliminar símbolo ₹
df["AskPrice"] = df["AskPrice"].str.replace(",", "", regex=False)  # Eliminar comas
df["AskPrice"] = pd.to_numeric(df["AskPrice"], errors="coerce")  # Convertir a numérico

# Limpieza de la columna kmDriven
df["kmDriven"] = df["kmDriven"].str.replace(
    " km", "", regex=False
)  # Eliminar texto ' km'
df["kmDriven"] = df["kmDriven"].str.replace(",", "", regex=False)  # Eliminar comas
df["kmDriven"] = pd.to_numeric(df["kmDriven"], errors="coerce")  # Convertir a numérico

# Eliminar las columnas que no queremos analizar: "AdditionInfo" y "PostedDate"
df = df.drop(columns=["AdditionInfo", "PostedDate"])

## Eliminar filas con valores nulos después de la conversión
df = df.dropna(subset=["AskPrice", "kmDriven"])

# Dividir en entrenamiento y test (80% entrenamiento, 20% test)
train_size = int(len(df) * 0.8)
df_train = df.iloc[:train_size]
df_test = df.iloc[train_size:]

# Variables predictoras y objetivo
X_train = df_train[["kmDriven"]]
y_train = df_train["AskPrice"]
X_test = df_test[["kmDriven"]]
y_test = df_test["AskPrice"]

# Modelo de regresión lineal simple
modelo_lineal = LinearRegression()
modelo_lineal.fit(X_train, y_train)

# Predicción
y_pred = modelo_lineal.predict(X_test)

# Evaluación del error
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
print(f'RMSE: {rmse:.2f}')

# Gráfica de predicción vs datos reales
plt.figure(figsize=(10, 5))
plt.scatter(X_test, y_test, color='blue', label='Datos reales', alpha=0.5)
plt.plot(X_test, y_pred, color='red', linestyle='--', label='Predicción')
plt.title('Regresión Lineal Simple: kmDriven vs AskPrice')
plt.xlabel('Kilometraje recorrido (kmDriven)')
plt.ylabel('Precio de venta (AskPrice)')
plt.grid(True)
plt.legend()
plt.show()
