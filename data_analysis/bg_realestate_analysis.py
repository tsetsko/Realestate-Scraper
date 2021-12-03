import pandas as pd
import os
import matplotlib

dataset_original = pd.read_csv('/Users/tdonov/Desktop/Python/Realestate Scraper/master_data_for_realestate.csv')
dataset_original.head()

dataset = dataset_original.copy()

columns_to_drop = ['description', 'link']
dataset = dataset.drop(columns=columns_to_drop)

dataset_sofia = dataset.loc[dataset['city_or_province'] == "София"].reset_index()
dataset_sofia_province = dataset.loc[dataset['city_or_province'] != "София"].reset_index()

unique_hoods = dataset_sofia['location'].unique()
print(len(unique_hoods))

print(unique_hoods)
# print(dataset_sofia)
# print(dataset_sofia_province)