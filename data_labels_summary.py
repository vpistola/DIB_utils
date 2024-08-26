import os
from collections import Counter
import matplotlib.pyplot as plt

distinct_dir = 'D:/MICRO_ALGAE_DATASET/final_dataset/dataset/distinct/bbs'
clusters_dir = 'D:/MICRO_ALGAE_DATASET/final_dataset/dataset/clusters/bbs'
lines = []

## Search the distinct directory
for root, _, files in os.walk(distinct_dir):
    for file in files:
        filename = os.path.join(root, file)
        with open(filename) as file:
            lines.append([line.rstrip().split()[0] for line in file])

## Search the clusters directory
for root, _, files in os.walk(clusters_dir):
    for file in files:
        filename = os.path.join(root, file)
        with open(filename) as file:
            lines.append([line.rstrip().split()[0] for line in file])

def flatten_iterable(matrix):
    return [item for row in matrix for item in row]

def plot_bar(plot_data):
    data_label_type = list(plot_data.keys())
    data_label_type[0] = 'Chlorella vulgaris'
    data_label_type[1] = 'Clusters'
    data_label_count = list(plot_data.values())

    fig = plt.figure(figsize = (2, 2))

    # creating the bar plot
    plt.bar(data_label_type, data_label_count, color ='blue', width = 0.2)

    plt.xlabel("Data label")
    plt.ylabel("Count of data label")
    plt.title("Data label counts")
    plt.show()


lines = flatten_iterable(lines)
plot_data = Counter(lines)
print(plot_data)
plot_bar(plot_data)