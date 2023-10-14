import json

# Load the JSON data from the file
with open('data/dataUWA/extractedInformation/soupedUnits2023.json', 'r') as file:
    data = json.load(file)

# Iterate over each unit
for unit_key, unit_values in data.items():
    print(f"Unit {unit_key}:")

    # Access and print specific values within the unit
    print("Unit Code:", unit_values.get("Unit Code", ""))
    print("Title:", unit_values.get("Title", ""))
    print("School:", unit_values.get("School", ""))
    print("Content:", unit_values.get("Content", ""))
    print("Unit Learning Outcomes:", unit_values.get("Unit Learning Outcomes", []))
    print()  # Print an empty line to separate units