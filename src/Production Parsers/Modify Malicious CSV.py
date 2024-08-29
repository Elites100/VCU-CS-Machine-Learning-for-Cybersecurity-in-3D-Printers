import csv
import os

def update_csv(csv1_filepath, csv2_directory):
    # Open csv1 and get the modified layers
    with open(csv1_filepath, 'r') as csv1_file:
        csv1_reader = csv.reader(csv1_file)
        next(csv1_reader)  # Skip header
        for row in csv1_reader:
            gcode_filename = row[0]
            modified_layers_str = row[2]
            modified_layers = modified_layers_str.split(',')

            # Open corresponding gcode_csvs file and update 'Modified' column
            csv2_filename = os.path.join(csv2_directory, gcode_filename.replace('.gcode', '.csv'))
            
            try:
                with open(csv2_filename, 'r') as csv2_file:
                    csv2_reader = csv.reader(csv2_file)
                    rows = list(csv2_reader)
            except FileNotFoundError:
                # print(f"CSV file not found: {csv2_filename}. Skipping.")
                continue  # Skip processing this CSV file
            
            with open(csv2_filename, 'w', newline='') as csv2_file:
                csv2_writer = csv.writer(csv2_file)
                csv2_writer.writerow(rows[0])  # Write header
                print(gcode_filename)
                for i in range(1, len(rows)):
                    print("i = " + str(i) + ", rows[i][0] = " + rows[i][0])
                    if rows[i][1] in modified_layers:
                        rows[i][-1] = '1'  # Assuming 'Modified' column is the last one
                        print("-------------changing layer " + rows[i][1] + " to a 1 in " + gcode_filename)
                    csv2_writer.writerow(rows[i])

# Example usage
csv1_filepath = r'Z:\Capstone Data\Dataset\G-Code - Bad\Modified_Files - 1\modified_files_info.csv'
csv2_directory = r'Z:\Capstone Data\Dataset\G-Code - Bad\Modified_Files - 1'
update_csv(csv1_filepath, csv2_directory)
