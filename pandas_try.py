import pandas as pd


# Step 1: Prepare the Data
data1 = pd.read_excel('data_table.xlsx')
X = data1.iloc[:, -1:].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)  # Input features (keywords)

print (X)