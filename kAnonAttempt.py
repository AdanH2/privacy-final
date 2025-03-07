from pycanon.anonymity import k_anonymity, l_diversity, t_closeness
from pycanon import report
import random
import pandas as pd

data = {
    "Id": [i for i in range(1,101)],
    "Age": [random.randint(20, 50) for _ in range(100)],
    "Zipcode": [random.choice(["97225", "97035", "97203", "97068"]) for _ in range(100)],
    "Employment": [random.choice(["private", "government", "self", "other"]) for _ in range(100)],
    "Salary": [random.choice(["<20,000", "20,000", "40,000", "60,000", "80,000", "100,000", ">100,000"]) for _ in range(100)]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Print each row
"""for index, row in df.iterrows():
    print(row.to_dict())
"""

QI = ["Age","Zipcode","Employment"]
SA = ["Salary"]

k = k_anonymity(df,QI)

report.print_report(df,QI,SA)
grouped_data = df.groupby(QI).size().reset_index(name="Group Size")
print("\nAnonymity Groups:")
print(grouped_data)

data = {
    "Id": [i for i in range(1,101)],
    "Age": [random.randint(20, 50) for _ in range(100)],
    "Zipcode": [random.choice(["97225", "97035", "97203", "97068"]) for _ in range(100)],
    #"Employment": [random.choice(["private", "government", "self", "other"]) for _ in range(100)],
    "Salary": [random.choice(["<20,000", "20,000", "40,000", "60,000", "80,000", "100,000", ">100,000"]) for _ in range(100)]
}

df = pd.DataFrame(data)

# 🟢 Generalize Age (grouping into bins of 10)
df["Age"] = df["Age"] // 20 * 20  # Converts 23 → 20, 34 → 20, 48 → 40

# 🟢 Generalize Zipcode (only first 3 digits)
df["Zipcode"] = df["Zipcode"].str[:3] + "XX"  # "97225" → "9XXXX"

# 🟢 Merge Employment categories
#df["Employment"] = df["Employment"].replace({"self": "other"})  # Merge "self" into "other"

"""for index, row in df.iterrows():
    print(row.to_dict())
    """


# Define QI & SA
#QI = ["Age", "Zipcode", "Employment"]
QI = ["Age", "Zipcode"]

SA = ["Salary"]

# Compute k-anonymity
k = k_anonymity(df, QI)
print(f"Updated k-anonymity level: {k}")

# Print anonymity report
r3 =report.print_report(df, QI, SA)


grouped_data = df.groupby(QI).size().reset_index(name="Group Size")
print("\nAnonymity Groups:")
print(grouped_data)



# Group data by quasi-identifiers to see anonymity groups
df["Anonymity Group Size"] = df.groupby(QI)[QI[0]].transform("count")

# Sort the data by anonymity groups for better visualization
sorted_data = df.sort_values(by=["Anonymity Group Size"], ascending=False)

print("\nData Grouped by Anonymity Level:\n")
print(sorted_data)

# Compute k-Anonymity
k_value = k_anonymity(df, QI)

# Compute l-Diversity
l_value = l_diversity(df, QI, SA)

# Compute t-Closeness
t_value = t_closeness(df, QI, SA)

# Print extracted values
print(f"k-Anonymity: {k_value}")
print(f"l-Diversity: {l_value}")
print(f"t-Closeness: {t_value}")