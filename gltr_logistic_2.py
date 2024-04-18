import pandas as pd
import json

# Load the datasets
def load_and_prepare_data(file_path):
    with open(file_path, 'r') as file:
        data = pd.json_normalize(json.load(file))

    return data


df1 = load_and_prepare_data('./xsum-half.train.jsonl.json')
df2 = load_and_prepare_data('./xsum-mixed-gltr.json')

# Merge the two datasets
df = pd.concat([df1, df2], ignore_index=True)
# Convert source to binary (0, 1) where 'AI' might be 1 and 'human' might be 0
df['source'] = (df['source'] == 'AI').astype(int)
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Assuming all features except 'id', 'text', and 'source' are used as predictors
X = df.drop(['id', 'text', 'source'], axis=1)
y = df['source']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train a logistic regression model
model = LogisticRegression(max_iter=1000)  # Increased max_iter for convergence
model.fit(X_train, y_train)
from joblib import dump

# 'model' is the trained model object
# dump(model, 'gltr_logistic.joblib')
# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred))

