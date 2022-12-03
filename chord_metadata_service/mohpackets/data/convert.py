import json
import sys
import os
from pathlib import Path

"""
    This script helps to convert the raw data generated by Mockaroo into a 
    format that can be used by Django fixtures.

"""

# Path to the synthetic data folder
script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
synthetic_folder_path = os.path.join(script_dir, "synthetic_data")
fixtures_folder_path = os.path.join(script_dir, "fixtures")
# create fixtures folder if it doesn't exist
Path(fixtures_folder_path).mkdir(parents=True, exist_ok=True)


# get all the json names in the directory data
json_names = []
for file in os.listdir(synthetic_folder_path):
    if file.endswith(".json"):
        json_names.append(file)

# open each json file
for file_name in json_names:
    print(f"Processing {file_name}...")
    obj_name = file_name.split(".")[0].lower()
    dj_fixtures = []
    with open(f"{synthetic_folder_path}/{file_name}") as f:
        data = json.load(f)

        for line in data:
            # create new json object
            dj_fixture = {"model": "mohpackets." + obj_name, "fields": line}
            dj_fixtures.append(dj_fixture)

    # write to new json file
    with open(f"{fixtures_folder_path}/{file_name}", "w") as f:
        json.dump(dj_fixtures, f, indent=4)
