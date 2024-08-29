import os
import re
import random
import csv
from shutil import copyfile

def parse_gcode_file(file_path):
    """
    Parse a G-Code file and extract the layer count.

    Args:
    file_path (str): Path to the G-Code file.

    Returns:
    int: The total number of layers found in the G-Code file.
    """
    layer_count = 0
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(";LAYER_COUNT:"):
                try:
                    layer_count = int(line.split(":")[1].strip())
                    break
                except (IndexError, ValueError):
                    continue
    return layer_count

def select_and_modify_layers(gcode_file_path):
    """
    Select random lines from the beginning of a random layer in a G-Code file
    and modify parameters randomly.

    Args:
    gcode_file_path (str): Path to the G-Code file.

    Returns:
    str: Modified G-Code content after modifications.
    str: Modified file name indicating the modified layers.
    list: Information about modified layers.
    """
    modified_layers_info = []  # Information about modified layers
    random_layer = 0

    # Parse the G-Code file to get the layer count
    layer_count = parse_gcode_file(gcode_file_path)

    if layer_count == 0:
        print("No layer count information found in the G-Code file.")
        return None, None, None

    # Select a random layer within the valid range (0 to layer_count - 1)
    if layer_count > 0:
        random_layer = random.randint(1, layer_count - 1)
    else:
        print("Invalid layer count.")
        return None, None, None

    if random_layer == 0:
        random_layer += 1

    elif random_layer == layer_count:
        random_layer -= 1
    # Open the G-Code file and read its content
    with open(gcode_file_path, 'r') as file:
        gcode_lines = file.readlines()

    
    
    
    # Find the start and end indices of the selected layer
    start_index = None
    end_index = None
    current_layer = -1
    for i, line in enumerate(gcode_lines):
        if line.startswith(";LAYER:"):
            try:
                current_layer = int(line.split(":")[1].strip())
                if current_layer == random_layer:
                    start_index = i + 1  # Start of thse selected layer
                elif current_layer > random_layer:
                    end_index = i - 1  # End of the previous layer
                    break
            except (IndexError, ValueError):
                current_layer = -1

    if start_index is None:
        print(f"Layer {random_layer} not found in the G-Code file.")
        return None, None, None

    if end_index is None:
        end_index = len(gcode_lines) - 1  # End of the last layer

    # Select a random number of lines from the start of the layer to modify
    num_lines_to_modify = random.randint(1, min(10, end_index - start_index + 1))  # Maximum 10 lines

    # Randomly select lines to modify
    lines_to_modify_indices = random.sample(range(start_index, end_index + 1), num_lines_to_modify)


    # Randomly select a parameter to modify
    choice = random.choice(['1'])
    
    # Modify parameters for the selected lines
    modified_lines = gcode_lines[:]  # Create a copy of the original lines


    # Modify the selected parameter based on random choice 

    # turns the fan on/off

    line_index = 0
    count = 0
    if choice == '1':
        new_value = random.choice(['y', 'n'])
        m107_lines = []
        for i, line in enumerate(gcode_lines):
            if line.startswith("M107"):
                m107_lines.append(i)  # Append the line to the m107_lines list
                count += 1
        last_layer = parse_gcode_file(gcode_file_path)
        if new_value == 'y':  # If choice is to turn the fan on
            length = len(m107_lines)
            last_m107 = m107_lines[length - 1]
            new_line = random.choice([';\n', 'M106 S255\n'])
            modified_lines[last_m107] = new_line

            modified_layers_info.append((last_layer, f"Fan On"))
                    
        elif new_value == 'n':  # If choice is to turn the fan off
            
            # Construct the new line with the M107 command
            new_line = 'M107\n'

            
            # Insert the new line at the current line_index
            modified_lines.insert(start_index + random.randint(1, 20), new_line)
            modified_layers_info.append((random_layer, "Fan OFF"))
        
    if choice == '2':
        for line_index in lines_to_modify_indices:
            line = modified_lines[line_index]
            new_value = str(random.randint(0, 255))
            new_line = f'M106 S{new_value}\n'  # Construct the new line with the random value
            modified_lines.insert(line_index, new_line)  # Insert the new line at the specified index
            modified_layers_info.append((random_layer, f"Fan Speed: {new_value}"))

    elif choice == '3':
        for line_index in lines_to_modify_indices:
            line = modified_lines[line_index]
            new_value = str(random.randint(0, 99999))
            new_line = f'M109 S{new_value}\n'  # Construct the new line with the random value
            modified_lines.insert(line_index, new_line)  # Insert the new line at the specified index
            modified_layers_info.append((random_layer, f"Temperature: {new_value}"))

    elif choice == '4':
        for line_index in lines_to_modify_indices:
            new_value = str(random.uniform(0, 5))
            line = modified_lines[line_index]
            linelist = line.split()
            for i, item in enumerate(linelist):
                if item.startswith("Z"):
                    linelist[i] = "Z" + new_value

            new_line = ' '.join(linelist) + '\n'  # Reconstruct the modified line with spaces and add a newline
            modified_lines[line_index] = new_line  # Replace the line in the modified lines list
            modified_layers_info.append((random_layer, f"Layer Height: {new_value}"))

    elif choice == '5':
        for line_index in lines_to_modify_indices:
            new_value = str(random.uniform(0,5))
            linelist = line.split()
            for i, item in enumerate(linelist):
                if item.startswith("E"):
                    linelist[i] = "E" + new_value
    
            new_line = ' '.join(linelist)  # Reconstruct the modified line with spaces and add a newline
            modified_lines.insert(line_index, new_line)  # Insert the new line at the specified index
            modified_layers_info.append((random_layer, f"Extrusion Rate: {new_value}"))


    # Return modified G-Code content, modified file name, and information about modified layers
    modified_gcode_content = ''.join(modified_lines)
    file_name_without_extension = os.path.splitext(os.path.basename(gcode_file_path))[0]
    modified_file_name = f"{file_name_without_extension}_Layer-{random_layer}.gcode"

    return modified_gcode_content, modified_file_name, modified_layers_info

