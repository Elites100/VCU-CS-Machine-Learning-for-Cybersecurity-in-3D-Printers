import os
import pandas as pd

def calculate_layer_average(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    
    for file in files:
        # Check if the file is a CSV file
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            
            # Group by the 'Layer' column and calculate the mean for each group
            df_grouped = df.groupby('Layer').mean().reset_index()
            
            # Save the grouped DataFrame back to the same CSV file
            df_grouped.to_csv(file_path, index=False)
            print(f"Modified {file}")

# Provide the path to the folder containing the CSV files
folder_path = r"C:\Users\traee\Downloads\Senior Project\Testing_Bad"
calculate_layer_average(folder_path)
