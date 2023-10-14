import json
import openai
import os
import time


path = "data/dataUWA/extractedInformation/soupedUnits2023.json"

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = os.environ["OPENAI_API_KEY"]



with open(path, 'r') as file:
    data = json.load(file)


def cleanContent(content):
    # Extract key words
    promptContent = f"""Extract topics from the following text:'{content} \n 
                Return a single string using the "|" as a seperator: topic1|topic2|topic3|.. """
    responseContent = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "user", "content": promptContent}])

    output = responseContent.choices[0].message.content
    return output



def cleanOutcome(outcome):
    # Extract key words
    promptContent = f"""Compress this outcome:'{outcome} \n 
    Keep key outcomes and return only the compressed version in lowercase, nothing else"""
    responseContent = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                   messages=[{"role": "user", "content": promptContent}])

    output = responseContent.choices[0].message.content
    return output



def tripletFrom(obj, type, sub):
    return {'head': obj, 'type': type, "tail": sub}



def extractTripletsFromDict(dict):
    unitCode = dict.get("Unit Code", None)
    title = dict.get("Title", None)
    school = dict.get("School", None)
    content = dict.get("Content", None)
    outcomes = dict.get("Unit Learning Outcomes", None)

    triplets = []

    if unitCode is not None:
        triplets.append(tripletFrom(title, 'unit code', unitCode))
    if school is not None:
        triplets.append(tripletFrom(title, 'located in', school))
        triplets.append(tripletFrom(school, 'offers', title))
    if content is not None:
        skillList = cleanContent(content)
        skillListSplit = skillList.split("|")
        for skill in skillListSplit:
            triplets.append(tripletFrom(title, 'topic', skill))
    if outcomes is not None:
        for outcome in outcomes:
            summarizedOutcome = cleanOutcome(outcome)
            triplets.append(tripletFrom(title, 'outcome', summarizedOutcome))

    return triplets


# Iterate over each unit
triplets = []
fhandle = open("data/dataUWA/unitTriples_complete.txt", "a")
dataToWorkOn = list(data.values())
itemsFinished = 0

while len(dataToWorkOn) > itemsFinished:
    for unit_values in dataToWorkOn[itemsFinished:]:
        try:
            print(f"Working on item {itemsFinished}")
            unitTriplets = extractTripletsFromDict(unit_values)

            for triplet in sorted(unitTriplets, key=lambda x: x["head"]):
                triplets.append(triplet)

            itemsFinished += 1
        except:
            print(f"We crashed after {len(triplets)} items.")
            break

        #print("\n\n\n")


    if(itemsFinished < len(dataToWorkOn)):
        print(f"We did {len(triplets)} courses so far.")
        print("Retry in 30s")
        time.sleep(30)

print("Writing all Triplets to file")
with open("data/dataUWA/unitTriples_complete.json", "w") as file:
   json.dump(triplets, file)

print("done")
