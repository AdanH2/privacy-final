from flask import render_template
from flask.views import MethodView, request

from pycanon.anonymity import k_anonymity, l_diversity, t_closeness
from pycanon import report
import random
import pandas as pd

class kAnonymity(MethodView):
    def get(self):
        # Initial GET request: Render the template with no form data
        return render_template('kAnonymity.html', 
                               ageCheck=None, 
                               zipCheck=None, 
                               employmentCheck=None, 
                               salaryCheck=None, 
                               diseaseCheck=None,
                               ageGenLevel=None,
                               zipGenLevel=None,
                               emplymentGenLevel=None,
                               grouped_data=None)

    def dispatch_request(self):
        if request.method == 'POST':
            # Retrieve form data
            ageCheck = request.form.get('cb1')
            zipCheck = request.form.get('cb2')
            employmentCheck = request.form.get('cb3')
            salaryCheck = request.form.get('cb4')
            diseaseCheck = request.form.get('cb5')
            ageGenLevel = request.form.get('sp1')
            zipGenLevel = request.form.get('sp2')
            emplymentGenLevel = request.form.get('sp3')

            # construct dictionary of id + QIs + SAs
            QI = []
            SA = []
            data = {
                "Id": [i for i in range(1, 101)],
            }
            if ageCheck == 'on':
                data["Age"] = [random.randint(20, 50) for _ in range(100)]
                QI.append("Age")
            if zipCheck == 'on':
                data["Zipcode"] = [random.choice(["97225", "97035", "97203", "97038"]) for _ in range(100)]
                QI.append("Zipcode")
            if employmentCheck == 'on':
                data["Employment"] = [random.choice(["private", "government", "self", "other"]) for _ in range(100)]
                QI.append("Employment")
            if salaryCheck == 'on':
                data["Salary"] = [random.choice(["<20,000", "20,000", "40,000", "60,000", "80,000", "100,000", ">100,000"]) for _ in range(100)]
                SA.append("Salary")
            if diseaseCheck == 'on':
                data["Disease"] = [random.choice(["diabetes", "cancer", "heart disease", "asthma"]) for _ in range(100)]
                SA.append("Disease")

            df = pd.DataFrame(data)

            # do generalizations if desired

            if ageGenLevel == "1":
                df["Age"] = df["Age"] // 5 * 5
            elif ageGenLevel == "2":
                df["Age"] = df["Age"] // 10 * 10
            elif ageGenLevel == "3":
                df["Age"] = df["Age"] // 20 * 20
            
            if zipGenLevel == "1":
                df["Zipcode"] = df["Zipcode"].str[:4] + "X"
            elif zipGenLevel == "2":
                df["Zipcode"] = df["Zipcode"].str[:3] + "XX"
            elif zipGenLevel == "3":
                df["Zipcode"] = df["Zipcode"].str[:2] + "XXX"

            if emplymentGenLevel == "1":
                df["Employment"] = df["Employment"].replace({"self": "other"})
            elif emplymentGenLevel == "2":
                df["Employment"] = df["Employment"].replace({"self": "other", "government": "private or government", "private": "private or government"})
            elif emplymentGenLevel == "3":
                df["Employment"] = df["Employment"].replace({"self": "*", "government": "*", "private": "*", "other": "*"})

            # do k-anonymity
            k = k_anonymity(df, QI)
            report.print_report(df, QI, SA)
            grouped_data = df.groupby(QI+SA).size().reset_index(name="Group Size")

            k_value = k_anonymity(df, QI)
            l_value = l_diversity(df, QI, SA)
            t_value = t_closeness(df, QI, SA)
            
            # Render template with form data
            return render_template('kAnonymity.html', 
                                   ageCheck=ageCheck, 
                                   zipCheck=zipCheck, 
                                   employmentCheck=employmentCheck, 
                                   salaryCheck=salaryCheck, 
                                   diseaseCheck=diseaseCheck, 
                                   ageGenLevel=ageGenLevel, 
                                   zipGenLevel=zipGenLevel, 
                                   emplymentGenLevel=emplymentGenLevel, 
                                   grouped_data=grouped_data.to_html(classes='table table-bordered'),
                                   k_value=k_value, 
                                   l_value=l_value, 
                                   t_value=t_value)

        # Default case (GET or non-POST): Render template with no form data
        return render_template('kAnonymity.html', 
                               ageCheck=None, 
                               zipCheck=None, 
                               employmentCheck=None, 
                               salaryCheck=None, 
                               diseaseCheck=None,
                               ageGenLevel=None,
                               zipGenLevel=None,
                               emplymentGenLevel=None,
                               grouped_data=None)
