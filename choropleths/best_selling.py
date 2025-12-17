import json
import numpy as np
import plotly.express as px
import pandas as pd


def fix_french_float(f: str) -> str:
    f = f.replace(".", "")
    last_comma_idx = f.rfind(",")
    if last_comma_idx != -1:
        f = f[:last_comma_idx] + "." + f[last_comma_idx + 1 :]
    return f


with open("./dataset/regions.json") as geojson_file:
    geojson = json.loads(geojson_file.read())

    df = pd.read_csv("./dataset/OPEN_MEDIC_2024.csv", sep=";", encoding="latin1")
    df["REM"] = df["REM"].apply(lambda s: float(fix_french_float(s)))
    df = df[["L_ATC2", "BEN_REG", "REM"]].groupby(by=["BEN_REG", "L_ATC2"])["REM"].sum()
    data = {}
    for region in geojson["features"]:
        properties = region["properties"]
        if (properties["code"],) not in df:
            continue
        data[properties["code"]] = {
            **properties,
            "best_seller": df[(properties["code"],)].idxmax(),
        }

    data = pd.DataFrame.from_dict(data, orient="index")
    fig = px.choropleth(
        data,
        geojson=geojson,
        color="best_seller",
        locations="join_key",
        featureidkey="properties.join_key",
        projection="equirectangular",
        center={"lat": 46, "lon": 2},
        color_discrete_sequence=px.colors.sequential.Plasma,
    )
    fig.update_geos(visible=False, projection_scale=15)
    fig.show()