def write_to_csv(file_name, data):
    """
    Write data to a CSV file.

    Args:
    file_name (str): Name of the CSV file.
    data (list of tuples): Data to be written to the CSV file.
    """
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['File Name', 'Modification', 'Layer'])
        writer.writerows(data)

def main():
    g_code_folder_path = r'Z:\Capstone Data\Dataset\Bad G-Code\Modified_Files'
    modified_folder_path = r'Z:\Capstone Data\Dataset\Bad G-Code\Modified_Files'

    # Create a folder to store modified files if it doesn't exist
    if not os.path.exists(modified_folder_path):
        os.makedirs(modified_folder_path)

    gcode_files = []
    for filename in os.listdir(g_code_folder_path):
        if filename.endswith(".gcode"):
            gcode_files.append(os.path.join(g_code_folder_path, filename))
            

    # List G-Code files in the specified folder
    gcode_files = [f for f in os.listdir(g_code_folder_path) if f.endswith('.gcode')]

    if not gcode_files:
        print("No G-Code files found in the current directory.")
        return

    modified_files_info = {}  # Information about modified files

    # Process each G-Code file
    for file_name in gcode_files:
        file_path = os.path.join('.', file_name)
        print(file_path)
        print(f"Processing G-Code file: {file_name}")
        
        modified_gcode, modified_file_name, modified_layers_info = select_and_modify_layers(file_path)

        if modified_gcode:
            # Check if the modified file already exists in the destination directory
            modified_file_path = os.path.join(modified_folder_path, modified_file_name)
            if not os.path.exists(modified_file_path):
                # Save modified G-Code to a new file
                with open(modified_file_path, 'w') as modified_file:
                    modified_file.write(modified_gcode)
                print(f"Modified G-Code saved to: {modified_file_path}")

                modified_files_info[modified_file_name] = modified_layers_info

    # Write information about modified files to a CSV file
    csv_data = [(file_name, layer[1], f"Layer {layer[0]}") for file_name, layers_info in modified_files_info.items() for layer in layers_info]
    write_to_csv(os.path.join(modified_folder_path, 'modified_files_info.csv'), csv_data)

    print("Processing completed.")

if __name__ == "__main__":
    main()
