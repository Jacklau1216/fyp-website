import os
import json

# The directory containing your .sum files
directory = "."
data = []

# Iterate over the files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".sum"):
        # Extract the id from the filename pattern "{i}-{id}.sum"
        file_id = filename.split('-')[-1].rstrip('.sum')

        # Construct the file path
        file_path = os.path.join(directory, filename)

        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()

        # Create a dictionary with the id, text, and source
        entry = {
            "id": file_id,
            "text": text_content,
            "source": "AI"
        }

        # Append the dictionary to the list
        data.append(entry)

# Write the list to a JSON file
with open("xsum-gpt3.json", "w", encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4)
