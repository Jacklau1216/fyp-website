import pandas as pd
import json

# Load the datasets
def load_and_prepare_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data =json.load(file)
    except:
        data = []
        # Try to open the file and load its contents
        try:
            file_name = file_path
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # Load each line as a separate JSON object
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON from line in file: {file_name}")

            print(f"Loaded {len(data)} records from {file_name}.")
        except FileNotFoundError:
            print(f"File not found: {file_name}")
    return pd.json_normalize(data)


df1 = load_and_prepare_data('./xsum-mixed-gltr.json')
# df2 = load_and_prepare_data('./gltr_webtext.json')
# print(df1)
# Merge the two datasets
# df = pd.concat([df1,df2], ignore_index=True)
df = df1
# Convert source to binary (0, 1) where 'AI' might be 1 and 'human' might be 0
df['source'] = (df['source'] == 'AI').astype(int)
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Assuming all features except 'id', 'text', and 'source' are used as predictors
X = df.drop(['id', 'text', 'source'], axis=1)
y = df['source']
label_counts = df['source'].value_counts()

# Now, let's print out the counts for each label.
print(label_counts)
# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train a logistic regression model
model = LogisticRegression(max_iter=1000)  # Increased max_iter for convergence
model.fit(X_train, y_train)
from joblib import dump

# 'model' is the trained model object
dump(model, 'gltr_logistic.joblib')
# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
print(classification_report(y_test, y_pred))

