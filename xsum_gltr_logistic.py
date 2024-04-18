import pandas as pd
import json
from sklearn.metrics import classification_report
from joblib import load
# Function to load data from a JSON file
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = pd.json_normalize(json.load(file))
    return data
# def load_data(filename):
#     records = []
#     with open(filename, 'r', encoding='utf-8') as file:
#         for line in file:
#             records.append(json.loads(line))
#     data = pd.json_normalize(records)
#     return data
# Load datasets
df1 = load_data('.json')
df2 = load()
# Merge the datasets

# Convert 'source' to binary: 1 for 'AI' and 0 for 'Human'
df_combined['source'] = (df_combined['source'] == 'AI').astype(int)

# Assuming all necessary features are present and preprocessed
X = df_combined.drop(['id', 'text', 'source'], axis=1)
y = df_combined['source']
# Load the pre-trained logistic regression model
model = load('gltr_logistic.joblib')

# Predict on the entire dataset
y_pred = model.predict(X)
# Generate and print the classification report
report = classification_report(y, y_pred, target_names=['Human', 'AI'])
print(report)
