import requests
import pandas as pd

# https://gisdata-occokc.opendata.arcgis.com/
# RDBMS_WELLS dataset

# browser-only
# https://gis.occ.ok.gov/server/rest/services/Hosted/RBDMS_WELLS/FeatureServer/220/query?where=county%3D%27KINGFISHER%27&outFields=*&returnGeometry=false&f=json

OCC_URL = "https://gis.occ.ok.gov/server/rest/services/Hosted/RBDMS_WELLS/FeatureServer/220/query"

FIELDS = [
    "api",
    "sh_lat",
    "sh_lon",
    "county",
    "well_name",
    "well_num",
    "operator",
    "symbol_class",
    "wellstatus",
    "welltype",
]

COLUMN_RENAMES = {
    "well_num": "well_number",
    "symbol_class": "well_symbol",
    "wellstatus": "well_status",
    "welltype": "well_type",
}


def get_occ_well_header_by_county(county="KINGFISHER") -> str | None:
    out_file = f"{county.lower()}_well_header_occ.csv"
    params = {
        "where": f"county='{county}'",  # case-sensitive
        "outFields": ",".join(FIELDS),  # use "*" for all
        "returnGeometry": "false",
        "f": "json",
        "resultOffset": 0,
        "resultRecordCount": 2000,  # (ArcGIS Online limit is allegedly 2000)
    }

    all_features = []

    while True:
        print(f"Fetching offset {params['resultOffset']} …")
        response = requests.get(OCC_URL, params=params)
        data = response.json()

        if "error" in data:
            print("Error received from server:", data["error"])
            break

        features = data.get("features", [])
        if not features:
            print("No more records.")
            break

        all_features.extend([feature["attributes"] for feature in features])

        if len(features) < params["resultRecordCount"]:
            break

        params["resultOffset"] += params["resultRecordCount"]

    if all_features:
        df = pd.DataFrame.from_records(all_features)
        df_adjusted = df[FIELDS].rename(columns=COLUMN_RENAMES)
        df_adjusted.to_csv(out_file, index=False)
        print(f"✅ Saved {len(df_adjusted)} rows to '{out_file}'")
        return out_file
    else:
        print("⚠ No data found for KINGFISHER county.")
        return None


result = get_occ_well_header_by_county(county="KINGFISHER")
print(result)
