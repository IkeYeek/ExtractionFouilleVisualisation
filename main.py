import pandas as pd

# variables = pd.read_excel("2024_descriptif-variables_open-medic.xls")
# print(variables)
col_to_label = {
    "ATC1": "Goupe Principal Anatomique",
    "ATC2": "Sous-Groupe Thérapeutique",
    "ATC3": "Sous-Groupe Pharmacologique",
    "ATC4": "Sous-Groupe Chimique",
    "ATC5": "Sous-Groupe Substance Chimique",
    "CIP13": "Code Identification Spécialité Pharmaceutqiue",
    "TOP_GEN": "Top Générique",
    "GEN_NUM": "Groupe Générique",
    "age": "Age",
    "sexe": "Sexe",
    "Bénéficiaire": "Bénéficiaire",
    "BEN_REG": "Région de Résidence du Bénéficiaire",
    "PSP_SPE": "Prescripteur",
    "REM": "Montant Remboursé",
    "BSE": "Base de Remboursement",
    "BOITES": "Nombre de boîtes délivrées",
    "NBC": "Nombre de consommants"
}



df = pd.read_csv("OPEN_MEDIC_2024.CSV", encoding="latin2", sep=";")
print(df.columns) # ['ATC1', 'l_ATC1', 'ATC2', 'L_ATC2', 'ATC3', 'L_ATC3', 'ATC4', 'L_ATC4', 'ATC5', 'L_ATC5', 'CIP13', 'l_cip13', 'TOP_GEN', 'GEN_NUM', 'age', 'sexe', 'BEN_REG', 'PSP_SPE', 'BOITES', 'REM', 'BSE']
