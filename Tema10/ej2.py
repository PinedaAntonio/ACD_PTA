import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Lasso
from sklearn.preprocessing import OrdinalEncoder
from sklearn.metrics import mean_squared_error

# Cargar el dataset
df = pd.read_csv("used_car_dataset.csv")

# Limpieza de la columna AskPrice
df["AskPrice"] = df["AskPrice"].str.replace(
    "\u20b9", "", regex=False
)  # Eliminar símbolo ₹
df["AskPrice"] = df["AskPrice"].str.replace(",", "", regex=False)  # Eliminar comas
df["AskPrice"] = pd.to_numeric(df["AskPrice"], errors="coerce")  # Convertir a numérico

# Limpieza de la columna kmDriven
df["kmDriven"] = df["kmDriven"].str.replace(
    " km", "", regex=False
)  # Eliminar texto ' km'
df["kmDriven"] = df["kmDriven"].str.replace(",", "", regex=False)  # Eliminar comas
df["kmDriven"] = pd.to_numeric(df["kmDriven"], errors="coerce")  # Convertir a numérico

# Aplicar One-Hot Encoding a Transmission (solo una variable categórica)
df = pd.get_dummies(df, columns=["Transmission"], drop_first=True)

# Eliminar filas con valores nulos después de la conversión
df = df.dropna()

# Seleccionar solo las variables predictoras requeridas
columnas_predictoras = ["Age", "kmDriven"] + [
    col for col in df.columns if "Transmission" in col
]

# Dividir en entrenamiento y test (80% entrenamiento, 20% test)
train_size = int(len(df) * 0.8)
df_train = df.iloc[:train_size]
df_test = df.iloc[train_size:]

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
rmse = mse**0.5
print(f"RMSE con Regresión Lasso: {rmse:.2f}")

# Identificar variables eliminadas por Lasso
coeficientes = pd.Series(modelo_lasso.coef_, index=columnas_predictoras)
variables_seleccionadas = coeficientes[coeficientes != 0].index.tolist()
variables_eliminadas = coeficientes[coeficientes == 0].index.tolist()
print("\nVariables seleccionadas por Lasso:")
print(variables_seleccionadas)
print("\nVariables eliminadas por Lasso:")
print(variables_eliminadas)

# Seleccionar 30 índices equidistantes dentro del conjunto de prueba
indices = np.linspace(0, len(df_test) - 1, 30, dtype=int)

# Extraer los valores correspondientes
X_test_sampled = X_test.iloc[indices]
y_test_sampled = y_test.iloc[indices]
y_pred_sampled = y_pred[indices]

# Obtener los índices originales del dataset para estos coches
dataset_indices = df_test.iloc[indices].index  # Índices reales del dataset

# Gráfica de predicción vs datos reales con índices reales
plt.figure(figsize=(12, 6))
plt.plot(
    dataset_indices,
    y_test_sampled,
    color="blue",
    label="Datos reales",
    linestyle="--",
    marker="o",
    alpha=0.6,
)
plt.plot(
    dataset_indices,
    y_pred_sampled,
    color="red",
    linestyle="--",
    label="Predicción",
    marker="o",
)
plt.title(
    "Regresión Lasso: Comparación entre precios reales y predichos (Muestra de 30 coches)"
)
plt.xlabel("Índice del coche en el dataset")
plt.ylabel("Precio de venta (AskPrice)")
plt.xticks(dataset_indices, rotation=45)  # Mostrar los índices reales
plt.grid(True, linestyle="--", alpha=0.7)
plt.legend()
plt.show()
