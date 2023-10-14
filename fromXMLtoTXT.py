import json

# Load the JSON data from the file
with open('data/dataUWA/extractedInformation/soupedUnits2023.json', 'r') as file:
    data = json.load(file)

documents = []



# Iterate over each unit
for unit_key, unit_values in data.items():

    print(unit_values)
    break

    title = unit_values.get("Title", "")
    unitCode = unit_values.get("Unit Code", "")
    school = unit_values.get("School", "")
    content = unit_values.get("Content", "")
    outcomes = unit_values.get("Unit Learning Outcomes", [])

    #print([outcomes[index] for index, _ in len(outcomes)])


    cleanedOutcome = ""
    for index, _ in enumerate(outcomes):
        if index == len(outcomes) - 1:
            cleanedOutcome += outcomes[index] + "."
            break

        cleanedOutcome += outcomes[index] + "; "



    text = f"{title} is a unit at the {school}.\nThe unit code is {unitCode}.\n {content} \nThe outcomes of this unit are: {cleanedOutcome} \n\n"
    print(text)
    print("")

    with open("data/dataUWA/Output_someExamples2.txt", "a") as text_file:
        text_file.write(text)

    if unit_key == 20:
        break

