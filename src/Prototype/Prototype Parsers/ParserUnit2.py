import os
import csv

def extract_info(file_path):
  # Open the file and initialize counters
  with open(file_path, 'r') as file:
      
    # Variable for tracking incorrect commands
    incorrect_commands = 0

    # Variables for tracking line numbers and layer numbers
    line_number = 0
    current_layer = 0
    layer_number = 0
    
    
    # Read each line 
    for line in file:
        # Add lines to total lines
        line_number += 1
        # Check for layers
        # check total line commands of line x of layer x
        if line.startswith(';LAYER:'):
          current_layer += 1
          layer_number += int(line.split(';LAYER:')[1])

########################################Incorrect commands############################################
######################################################################################################
  
        if not line.startswith(('G0', 'G1', 'G4' , 'G28', 'G11', 'G10', 'G92', 'M107', 'M106', 'M82', 'G280', 'M204', 'M205', 'M104', 'G91', 'T1', 'G90', 'M109', ';')):
            # Count incorrect commands
            incorrect_commands += 1

  return incorrect_commands, line_number, current_layer, layer_number
           
        
def process_folder(folder_path, output_csv):
  # Create or overwrite the CSV file
  with open(output_csv, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write header
    csv_writer.writerow(['Filename', 'incorrect_commands', 'TotalLines', 'TotalLayers', 'TotalLayerNumbers'])

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
      if filename.endswith(".gcode"):
        file_path = os.path.join(folder_path, filename)

        # Extract information
        incorrect_commands, line_number, current_layer, layer_number = extract_info(file_path)
        

        # Write information to CSV
        csv_writer.writerow([filename, incorrect_commands, str(line_number), str(current_layer), str(layer_number)])

if __name__ == "__main__":
  # Specify the folder containing .gcode files and the output CSV file
  folder_path = r'C:\Users\Kevin Phung\Documents\Classes\Computer science\Project 3D printing\TestingFiles'  # Use 'r' to create a raw string
  output_csv = 'output2.csv' # Excel CSV file that appears in the current code file

  # Process the folder and write results to CSV
  process_folder(folder_path, output_csv)
