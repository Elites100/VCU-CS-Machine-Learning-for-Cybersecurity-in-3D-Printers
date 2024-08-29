import os
import pandas as pd

def delete_files_with_same_name(csv_file_path, directory_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path)

    # Check if the 'filename' column exists
    if 'File Name' not in df.columns:
        print("Error: 'filename' column not found in the CSV file.")
        return

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        filename = row['File Name']
        file_path = os.path.join(directory_path, filename)
        # Check if the file exists
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)
            print(f"Deleted file: {filename}")
        else:
            print(f"File not found: {filename}")

# Example usage
csv_file_path = 'Z:\Capstone Data\Error.csv'
directory_path = 'Z:\Capstone Data\Dataset\CSV - Bad'
delete_files_with_same_name(csv_file_path, directory_path)
