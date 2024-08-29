import os
import pandas as pd

def remove_column_and_replace_value(folder_path):
    # List all files in the folder
    files = os.listdir(folder_path)
    
    for file in files:
        # Check if the file is a CSV file
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            
            # Remove the 'regex' column if it exists
            if 'Regex' in df.columns:
                df.drop(columns=['Regex'], inplace=True)
            
            # Replace -1 with 0 in the 'Layer' column
            df['Layer'] = df['Layer'].replace(-1, 0)
            
            # Save the modified DataFrame back to the same CSV file
            df.to_csv(file_path, index=False)
            print(f"Modified {file}")

# Provide the path to the folder containing the CSV files
folder_path = r"C:\Users\traee\Downloads\Senior Project\Testing_Bad"
remove_column_and_replace_value(folder_path)
