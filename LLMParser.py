import openai
import pandas as pd
import spacy

openai.api_key = "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"


class LLMParser():
    def __init__(self, csvPath):
        self.path = csvPath


    def extract(self):
        # Create a new DataFrame to store the cleaned data
        cleaned_df = pd.DataFrame(columns=["Unit Code", "Title", "School", "Content", "Unit Learning Outcomes"])

        df = pd.read_csv(self.path)
        for index, row in df.iterrows():
            unit_code = row['Unit Code']
            title = row['Title']
            school = row['School']
            content = row['Content']

            outcomes = row['Unit Learning Outcomes']


            # Extract key words
            promptContent = f"Generate triples from the following text:'{content}'"
            responseContent = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": promptContent}])
            cleanedContent = responseContent.choices[0].message.content

            promptOutcomes = f"Extract skills/outcomes from the following text: '{outcomes}'. Structure your answer as a list (csv format)"
            responseContent = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": promptOutcomes}])
            cleanedOutcomes = responseContent.choices[0].message.content

            # Append the cleaned data to the new DataFrame
            cleaned_df = cleaned_df.append({
                "Unit Code": unit_code,
                "Title": title,
                "School": school,
                "Content": cleanedContent,
                "Unit Learning Outcomes": cleanedOutcomes
            }, ignore_index=True)
            break

        return cleaned_df





#answer = completion.choices[0].message.content


