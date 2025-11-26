import pandas as pd
import matplotlib.pyplot as plt

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

def fix_french_float(f: str) -> str:
    f = f.replace(".", "")
    last_comma_idx = f.rfind(",")
    if last_comma_idx != -1:
        f = f[:last_comma_idx] + "." + f[last_comma_idx+1:]
    return f

df = pd.read_csv("OPEN_MEDIC_2024.CSV", encoding="latin2", sep=";")
# # print(df.columns) # ['ATC1', 'l_ATC1', 'ATC2', 'L_ATC2', 'ATC3', 'L_ATC3', 'ATC4', 'L_ATC4', 'ATC5', 'L_ATC5', 'CIP13', 'l_cip13', 'TOP_GEN', 'GEN_NUM', 'age', 'sexe', 'BEN_REG', 'PSP_SPE', 'BOITES', 'REM', 'BSE']

df["REM"] = df["REM"].apply(lambda s: float(fix_french_float(s))) # fix french floats ... (1.234,56) ...
region_map = {5:'''Outre-mer ''',11:'Ile-de-France', 24:'Centre-Val de Loire', 27:'Bourgogne-Franche-Comté',
    28:'Normandie',32:'Nord-Pas-de-Calais-Picardie', 44:'Alsace-Champagne-Ardenne-Lorraine',
    52:'Pays de la Loire', 53:'Bretagne',75:'Aquitaine-Limousin-Poitou-Charentes',
    76:'Languedoc-Roussillon-Midi-Pyrénées',84:'Auvergne-Rhône-Alpes',93:'''Provence-Alpes-Côte d'Azur et Corse''',
    0:'Inconnue',9:'Inconnue',99:'Inconnue'
} # <- Unknown regions
age_map = {0:'0 to 19 years',20:'20 to 59 years', 60:'Over 60 years', 99:'Age Inconnu'}

df = df[~df["BEN_REG"].isin([0, 9, 99])] # drop Unknown regions

# print(df.groupby(["BEN_REG", "age"])["REM"].count().groupby(level=0).idxmax().map(lambda x: x[1])) # groupe avec le + de remboursements


# https://www.insee.fr/fr/statistiques/2012713#tableau-TCRD_004_tab1_regions2016
region_to_pop_2025 = {
    5: 2_253_657, # 68605616 - 66351959
    11: 12_450_849,
    24: 2_581_479,
    27: 2_793_080,
    28: 3_341_312,
    32: 5_973_933, # Hauts-de-France
    44: 5_544_051, # Grand Est
    52: 3_936_719,
    53: 3_475_895,
    75: 6_191_209,
    76: 6_201_587,
    84: 8_260_096,
    93: 5_241_587 + 360_162 # Provence-Alpes-Côte d'Azur + Corse
}

def normalize_by_pop(v: pd.Series):
    region, reimbursed = v.name, v.iloc[0]

    if region in region_to_pop_2025:
        reimbursed /= region_to_pop_2025[region]
    else:
        print(f"warn: {region} not in region_to_pop_2025")

    return pd.Series(data=[reimbursed], index=["REM"])

# Plot montant remboursé euros par habitant VS region
# reg_to_reimbursement: pd.Series = df.groupby(by="BEN_REG")["REM"].sum()
# reg_to_reimbursement_normalized = reg_to_reimbursement.to_frame().apply(normalize_by_pop, axis=1) # normalize py pop
# reg_to_reimbursement_normalized.index = reg_to_reimbursement_normalized.index.map(region_map)
# reg_to_reimbursement_normalized.sort_values(by="REM", ascending=True).plot.barh(ylabel="Montant remboursé euros par habitant", legend=False)
# plt.show()

# Plot montant remboursé euros par (habitant: chaque tranche d'age stackée) VS region (stacked)
reg_to_reimbursement: pd.Series = df.groupby(by=["BEN_REG", "age"])["REM"].sum()
reg_to_reimbursement_normalized = reg_to_reimbursement.to_frame().apply(lambda s: s.iloc[0] / region_to_pop_2025[s.name[0]], axis=1).reset_index(name="reimbursed_per_person") # normalize py pop (douteux puisque nombre(vieux) != nombre(jeunes) dans chaque région mais bon..)
pivot = reg_to_reimbursement_normalized.pivot(index="BEN_REG", columns="age", values="reimbursed_per_person")
pivot = pivot[[0, 20, 60]]
sorted_pivot = pivot.iloc[pivot.sum(axis=1).reset_index()[0].sort_values(ascending=True).index] # ugly sort
sorted_pivot.index = sorted_pivot.index.map(region_map) # map INSEE region code to region name
sorted_pivot.columns = sorted_pivot.columns.map(age_map) # map to age groups names
sorted_pivot.plot.barh(stacked=True, ylabel="Montant remboursé euros par habitant", xlabel="", title="Montant remboursé euros par habitant(et tranche d'age) par region")
plt.subplots_adjust(left=0.3)
plt.show()
