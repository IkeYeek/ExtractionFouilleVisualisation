import pandas as pd

df = pd.read_excel("TCRD_021.xlsx", sheet_name="REG", header=3)
df.columns = ["region_id", "region_name", "total_population", "women_percent", "men_percent", "0yo_to_24yo_percent", "25yo_to_59yo_percent", "60yo_and_more_percent", "75yo_and_more_percent"]
df = df.dropna(axis=0)
df = df[~df["region_id"].isin(["M", "F"])] # drop metropolitan total and France total

total_people_per_region = {}
total_people_per_age_per_region = {}
old_people_percent_per_region = {}

for row in df.iloc:
    region_id = int(row["region_id"])
    total_population = int(row["total_population"])
    sixty_yo_and_more_percent = float(row["60yo_and_more_percent"])
    total_people_per_region[region_id] = total_population
    old_people_percent_per_region[region_id] = sixty_yo_and_more_percent
    total_people_per_age_per_region[region_id] = {
        0:  (float(row["0yo_to_24yo_percent"]) / 100.) * total_population,
        20:  (float(row["25yo_to_59yo_percent"]) / 100.) * total_population,
        60:  (float(row["60yo_and_more_percent"]) / 100.) * total_population,
    }

# compute over seas ..
total_over_seas_population = sum(total_people_per_region[i] for i in range(10) if i in total_people_per_region)
total_over_seas_population_by_age_group = {
    0: 0,
    20: 0,
    60: 0
}
for i in range(10):
    if i not in old_people_percent_per_region:
        continue # skip
    total_over_seas_population_by_age_group[0] += total_people_per_region[i] * (total_people_per_age_per_region[i][0]/100.)
    total_over_seas_population_by_age_group[20] += total_people_per_region[i] * (total_people_per_age_per_region[i][20]/100.)
    total_over_seas_population_by_age_group[60] += total_people_per_region[i] * (total_people_per_age_per_region[i][60]/100.)

total_people_per_region[5] = total_over_seas_population
total_people_per_age_per_region[5] = total_over_seas_population_by_age_group
old_people_percent_per_region[5] = (total_over_seas_population_by_age_group[60] / total_people_per_region[5]) * 100.
