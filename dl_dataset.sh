#!/bin/bash
set -e

OUTPUT_DIR="./dataset"

BASE_URL="https://open-data-assurance-maladie.ameli.fr/medicaments/download.php?Dir_Rep=Open_MEDIC_Base_Complete&Annee="
DOWNLOAD_BASE="https://open-data-assurance-maladie.ameli.fr/medicaments/"
YEARS=($(seq 2014 2024))
TMP_DIR="$OUTPUT_DIR/tmp"

mkdir -p "$TMP_DIR"

curl -L "https://www.assurance-maladie.ameli.fr/sites/default/files/2024_descriptif-variables_open-medic.xls" -o "$OUTPUT_DIR/var_desc.xls"

for year in "${YEARS[@]}"; do
  URL="$BASE_URL$year"
  FILE_PATH=$(wget -q -O - "$URL" | sed -n 's/.*href="\([^"]*\)".*/\1/p')

  if [ -z "$FILE_PATH" ]; then
    echo "Error: Could not extract file path for year $year"
    exit 1
  fi

  if [[ $FILE_PATH == *.zip ]]; then
    curl -L "$DOWNLOAD_BASE$FILE_PATH" -o "$TMP_DIR/$year.zip" || exit 1
    unzip -d "$TMP_DIR" "$TMP_DIR/$year.zip" || exit 1
    rm "$TMP_DIR/$year.zip"
    mv "$TMP_DIR"/* "$OUTPUT_DIR/OPEN_MEDIC_$year.csv"
  else
    curl -L "$DOWNLOAD_BASE$FILE_PATH" -o "$TMP_DIR/$year.gz" || exit 1
    gunzip "$TMP_DIR/$year.gz" || exit 1
    mv "$TMP_DIR"/* "$OUTPUT_DIR/OPEN_MEDIC_$year.csv"
  fi
  sleep 30 # desperate attempt to fight rate limits...
done
