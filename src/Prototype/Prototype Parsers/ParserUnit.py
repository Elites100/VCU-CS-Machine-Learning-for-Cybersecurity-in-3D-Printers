import os
import csv

def extract_info(file_path):
  # Open the file and initialize counters
  with open(file_path, 'r') as file:
      
    # Variables for print time
    # Storing Total distance travel and max speed 
    total_travel_distance = 0
    max_speed = 0

    
    # Variables for print range
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    min_z, max_z = float('inf'), float('-inf')
    max_height = float('-inf')

    # Variables for occurrence of G28 (included in print range)
    G28_count = 0
    
    # Read each line and ignore the comments 
    for line in file:
      if line.startswith(';'):
        # Ignore comments
        continue

################################################### FEATURE 1 #########################################
################################################## Print Time #########################################
      # Max Speed calculations using F (The maximum movement rate of the move) in G1 or G0
      if line.startswith(('G0 ', 'G1 ')):
        speed_code = [code for code in line.split() if code.startswith('F')]
        if speed_code:
          speed = float(speed_code[0][1:])  # Extract speed value
          max_speed = max(max_speed, speed)  # Update maximum speed

      # Extract distance information from G0 and G1 commands
      if line.startswith(('G0 ', 'G1 ')):
        distance_code = [code for code in line.split() if code.startswith(('X', 'Y', 'Z'))]
        if distance_code:
          distances = [float(code[1:]) for code in distance_code]  # Extract distance values
          total_travel_distance += sum(distances)  # Update total travel distance
  
######################################## FEATURE 2 AND 3 ###############################################
#################################### Print Range AND MAX PH & PW #######################################
      # Count occurance of G28 code
      G28_count = line.count('G28')

      if line.startswith(('G0 ', 'G1 ')):
        distance2_code = [code for code in line.split() if code.startswith(('X', 'Y', 'Z'))]
        if distance2_code:
          for code in distance2_code:
            axis, value = code[0], float(code[1:])
            if axis == 'X':
              min_x = min(min_x, value)
              max_x = max(max_x, value)
            elif axis == 'Y':
              min_y = min(min_y, value)
              max_y = max(max_y, value)
            elif axis == 'Z':
              min_z = min(min_z, value)
              max_z = max(max_z, value)
              # Update maximum height
              max_height = max(max_height, value)  

  # Calculate print width
  print_width = max_x - min_x if max_x != float('-inf') and min_x != float('inf') else 0

  # Calculate estimated print time
  if max_speed > 0:
    print_time = total_travel_distance / max_speed
  else:
    print_time = 0

  return round(print_time,2), (min_x, max_x), (min_y, max_y), (min_z, max_z), G28_count, max_height, round(print_width,2), max_speed
           
        
def process_folder(folder_path, output_csv):
  # Create or overwrite the CSV file
  with open(output_csv, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)

    # Write header
    csv_writer.writerow(['Filename', 'PrintTime', 'PrintRangeX', 'PrintRangeY', 'PrintRangeZ', 'G28_count', 'MaxHeight', 'PrintWidth', 'MaxSpeed'])

    # Iterate through files in the folder
    for filename in os.listdir(folder_path):
      if filename.endswith(".gcode"):
        file_path = os.path.join(folder_path, filename)

        # Extract information
        print_time, print_range_x, print_range_y, print_range_z, G28_count, max_height, print_width, maxSpeed = extract_info(file_path)
        

        # Write information to CSV
        csv_writer.writerow([filename, print_time, str(print_range_x), str(print_range_y), str(print_range_z), G28_count, max_height, print_width, maxSpeed])

if __name__ == "__main__":
  # Specify the folder containing .gcode files and the output CSV file
  folder_path = r'C:\Users\Kevin Phung\Documents\Classes\Computer science\Project 3D printing\TestingFiles'  # Use 'r' to create a raw string
  output_csv = 'output.csv' # Excel CSV file that appears in the current code file

  # Process the folder and write results to CSV
  process_folder(folder_path, output_csv)

























# for line in file:
#     if line.startswith(';Time'):
#         print_time_str = line.strip().split()
#         printTime = float(print_time_str)
