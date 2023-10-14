# clean with beautiful soup so there are less tokens
# parse with langChain to build customized schemas

from bs4 import BeautifulSoup


class SoupExtractor():
    def __init__(self, path):
        self.path = path

    def extract(self):

        with open(self.path, 'r', encoding='utf-8') as file:
            jobData = file.read()

        soup = BeautifulSoup(jobData, 'xml')

        tagsToKeep = ["CanonCity", "CleanJobTitle", "JobText", "CanonCertification", "CanonSkillClusters",
                      "CanonSkills", "CanonRequiredDegrees", "MinExperience", "MaxAnnualSalary"]

        allJobs = soup.find_all("Job")

        for job in allJobs:
            jobTags = job.find_all()

            for tag in jobTags:
                if tag.name not in tagsToKeep:
                    tag.extract()

        with open("data/dataUWA/cleanedJobData.xml", "w", encoding='utf-8') as output:
            output.write(soup.prettify())


soupedUnits = SoupExtractor("data/dataUWA/jobData.xml")
soupedUnits.extract()
