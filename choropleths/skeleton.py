import json
import numpy as np
import plotly.express as px
import pandas as pd

with open("./dataset/regions.json") as geojson_file:
    geojson = json.loads(geojson_file.read())
    data = {
        i: [
            geojson["features"][i]["properties"]["code"],
            geojson["features"][i]["properties"]["nom"],
        ]
        for i in range(len(geojson["features"]))
    }
    columns_names = np.array(["code", "name"])
    df = pd.DataFrame.from_dict(data, orient="index", columns=columns_names)
    fig = px.choropleth(
        df,
        geojson=geojson,
        color="name",
        locations="code",
        featureidkey="properties.code",
        projection="equirectangular",
        center={"lat": 46, "lon": 2},
        color_discrete_sequence=px.colors.sequential.Plasma,
    )
    fig.update_geos(visible=False, projection_scale=15)
    fig.show()
