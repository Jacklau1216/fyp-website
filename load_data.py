import os
import json

def load_data(dataset_name, split):
    # Path to the directory where datasets are stored
    base_path = './'

    # Construct the file name and its path
    file_name = f"{dataset_name}.json"
    file_path = os.path.join(base_path, file_name)

    data = []
    # Try to open the file and load its contents
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Load the entire file as a JSON array
            data = json.load(file)
        print(f"Loaded {len(data)} records from {file_name}.")
    except FileNotFoundError:
        print(f"File not found: {file_name}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_name}")

    return data
# List of dataset names and splits
datasets = [
    'webtext',
    'small-117M', 'small-117M-k40',
    'medium-345M', 'medium-345M-k40',
    'large-762M', 'large-762M-k40',
    'xl-1542M', 'xl-1542M-k40',
]

splits = ['train', 'valid', 'test']

import json
import myGLTR
import os

# Load your dataset
data = load_data("merged_output", "")


# Initialize GPT-2 model
gpt2 = myGLTR.GPT2().model

# Filename for saving the processed data
filename = "xsum-half-gltr.json"

# Load existing data if file exists to resume
if os.path.exists(filename):
    with open(filename, "r") as f:
        dataset_json = json.load(f)
    start_index = len(dataset_json)  # Determine the starting index
else:
    dataset_json = []
    start_index = 0

# Parameters for model analysis
countArray = [10, 100, 1000, 10000]
prob_steps = [i * 0.2 for i in range(13)]
k=0

# Process data starting from the last saved index
for i in data[start_index:]:
    for j in i:
        try:
            text = i[j][:2048]  # Trim text if necessary
            m = gpt2.lm.check_probabilities(text, 40)
            real_topk = m["real_topk"]
            pred_topk = m["pred_topk"]
            fracp = gpt2.lm.getFracpCount(real_topk, pred_topk, [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
            topK = gpt2.lm.getTopKCount(real_topk, countArray)
            topKEntropy = gpt2.lm.getTopEntropy(pred_topk, prob_steps)
            k+=1
            print(k)
            # Append new result to dataset
            entry = {
                "id": j,
                "text": text,
                "fracp": fracp,
                "topK": topK,
                "topKEntropy": topKEntropy,
                "source": "AI"
            }
            dataset_json.append(entry)
        except:
            pass
        if len(dataset_json) % 100 == 0:
            with open(filename, "w") as f:
                json.dump(dataset_json, f, indent=4)
            print(f"Saved {len(dataset_json)} entries.")

# Final save to capture any remaining data
with open(filename, "w") as f:
    json.dump(dataset_json, f, indent=4)
print(f"Final save complete. Total entries saved: {len(dataset_json)}")
