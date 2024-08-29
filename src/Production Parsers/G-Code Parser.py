import csv
import os
import re

# Define global variables for previous temperature and fan speed
global previous_temperature
global previous_fan_speed

def read_gcode_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".gcode"):
            input_file_path = os.path.join(folder_path, filename)
            output_file_path = os.path.join(folder_path, f'{os.path.splitext(filename)[0]}.csv')
            read_gcode_file(input_file_path, output_file_path)

def read_gcode_file(input_file_path, output_file_path):
    """
    Reads a single G-code file, processes it, and writes the results to a CSV file.

    Parameters:
        input_file_path (str): The path to the input G-code file.
        output_file_path (str): The path to the output CSV file.
    """
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        # Write CSV header
        csv_writer.writerow(['Ultimaker Version', 'Layer', 'Fan on/off', 'Fan speed (min)', 'Fan speed (max)', 'Fan speed (avg)',
                             'Temperature (min)', 'Temperature (max)', 'Temperature (avg)',
                             'Feedrate (min)', 'Feedrate (max)', 'Feedrate (avg)', 'Layer height', 'modified'])

        ultimaker_version = 2
        layer = '-1'
        temperature_values = []  # Store temperature values for each layer
        fan_on = '0'
        fan_speed = []
        feedrate_values = []  # Store feedrate values for each layer
        current_height = '0'
        layer_0_found = False  # Flag to indicate if layer 0 is found
        current_temperature = 0  # Variable to store the current temperature
        previous_temperature = 0
        modified = 0;

        for line in input_file:
            line = line.strip()
            if line.startswith(';'):
                if line.startswith(';LAYER:'):
                    # Process data for the previous layer
                    if layer_0_found:
                        process_layer_data(ultimaker_version, layer, fan_on, temperature_values, fan_speed, feedrate_values, current_height, modified, csv_writer)
                    # Reset data for the new layer
                    layer = line.split(':')[-1]
                    if temperature_values:
                        previous_temperature = temperature_values[-1]  # Update previous_temperature with the last temperature value
                        temperature_values = [previous_temperature]  # Keep the last temperature value
                    if fan_speed:
                        previous_fan_speed = fan_speed[-1]  # Update previous_fan_speed with the last fan speed value
                        fan_speed = [previous_fan_speed]  # Keep the last fan speed value
                    if feedrate_values:
                        previous_feedrate = feedrate_values[-1]
                        feedrate_values = [previous_feedrate]
                    if layer == '0':
                        layer_0_found = True
                continue

            elif line.startswith('M109'):
                current_temperature = extract_temperature_value(line)
                temperature_values.append(current_temperature)
                ultimaker_version = 3

            if not layer_0_found:
                continue

            if 'Z' in line:
                current_height = extract_layer_height(line)

            if 'F' in line:
                feedrate_values.append(float(extract_feedrate(line)))

            if line.startswith('M104') or line.startswith('M109'):
                temperature = extract_temperature_value(line)
                if temperature is not None:
                    current_temperature = temperature
            elif len(temperature_values) > 0 and current_temperature != 0:
                    temperature_values.append(previous_temperature)

            if 'M106' in line:
                fan_speed.append(float(re.search(r'S(\d+(?:\.\d+)?)', line).group(1)))
                fan_on = '1'

            elif line.startswith('M107'):
                fan_on = '0'
                fan_speed.append(0)  # Set fan speed to 0 when fan is turned off


            if 'M104' in line or 'M109' in line:
                current_temperature = extract_temperature_value(line)
                temperature_values.append(current_temperature)
                previous_temperature = current_temperature

        # Process data for the last layer
        if layer_0_found:
            process_layer_data(ultimaker_version, layer, fan_on, temperature_values, fan_speed, feedrate_values, current_height, modified, csv_writer)

def process_layer_data(ultimaker_version, layer, fan_on, temperature_values, fan_speed, feedrate_values, current_height, modified, csv_writer):
    """
    Process the data for a single layer and write it to the CSV file.

    Parameters:
        layer (str): The layer number.
        temperature_values (list): List of temperature values for the layer.
        fan_speed (list): List of fan speed values for the layer.
        feedrate_values (list): List of feedrate values for the layer.
        current_height (str): The height of the current layer.
        modified (int): Identified if a modification occured in this layer.
        csv_writer (csv.writer): CSV writer object for writing data to the output file.
    """
    global previous_temperature, previous_fan_speed

    # Use values from the last layer if not specified for the current layer
    if not temperature_values:
        min_temperature = 0
        max_temperature = 0
        avg_temperature = 0
    else:
        min_temperature = min(temperature_values)  # Minimum temperature of this layer
        max_temperature = max(temperature_values)
        avg_temperature = sum(temperature_values) / len(temperature_values) if temperature_values else 0

    if not fan_speed:
        min_fan_speed = 0
        max_fan_speed  = 0
        avg_fan_speed = 0

    else:
        min_fan_speed = min(fan_speed)
        max_fan_speed = max(fan_speed)
        avg_fan_speed = sum(fan_speed) / len(fan_speed)

    min_feedrate = min(feedrate_values) if feedrate_values else 0
    max_feedrate = max(feedrate_values) if feedrate_values else 0
    avg_feedrate = sum(feedrate_values) / len(feedrate_values) if feedrate_values else 0

    if layer != '0':   
        csv_writer.writerow([ultimaker_version, layer, fan_on, min_fan_speed, max_fan_speed, avg_fan_speed,
                         min_temperature, max_temperature, avg_temperature, 
                         min_feedrate, max_feedrate, avg_feedrate,
                         current_height, modified])
    else:
        csv_writer.writerow([ultimaker_version, layer, fan_on, min_fan_speed, max_fan_speed, avg_fan_speed,
                         min_temperature, max_temperature, avg_temperature, 
                         min_feedrate, max_feedrate, avg_feedrate,
                         current_height, modified])

def extract_layer_height(line):
    """
    Extracts the layer height from a line of G-code.

    Parameters:
        line (str): A line of G-code.

    Returns:
        str: The layer height extracted from the line.
    """
    tokens = line.split()
    for token in tokens:
        if token.startswith('Z'):
            return token[1:]
    return "Error"

def extract_feedrate(line):
    """
    Extracts the feedrate from a line of G-code.

    Parameters:
        line (str): A line of G-code.

    Returns:
        str: The feedrate extracted from the line.
    """
    tokens = line.split()
    for token in tokens:
        if token.startswith('F'):
            return token[1:]
    return "Error"

def extract_temperature_value(line):
    """
    Extracts the temperature value from a line of G-code starting with M104 or M109.

    Parameters:
        line (str): A line of G-code.

    Returns:
        float: The temperature value extracted from the line.
    """
    if line.startswith('M104') or line.startswith('M109'):
        temperature_match = re.search(r'S(\d+(\.\d+)?)', line)
        if temperature_match:
            return float(temperature_match.group(1))
    return None

if __name__ == "__main__":
    folder_path = r'Z:\Capstone Data\Dataset\G-Code - Good'
    read_gcode_folder(folder_path)
