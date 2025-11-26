import pandas as pd

df = pd.read_csv("OPEN_MEDIC_2024.CSV", encoding="latin2", sep=";")
print(df.head())
