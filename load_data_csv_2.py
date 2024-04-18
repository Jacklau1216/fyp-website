import pandas as pd
import json
import myGLTR
import os

def load_data(filename):
    # Load CSV file
    try:
        data = pd.read_csv(filename)
        print(f"Loaded {len(data)} records from {filename}.")
        # Map source from numeric to text labels
        data['source'] = data['source'].map({0: 'human', 1: 'AI'})
    except FileNotFoundError:
        print(f"File not found: {filename}")
        data = pd.DataFrame()
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        data = pd.DataFrame()
    return data

# Load your dataset
data = load_data("data/SQuAD_no_watermark_data_pred.csv")

# Initialize GPT-2 model from myGLTR
gpt2 = myGLTR.GPT2().model

# Filename for saving the processed data
filename = "./SQuAD_no_watermark_data_pred_gltr.json"

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
for i, row in data.iloc[start_index:].iterrows():
    print(row["source"])
    text = row['text'][:2048]  # Trim text if necessary
    try:
        k+=1
        print(k)
        m = gpt2.lm.check_probabilities(text, 40)
        real_topk = m["real_topk"]
        pred_topk = m["pred_topk"]
        fracp = gpt2.lm.getFracpCount(real_topk, pred_topk, [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1])
        topK = gpt2.lm.getTopKCount(real_topk, countArray)
        topKEntropy = gpt2.lm.getTopEntropy(pred_topk, prob_steps)
        # Append new result to dataset
        entry = {
            "id": i,
            "text": text,
            "fracp": fracp,
            "topK": topK,
            "topKEntropy": topKEntropy,
            "source": row["source"]
        }
        dataset_json.append(entry)
        if len(dataset_json) % 100 == 0:
            with open(filename, "w") as f:
                json.dump(dataset_json, f, indent=4)
            print(f"Saved {len(dataset_json)} entries.")
    except Exception as e:
        print(f"Error processing record {i}: {str(e)}")

# Final save to capture any remaining data
with open(filename, "w") as f:
    json.dump(dataset_json, f, indent=4)
print(f"Final save complete. Total entries saved: {len(dataset_json)}")
