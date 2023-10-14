from bs4 import BeautifulSoup

#path = "data/dataUWA/cleanedJobData.xml"
path = "data/dataUWA/jobData.xml"

allJobs = []
with open(path, 'r', encoding='utf-8') as file:
    jobData = file.read()
    soup = BeautifulSoup(jobData, 'xml')
    allJobs = soup.find_all("Job")

def cleanSkill(value):
    allSkills = value.split("|")

    cleanSkills = []

    for skill in allSkills:
        if skill == "Specialised Skills":
            continue

        skillClean = ""
        try:
            skillClean = skill.split("Specialised Skills")[0]
        except:
            skillClean = skill

        skillClean = skillClean.strip()
        if skillClean == "":
            continue

        if skillClean[-1] == ";":
            skillClean = skillClean[:-1]

        cleanSkills.append(skillClean)

    return cleanSkills


def tripletFrom(obj, type, sub):
    return {'head': obj, 'type': type, "tail": sub}

def extractTripletsFromDict(dict):
    title = dict.get("title", None)
    employer = dict.get("employer", None)
    email = dict.get("Email", None)
    skills = dict.get("skills", None)
    jobDate = dict.get("jobDate", None)
    city = dict.get("city", None)
    country = dict.get("country", None)
    state = dict.get("state", None)
    salary = dict.get("salary", None)
    requiredDegrees = dict.get("requiredDegrees", None)
    experience = dict.get("experience", None)
    jobType = dict.get("jobType", None)

    triplets = []

    if jobType is not None:
        triplets.append(tripletFrom(title, 'job type', jobType))
    if employer is not None:
        triplets.append(tripletFrom(title, 'employer', employer))
        triplets.append(tripletFrom(employer, 'offers', title))
    if email is not None:
        triplets.append(tripletFrom(title, 'contact', email))
    if salary is not None:
        triplets.append(tripletFrom(title, 'earns', salary))
    if jobDate is not None:
        triplets.append(tripletFrom(title, 'posted on', jobDate))

    if city is not None:
        triplets.append(tripletFrom(title, 'city', city))
        triplets.append(tripletFrom(city, 'offers', title))
    if country is not None:
        triplets.append(tripletFrom(title, 'country', country))
        triplets.append(tripletFrom(country, 'offers', title))
    if state is not None:
        triplets.append(tripletFrom(title, 'state', state))
        triplets.append(tripletFrom(state, 'offers', title))

    if requiredDegrees is not None:
        triplets.append(tripletFrom(title, 'requires', requiredDegrees))
    if experience is not None:
        triplets.append(tripletFrom(title, 'requires', f"{experience} years experience"))
    if skills is not None:
        for skill in skills:
            triplets.append(tripletFrom(title, 'requires', skill))

    return triplets

knowledge = {}

tripletList = []
for job in allJobs:
    jobTags = job.find_all()

    jobDict = {}

    for tag in jobTags:
        value = tag.get_text().strip()
        if value is None or value == "":
            continue

        if "SkillClusters" in tag.name:
            jobDict["skills"] = cleanSkill(value)
        elif "CanonCity" in tag.name:
            jobDict["city"] = value
        elif "Email" in tag.name:
            jobDict["Email"] = value
        elif "CanonState" in tag.name:
            jobDict["state"] = value
        elif "JobType" in tag.name:
            jobDict["jobType"] = value
        elif "JobDate" in tag.name:
            jobDict["jobDate"] = value
        elif "CanonCountry" in tag.name:
            jobDict["country"] = value
        elif "MaxAnnualSalary" in tag.name:
            jobDict["salary"] = value
        elif "CleanJobTitle" in tag.name:
            jobDict["title"] = value
        elif "CanonRequiredDegrees" in tag.name:
            jobDict["requiredDegrees"] = value
        elif "MinExperience" in tag.name:
            jobDict["experience"] = value

    triplets = extractTripletsFromDict(jobDict)


    #print("\n\n\n")
    for triplet in sorted(triplets, key=lambda x: x["head"]):
        tripletList.append(triplet)
        #print(triplet)


with open("data/dataUWA/complete_jobTriples.json", "w") as text_file:
    text_file.write(tripletList)

#
# with open("data/dataUWA/cleanedJobData.xml", "w", encoding='utf-8') as output:
#     output.write(soup.prettify())
#
#
# soupedUnits = SoupExtractor("data/dataUWA/jobData.xml")
# soupedUnits.extract()
