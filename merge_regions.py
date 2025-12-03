from io import TextIOWrapper
from shapely.geometry import shape, mapping
import sys
import json


def main(input: TextIOWrapper, output: TextIOWrapper):
    geojson_raw = input.read()
    geojson = json.loads(geojson_raw)
    features = geojson["features"]

    (
        idf,
        centre,
        bourgogne,
        normandie,
        haut_de_france,
        grand_est,
        pdl,
        bretagne,
        nouvelle_aquitaine,
        guadeloupe,
        martinique,
        guyane,
        reunion,
        mayotte,
        occitanie,
        auvergne,
        paca,
        corse,
    ) = features

    paca_geom = shape(paca["geometry"])
    corse_geom = shape(corse["geometry"])
    paca_corse_geom = paca_geom.union(corse_geom)

    paca_corse = {
        "type": "Feature",
        "properties": {**paca["properties"], "nom": "PACA + Corse"},
        "geometry": mapping(paca_corse_geom),
    }

    outre_mer_geoms = [
        shape(guadeloupe["geometry"]),
        shape(martinique["geometry"]),
        shape(guyane["geometry"]),
        shape(reunion["geometry"]),
        shape(mayotte["geometry"]),
    ]

    outre_mer_geom = outre_mer_geoms[0]
    for geom in outre_mer_geoms[1:]:
        outre_mer_geom = outre_mer_geom.union(geom)

    outre_mer = {
        "type": "Feature",
        "properties": {"code": 5, "nom": "Outre-Mer"},
        "geometry": mapping(outre_mer_geom),
    }

    new_features = [
        idf,
        centre,
        bourgogne,
        normandie,
        haut_de_france,
        grand_est,
        pdl,
        bretagne,
        nouvelle_aquitaine,
        occitanie,
        auvergne,
        paca_corse,
        outre_mer,
    ]

    new_geojson = {"type": "FeatureCollection", "features": new_features}
    output.write(json.dumps(new_geojson))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("arg error", file=sys.stderr)
        exit(1)
    with (
        open(sys.argv[1], "r") as input_json,
        open(sys.argv[2], "w+") as output_json,
    ):
        main(input_json, output_json)
