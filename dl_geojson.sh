curl -L "https://france-geojson.gregoiredavid.fr/repo/regions.geojson" -o "dataset/regions_temp.json"
python3 "merge_regions.py" "dataset/regions_temp.json" "dataset/regions.json"
rm "dataset/regions_temp.json"
