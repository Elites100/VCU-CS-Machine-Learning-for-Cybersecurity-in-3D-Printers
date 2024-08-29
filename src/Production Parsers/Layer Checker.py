import os
import csv

def find_non_numeric_layers(folder_path, output_file):
    # List all files in the folder
    files_with_error = []
    files = os.listdir(folder_path)
    
    # Loop through each file
    for file_name in files:
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                header = next(csv_reader)  # Get header row
                layer_index = None
                for i, col in enumerate(header):
                    if col.strip().lower() == 'layer':
                        layer_index = i
                        break
                if layer_index is None:
                    print(f"Error: 'Layer' column not found in file '{file_name}'")
                    continue
                
                # Iterate through each row
                for row in csv_reader:
                    # Check if layer column contains non-numeric value
                    try:
                        layer_value = float(row[layer_index])
                    except ValueError:
                        files_with_error.append(file_name)
                        break

    # Write list of files with errors to a new CSV file
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Files with Non-Numeric Layer Values'])
        csv_writer.writerows([[file] for file in files_with_error])
    print(f"CSV file '{output_file}' created listing files with non-numeric layer values.")

# Example usage
folder_path = r"Z:\Capstone Data\Dataset\CSV - Bad"
output_file = "files_with_errors.csv"
find_non_numeric_layers(folder_path, output_file)