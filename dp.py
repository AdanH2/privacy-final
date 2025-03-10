from flask import render_template, request, session
from flask.views import MethodView
import pandas as pd
from io import StringIO
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import statistics
import pydp as dp
from pydp.algorithms.laplacian import BoundedMean, BoundedSum, Count

load_dotenv()
chatGPTKey = os.getenv('CHATGPT_KEY')

class DP(MethodView):
    def get(self):
        return render_template('dp.html')
    
    def post(self):
        if request.form.get('num_rows') and request.form.get('num_cols') and request.form.get('prompt'):
            rows = request.form.get('num_rows')
            columns = request.form.get('num_cols')
            prompt = request.form.get('prompt')

            # url = "https://raw.githubusercontent.com/OpenMined/PyDP/dev/examples/Tutorial_1-carrots_demo/animals_and_carrots.csv"
            # df = pd.read_csv(url, sep=",", names=["animal", "carrots_eaten"])
            # print(df.head(int(rows)))
            # print(type(df.head()))

            # data = df.head(int(rows)).to_dict(orient='records')
            # print(data)


            chatGPTKey = os.getenv('CHATGPT_KEY')
            client = OpenAI(api_key=chatGPTKey)

            messages = [
                {"role": "system", "content": "You are a providing data needed to tranform easily to a csv format."},
                {"role": "user", "content": f"Give me the answer to the following question in a table format with {rows} rows and {columns} columns. Please provide just the table and no other information."},
                {"role": "assistant", "content": "Sure! Please provide the type of data you would like to see."},
                {"role": "user", "content": f"{prompt}"},
            ]

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            data=response.choices[0].message.content
            # data = """
            #     | Zip Code | Age | Income  | Gender | Occupation        |
            #     |----------|-----|---------|--------|--------------------|
            #     | 10001    | 29  | 55000   | Male   | Software Engineer   |
            #     | 10002    | 34  | 72000   | Female | Marketing Manager   |
            #     | 10003    | 46  | 85000   | Male   | Doctor              |
            #     | 10004    | 52  | 95000   | Female | Lawyer              |
            #     | 10005    | 23  | 43000   | Female | Graphic Designer    |
            #     | 10006    | 31  | 62000   | Male   | Data Scientist      |
            #     | 10007    | 38  | 78000   | Female | Project Manager     |
            #     | 10008    | 44  | 83000   | Male   | Architect           |
            #     | 10009    | 27  | 49000   | Male   | Teacher             |
            #     | 10010    | 36  | 91000   | Female | Financial Analyst   |
            #     | 10011    | 41  | 67000   | Male   | Nurse               |
            #     | 10012    | 55  | 104000  | Female | University Professor |
            #     | 10013    | 29  | 50000   | Male   | Sales Representative |
            #     | 10014    | 48  | 85000   | Female | HR Manager          |
            #     | 10015    | 39  | 72000   | Male   | Research Scientist   |
            #     | 10016    | 33  | 64000   | Female | Customer Service Rep |
            #     | 10017    | 25  | 48000   | Male   | Web Developer       |
            #     | 10018    | 30  | 58000   | Female | Data Analyst        |
            #     | 10019    | 43  | 88000   | Male   | Business Analyst    |
            #     | 10020    | 54  | 123000  | Female | CEO                 |
            #     """

            # Step 1: Clean the string by removing '|' and '-' characters and trimming spaces
            cleaned_data = re.sub(r'[\|\-]', '', data)

            # Step 2: Remove leading/trailing spaces and unnecessary empty lines
            cleaned_data = "\n".join(line.strip() for line in cleaned_data.splitlines() if line.strip())

            # Step 3: Replace multiple spaces with a single space to ensure correct column separation
            cleaned_data = re.sub(r'\s{2,}', ',', cleaned_data)

            # Step 4: Add headers (they were removed with the '|')
            # cleaned_data = "Zip Code,Age,Income,Gender,Occupation\n" + cleaned_data

            data_io = StringIO(cleaned_data)

            df = pd.read_csv(data_io)

            data_dicts = df.to_dict(orient='records')


            print(df)
            print("\nList of dictionaries:")
            print(type(data_dicts))

            return render_template('dp.html', data2=data_dicts)
        
        elif request.files['file']:
            file = request.files['file']
            df = pd.read_csv(file)
            data_dicts = df.to_dict(orient='records')
            return render_template('dp.html', data1=data_dicts)
        
    def mean(self, data, column) -> float:
        return statistics.mean(list(map(lambda x: x[column], data)))
    
    def sum_data(self, data, column) -> float:
        return sum(list(map(lambda x: x[column], data)))
    
    def count(self, data) -> int:
        return len(data)
    
    def mean_dp(self, data, column, epsilon, lower_bound=None, upper_bound=None) -> float:
        if lower_bound is None or upper_bound is None:
            mean = BoundedMean(epsilon=epsilon)
        else:
            mean = BoundedMean(epsilon=epsilon, lower_bound=lower_bound, upper_bound=upper_bound, dtype='float')
        return mean.quick_result(list(map(lambda x: x[column], data)))
    
    def sum_dp(self, data, column, epsilon, lower_bound=None, upper_bound=None) -> float:
        if lower_bound is None or upper_bound is None:
            sum = BoundedSum(epsilon=epsilon, dtype='float')
        else:
            sum = BoundedSum(epsilon=epsilon, delta = 0, lower_bound=lower_bound, upper_bound=upper_bound, dtype='float')
        return sum.quick_result(list(map(lambda x: x[column], data)))
    
    def count_dp(self, data, column, epsilon) -> int:
        count = Count(epsilon=epsilon, dtype='int')
        return count.quick_result(list(map(lambda x: x[column], data)))
        