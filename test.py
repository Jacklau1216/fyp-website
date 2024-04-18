import json
import pandas as pd
import matplotlib.pyplot as plt

# Mock data list, replace with actual data loading method
def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)
def load_jsonl(file_path):

    records = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    # Each line is a separate JSON object
                    record = json.loads(line)
                    records.append(record)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e} on line {line}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return pd.DataFrame(records)

def concat_data(file_path1, file_path2):

    # Load data from both files
    data1 = load_json(file_path1)
    data2 = load_json(file_path2)

    # Convert lists of dictionaries to DataFrames
    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)

    # Concatenate the DataFrames
    concatenated_df = pd.concat([df1, df2], ignore_index=True)

    return concatenated_df
# Example usage:
# Load data

# Convert to DataFrame
# df = pd.DataFrame(data)
# df = load_json("xsum-mixed-gltr.json")
df = concat_data("gltr_webtext.json","gltr_small_117M.json")
# Assume data is loaded into a DataFrame `df`
# Separating AI and Human data
df_ai = df[df['source'] == 'AI']
df_human = df[df['source'] == 'human']
print(df_human)
# Function to aggregate values
def aggregate_data(df, key):
    # Aggregates nested dictionaries into a single dictionary summing up all values for each key
    aggregated = {}
    for index, row in df.iterrows():
        data_dict = row[key]
        for k, v in data_dict.items():
            if k in aggregated:
                aggregated[k] += v
            else:
                aggregated[k] = v
    return aggregated

fracp_ai = aggregate_data(df_ai, 'fracp')
fracp_human = aggregate_data(df_human, 'fracp')
topK_ai = aggregate_data(df_ai, 'topK')
topK_human = aggregate_data(df_human, 'topK')
topKEntropy_ai = aggregate_data(df_ai, 'topKEntropy')
topKEntropy_human = aggregate_data(df_human, 'topKEntropy')
# Create plots
fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(12, 12))
fig.tight_layout(pad=5.0)

# Helper function to create a bar plot
def create_bar_plot(ax, data, title, xlabel, ylabel):
    keys = list(map(str, sorted(data.keys())))
    values = [data[key] for key in keys]
    ax.bar(keys, values, color='skyblue')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

# Create plots for AI
create_bar_plot(axes[0, 0], fracp_ai, 'AI Frac(P) Distribution', 'Frac(P) value', 'Count')
create_bar_plot(axes[1, 0], topK_ai, 'AI TopK Distribution', 'TopK', 'Count')
create_bar_plot(axes[2, 0], topKEntropy_ai, 'AI Top10 Entropy Distribution', 'Top10 Entropy', 'Count')

# Create plots for Human
create_bar_plot(axes[0, 1], fracp_human, 'Human Frac(P) Distribution', 'Frac(P) value', 'Count')
create_bar_plot(axes[1, 1], topK_human, 'Human TopK Distribution', 'TopK', 'Count')
create_bar_plot(axes[2, 1], topKEntropy_human, 'Human Top10 Entropy Distribution', 'Top10 Entropy', 'Count')

fig.savefig("openai.svg")