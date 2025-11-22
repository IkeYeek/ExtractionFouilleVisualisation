#!/bin/bash

BASE_URL="https://open-data-assurance-maladie.ameli.fr/medicaments/download.php?Dir_Rep=Open_MEDIC_Base_Complete&Annee="
DOWNLOAD_BASE="https://open-data-assurance-maladie.ameli.fr/medicaments/"
YEARS=($(seq 2014 2024))
OUTPUT_DIR="./dataset"

rm -rf $OUTPUT_DIR
mkdir $OUTPUT_DIR

for year in "${YEARS[@]}"; do
  URL="$BASE_URL$year"
  echo $URL
  FILE_PATH=$(wget -q -O - "$URL" | sed -n 's/.*href="\([^"]*\)".*/\1/p')
  wget -P "$OUTPUT_DIR" "$DOWNLOAD_BASE$FILE_PATH"
  gunzip "$OUTPUT_DIR"/*.gz
  mv "$OUTPUT_DIR"/*.csv "$OUTPUT_DIR/ds_$year.csv"
done
