import pandas as pd
import os
import csv
import tqdm

input_directory = 'tabset'
merged_data = pd.DataFrame()

for filename in tqdm.tqdm(os.listdir(input_directory)):
    if filename.endswith('.xlsx'):
        file_path = os.path.join(input_directory, filename)
        df = pd.read_excel(file_path)
        merged_data = merged_data.append(df, ignore_index=True)

# Filter rows where 'title', 'content', 'category', and 'date' are not empty
filtered_df = merged_data.dropna(subset=['title', 'content', 'category', 'date'])

# Select only the desired columns
selected_columns = ['title', 'content', 'category', 'date']
filtered_df = filtered_df[selected_columns]

# Save the merged data to a CSV file with proper character handling
filtered_df.to_csv('Tabnak.csv', index=False, encoding='utf-8', quoting=csv.QUOTE_NONNUMERIC)
