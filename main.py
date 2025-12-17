import pandas as pd
import matplotlib.pyplot as plt

pd_all_rows_ctx = lambda: pd.option_context('display.max_rows', None)

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
    "BEN_REG": "Région de Résidence du Bénéficiaire",
    "PSP_SPE": "Prescripteur",
    "REM": "Montant Remboursé",
    "BSE": "Base de Remboursement",
    "BOITES": "Nombre de boîtes délivrées",
    "NBC": "Nombre de consommants",
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


from population_stats import total_people_per_region as region_to_pop_2025
from population_stats import old_people_percent_per_region, total_people_per_age_per_region

def normalize_by_pop(v: pd.Series):
    region_code: int = v.name
    reimbursed: float = v.iloc[0]

    if region_code in region_to_pop_2025:
        reimbursed /= region_to_pop_2025[region_code]
    else:
        print(f"warn: {region_code} not in region_to_pop_2025")

    return pd.Series(data=[reimbursed], index=["REM"])

# Plot montant remboursé euros par habitant VS region

# reg_to_reimbursement: pd.Series = df.groupby(by="BEN_REG")["REM"].sum()
# reg_to_reimbursement_normalized = reg_to_reimbursement.to_frame().apply(normalize_by_pop, axis=1) # normalize py pop
# reg_to_reimbursement_normalized["old_people_percent"] = reg_to_reimbursement_normalized.index.map(old_people_percent_per_region) * 10 # TODO: fix this scale ..
# reg_to_reimbursement_normalized.index = reg_to_reimbursement_normalized.index.map(region_map)
# reg_to_reimbursement_normalized_sorted = reg_to_reimbursement_normalized.sort_values(by="REM", ascending=True)
# reg_to_reimbursement_normalized_sorted.plot.barh(ylabel="Montant remboursé euros par habitant", legend=False, title="Montant remboursé euros par habitant par région INSEE")


# Plot montant remboursé euros par (habitant: chaque tranche d'age stackée) VS region (stacked)

reg_to_reimbursement: pd.Series = df.groupby(by=["BEN_REG", "age"])["REM"].sum()
def f(r: pd.Series):
    region_id: int = r.name[0]
    age_group_id: int = r.name[1]
    if (region_id not in total_people_per_age_per_region) or (age_group_id not in total_people_per_age_per_region[region_id]):
        return None
    return r.iloc[0] / total_people_per_age_per_region[region_id][age_group_id]

# reg_to_reimbursement_normalized = reg_to_reimbursement.to_frame().apply(lambda s: s.iloc[0] / region_to_pop_2025[s.name[0]], axis=1).reset_index(name="reimbursed_per_person") # normalize py pop (douteux puisque nombre(vieux) != nombre(jeunes) dans chaque région mais bon..)
reg_to_reimbursement_normalized = reg_to_reimbursement.to_frame().apply(f, axis=1).reset_index(name="reimbursed_per_person") # normalize py pop (douteux puisque nombre(vieux) != nombre(jeunes) dans chaque région mais bon..)
pivot = reg_to_reimbursement_normalized.pivot(index="BEN_REG", columns="age", values="reimbursed_per_person")
pivot = pivot[[0, 20, 60]]
sorted_pivot = pivot.iloc[pivot.sum(axis=1).reset_index()[0].sort_values(ascending=True).index] # ugly sort
sorted_pivot.index = sorted_pivot.index.map(region_map) # map INSEE region code to region name
sorted_pivot.columns = sorted_pivot.columns.map(age_map) # map to age groups names
sorted_pivot.plot.barh(ylabel="Montant remboursé euros par habitant", xlabel="", title="Montant remboursé euros par habitant(et tranche d'age) par region")


# The french's preffered medication

# df.groupby(by=["L_ATC2"])["REM"].sum().sort_values(ascending=True).iloc[-10:].plot.barh(ylabel="Sous-Groupe Thérapeutique", xlabel="Montant total remboursé euros", title="Les médicaments coutant le plus cher à la sécu")

# df.groupby(by=["L_ATC5"])["BOITES"].sum().sort_values(ascending=True).iloc[-20:].plot.barh(ylabel="Sous-Groupe Substance Chimique", xlabel="Nombre de boites remboursées", title="Les catégories de médicaments préférées des français", logx=True)

plt.subplots_adjust(left=0.3) # leave space on the left ...
plt.show()
