import os
from bs4 import BeautifulSoup
import pandas as pd

class ConvertUnitsIntoJson():
    def __init__(self, path):
        self.path = path

    def extract(self):
        df = pd.DataFrame(columns=["Unit Code", "Title", "School", "Content", "Unit Learning Outcomes"])

        courses = os.listdir(self.path)
        for course in courses:
            coursePath = f"{self.path}/{course}"

            with open(coursePath, 'r', encoding='utf-8') as file:
                html_content = file.read()

            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the specific elements you want to extract
            unit_code = soup.find('th', text='Unit Code').find_next('td').text.strip()
            title = soup.find('th', text='Title').find_next('td').text.strip()
            school = soup.find('th', text='School').find_next('td').text.strip()
            content = soup.find('th', text='Content').find_next('td').text.strip()


            #Extract Unit Learning Outcomes
            outcomes = []
            outcomes_table = soup.find('th', text='Unit Learning Outcomes').find_next('table')
            for row in outcomes_table.find_all('tr')[1:]:
                outcome = row.find_all('td')[1].text.strip()
                outcomes.append(outcome)

            # Create the JSON data structure
            course_info = {
                "Unit Code": unit_code,
                "Title": title,
                "School": school,
                "Content": content,
                "Unit Learning Outcomes": outcomes
            }

            # Append course_info to a panda dataframe
            df = df.append(course_info, ignore_index=True)

        return df


# Parse html units with bs4 & save into json
# soupedUnits = ConvertUnitsIntoJson("data/dataUWA/Outlines/2023")
# df1 = soupedUnits.extract()
# df1.transpose().to_json(f"data/dataUWA/extractedInformation/soupedUnits2023.json")
#df1.to_csv(f"data/dataUWA/extractedInformation/soupedUnits2023.csv")

