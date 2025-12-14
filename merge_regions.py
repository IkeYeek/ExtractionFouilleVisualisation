from io import TextIOWrapper
from shapely.geometry import shape, mapping
from shapely import affinity
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
        "properties": {
            **paca["properties"],
            "nom": "PACA + Corse",
            "join_key": "PACA + Corse",
        },
        "geometry": mapping(paca_corse_geom),
    }

    outre_mer_list = [guadeloupe, martinique, guyane, reunion, mayotte]

    target_positions = [
        (-6.5, 50.0),
        (-6.5, 49.0),
        (-6.5, 48.0),
        (-6.5, 47.0),
        (-6.5, 46.0),
    ]

    moved_outre_mer = []

    for feature, (tgt_x, tgt_y) in zip(outre_mer_list, target_positions):
        geom = shape(feature["geometry"])

        if "Guyane" in feature["properties"].get("nom", ""):
            geom = affinity.scale(geom, xfact=0.2, yfact=0.2)
        else:
            geom = affinity.scale(geom, xfact=1.5, yfact=1.5)

        centroid = geom.centroid
        x_shift = tgt_x - centroid.x
        y_shift = tgt_y - centroid.y
        new_geom = affinity.translate(geom, xoff=x_shift, yoff=y_shift)

        new_properties = feature["properties"].copy()

        new_properties["join_key"] = "Outre-Mer"

        new_feature = {
            "type": "Feature",
            "properties": new_properties,
            "geometry": mapping(new_geom),
        }
        moved_outre_mer.append(new_feature)

    final_standard_regions = []
    standard_regions = [
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
    ]

    for reg in standard_regions:
        props = reg["properties"].copy()
        props["join_key"] = props.get("nom")
        final_standard_regions.append(
            {"type": "Feature", "properties": props, "geometry": reg["geometry"]}
        )

    new_features = [
        *final_standard_regions,
        paca_corse,
        *moved_outre_mer,
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
