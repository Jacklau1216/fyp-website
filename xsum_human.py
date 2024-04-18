from datasets import load_dataset
import json

# Load the ai_summaries_dataset.json to get the list of ids
with open('merged_output.json', 'r', encoding='utf-8') as json_file:
    ai_data = json.load(json_file)

# print(ai_data[0])
# Convert ai_data to a dictionary for faster access
ai_data_dict = [  i for j in ai_data for i in j ]
print(ai_data_dict)
# Load the XSum dataset
dataset = load_dataset('xsum')

# Access the training set
train_dataset = dataset['train']

# Prepare a list to store the new data
human_data = []

# Iterate over the training set and collect data for ids that are in ai_data_dict
for entry in train_dataset:
    entry_id = str(entry['id'])
    if entry_id in ai_data_dict:
        human_entry = {
            "id": entry_id,
            "text": entry['document'],
            "source": "Human"
        }
        human_data.append(human_entry)

# Save the human_data list to a JSON file
with open("xsum-half-human.json", "w", encoding='utf-8') as json_file:
    json.dump(human_data, json_file, indent=4)