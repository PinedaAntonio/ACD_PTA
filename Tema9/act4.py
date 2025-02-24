import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OrdinalEncoder


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


# Definir las columnas categóricas restantes
cat_cols = ["Brand", "model", "Transmission", "Owner", "FuelType"]


# Asegurarse de que estas columnas sean de tipo string
for col in cat_cols:
    df[col] = df[col].astype(str)


# Aplicar Ordinal Encoding a las columnas categóricas
encoder = OrdinalEncoder()
df[cat_cols] = encoder.fit_transform(df[cat_cols])


# Mostrar algunas filas del dataset tras la codificación ordinal
print("Primeras filas del dataset tras Ordinal Encoding:")
print(df.head())


# Calcular la matriz de correlación
corr_matrix = df.corr()


# Extraer las correlaciones de las variables codificadas con la variable objetivo AskPrice
corr_with_target = corr_matrix["AskPrice"].drop("AskPrice").sort_values(ascending=False)


print("\nCorrelaciones de las variables codificadas con 'AskPrice':")
print(corr_with_target)


# ---- 4. Identificación de valores nulos ----
print("\nValores nulos por columna:")
print(df[["Year", "kmDriven", "Transmission", "AskPrice"]].isnull().sum())


# ---- 5. Identificación de valores erróneos ----
# Comprobamos valores negativos o inválidos en las variables numéricas
print(
    "\nValores negativos en Year:", (df["Year"] < 1900).sum()
)  # Un año antes de 1900 no es válido
print("Valores negativos en kmDriven:", (df["kmDriven"] < 0).sum())
print("Valores negativos en AskPrice:", (df["AskPrice"] < 0).sum())


# ---- 6. Identificación de outliers ----
def detectar_outliers_zscore(data, columna, threshold=3):
    """Detecta outliers usando el método del Z-score"""
    mean = np.mean(data[columna])
    std = np.std(data[columna])
    z_scores = (data[columna] - mean) / std
    return data[abs(z_scores) > threshold]


print("\nOutliers detectados en Year:")
print(detectar_outliers_zscore(df, "Year"))


print("\nOutliers detectados en kmDriven:")
print(detectar_outliers_zscore(df, "kmDriven"))


print("\nOutliers detectados en AskPrice:")
print(detectar_outliers_zscore(df, "AskPrice"))


# ---- 7. Tratamiento de valores nulos ----
df[["Year", "kmDriven", "Transmission", "AskPrice"]] = df[
    ["Year", "kmDriven", "Transmission", "AskPrice"]
].fillna(df.median())


# ---- 8. Tratamiento de valores erróneos ----
df = df[df["Year"] >= 1900]  # Eliminar registros con años no válidos
df = df[df["kmDriven"] >= 0]
df = df[df["AskPrice"] >= 0]


# ---- 9. Tratamiento de outliers ----
# Eliminamos los outliers basados en Z-score
for col in ["Year", "kmDriven", "AskPrice"]:
    df = df[(np.abs((df[col] - df[col].mean()) / df[col].std()) < 3)]


# Mostrar las primeras filas del dataset procesado
print("\nDataset después del preprocesamiento:")
print(df.head())
