import matplotlib.pyplot as plt

def plot_dataset(dataset):
    for attr in dataset.combined_attr_list:
      print(attr)
      print(dataset.normalized_dataframe[attr])
      plt.hist(dataset.normalized_dataframe[attr])
      plt.show()
    print("Goals")
    for target in dataset.target_vars:
        plt.hist(dataset.normalized_dataframe[target])
        plt.show()