from enverus_developer_api import DeveloperAPIv3
import pandas as pd
import json

STATE = "OK"

v3 = DeveloperAPIv3(secret_key=SECRET_KEY)


def get_enverus_well_header_by_county(county="KINGFISHER") -> str | None:
    out_file = f"{county.lower()}_well_header_enverus.csv"

    records = []
    query = v3.query("well-headers", StateProvince=STATE, County=county)

    counter = 0

    for i, record in enumerate(query, start=1):
        counter += 1
        row = {
            "api": record["API_UWI_Unformatted"],
            "sh_lat": record["Latitude"],
            "sh_lon": record["Longitude"],
            "county": record["County"],
            "well_name": record["WellName"],
            "well_number": record["WellNumber"],
            "operator": record["ENVOperator"],
            "well_symbol": record["WellSymbols"],
            "well_status": record["ENVWellStatus"],
            "well_type": record["ENVWellType"],
        }
        records.append(row)

    df = pd.DataFrame.from_records(records)

    df.to_csv(out_file, index=False)
    print(f"✅ Saved {len(df)} rows to '{out_file}'")
    return out_file


get_enverus_well_header_by_county(county="KINGFISHER")
