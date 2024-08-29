import csv
import os
import re

PARAMETERS = {
    'Fan speed': 'M106',
    'Fan on/off': 'M107',
    'Temperature': 'M104',
    'M205': 'M205',
    'Positioning': {'G90', 'G91'},
    'Spindle speed': 'S0',
}

# Regex patterns for known command structures
KNOWN_COMMAND_PATTERNS = [
    r'^G0 F\d+ Y\d+(\.\d+)?(\s*;.*)?$',  # Pattern 1: G0 rapid move with feedrate and Y coordinate
    r'^G0 F\d+ X\d+(\.\d+)? Y\d+(\.\d+)? Z\d+(\.\d+)?(\s*;.*)?$',  # Pattern 2: G0 rapid move with feedrate and XYZ coordinates
    r'^G1 F\d+ X\d+(\.\d+)? Y\d+(\.\d+)? Z\d+(\.\d+)?(\s*;.*)?$',  # Pattern 3: G1 linear move with feedrate and XYZ coordinates
    r'^G1 X\d+(\.\d+)? Y\d+(\.\d+)? Z\d+(\.\d+)?(\s*;.*)?$',  # Pattern 4: G1 linear move with only XYZ coordinates
    r'^G1 F\d+ X\d+(\.\d+)? Y\d+(\.\d+)? E\d+(\.\d+)?(\s*;.*)?$',  # Pattern 5: G1 linear move with feedrate, XY coordinates, and extrusion
    r'^G1 X\d+(\.\d+)? Y\d+(\.\d+)? E\d+(\.\d+)?(\s*;.*)?$',  # Pattern 6: G1 linear move with XY coordinates and extrusion
    r'^G0 F\d+ X\d+(\.\d+)? Y\d+(\.\d+)?(\s*;.*)?$',  # Pattern 7: G0 rapid move with feedrate and XY coordinates
    r'^G92 E\d+(\.\d+)?(\s*;.*)?$',  # Pattern 8: Pattern for setting extruder position
    r'^M82(\s*;.*)?$',  # Pattern 9: Pattern for setting extruder to absolute mode
    r'^G10(\s*;.*)?$',  # Pattern 10: Pattern for retract filament
    r'^M107(\s*;.*)?$',  # Pattern 11: Pattern for turning off fan
    r'^G0 F\d+ Y\d+(\.\d+)?(\s*;.*)?$',  # Pattern 12: Duplicate pattern
    r'^G0 X\d+(\.\d+)? Y\d+(\.\d+)?(\s*;.*)?$',  # Pattern 13: Pattern for G0 rapid move with XY coordinates
    r'^G1 F\d+ X\d+(\.\d+)? Y\d+(\.\d+)? E\d+(\.\d+)?(\s*;.*)?$',  # Pattern 14: Pattern for G1 linear move with feedrate, XY coordinates, and extrusion
    r'^M106 S\d+(\s*;.*)?$',  # Pattern 15: Pattern for turning on fan
    r'^G11(\s*;.*)?$',  # Pattern 16: Pattern for setting extruder to relative mode
    r'^G1 F\d+(\.\d+)? X\d+(\.\d+)? Y\d+(\.\d+)? E\d+(\.\d+)?(\s*;.*)?$',  # Pattern 17: Pattern for G1 linear move with feedrate, XY coordinates, and extrusion (with decimal feedrate)
    r'^G1 X\d+(\.\d+)? Y\d+(\.\d+)? E\d+(\.\d+)?(\s*;.*)?$',  # Pattern 18: Pattern for G1 linear move with XY coordinates and extrusion
    r'^G1 F\d+(\.\d+)? X\d+(\.\d+)? Y\d+(\.\d+)? E\d+(\.\d+)?(\s*;.*)?$',  # Pattern 19: Duplicate pattern
    r'^G1 X\d+(\.\d+)? Y\d+(\.\d+)?(\s*;.*)?$',  # Pattern 20: Pattern for G1 linear move with XY coordinates
    r'^G0 X\d+(\.\d+)? Y\d+(\.\d+)? Z\d+(\.\d+)?(\s*;.*)?$',  # Pattern 21: Pattern for G0 rapid move with XYZ coordinates
    # --------UM3--------
    r'^T\d+(\s*;.*)?$',  # Pattern 22: Pattern for tool change command
    r'^M109 S\d+(\s*;.*)?$',  # Pattern 23: Pattern for setting extruder temperature and waiting
    r'^G280(\s*;.*)?$',  # Pattern 24: Pattern for filament unload command
    r'^G1 F\d+ E-?\d+(\.\d+)?(\s*;.*)?$',  # Pattern 25: Pattern for linear move with feedrate and extrusion (including negative values)
    r'^M204 S\d+(\s*;.*)?$',  # Pattern 26: Pattern for setting default acceleration
    r'^G1 F\d+ E\d+(\.\d+)?(\s*;.*)?$',  # Pattern 27: Pattern for linear move with feedrate and extrusion
    r'^M205 X\d+ Y\d+(\s*;.*)?$',  # Pattern 28: Pattern for setting max feedrate
    r'^G1 F\d+ Z\d+(\.\d+)?(\s*;.*)?$',  # Pattern 29: Pattern for linear move with feedrate and Z coordinate
    r'^M104 S\d+(\.\d+)?(\s*;.*)?$',  # Pattern 30: Pattern for setting extruder temperature
    r'^G91(\s*;.*)?$',  # Pattern 31: Pattern for setting relative positioning
    r'^G0 F\d+ X\d+(\.\d+)? Z\d+(\.\d+)? E-?\d+(\.\d+)?(\s*;.*)?$',  # Pattern 32: Pattern for G0 rapid move with feedrate, XZ coordinates, and extrusion
    r'^G0 F\d+ Z\d+(\.\d+)? E\d+(\.\d+)?(\s*;.*)?$',  # Pattern 33: Pattern for G0 rapid move with feedrate, Z coordinate, and extrusion
    r'^G90(\s*;.*)?$',  # Pattern 34: Pattern for setting absolute positioning
    r'^M104 T\d+ S\d+(\.\d+)?(\s*;.*)?$',  # Pattern 35: Pattern for setting extruder temperature for specific tool
]

def read_gcode_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".gcode"):
            input_file_path = os.path.join(folder_path, filename)
            output_file_path = os.path.join(folder_path, f'{os.path.splitext(filename)[0]}.csv')
            read_gcode_file(input_file_path, output_file_path)

def read_gcode_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        
        # Write Header
        header = ['Layer', 'Fan on/off', 'Fan speed', 'Temperature', 'Extrusion Mode', 'Feedreate', 'Layer height', 'Regex', 'Modified', 'Unknown Commands']
        csv_writer.writerow(header)

        layer = '-1'
        temperature = '0'
        fan_on = '0'
        fan_speed = '0'
        current_temperature = '0'
        extrusion_mode = ''
        seen_m82 = False
        seen_m83 = False
        previous_height = '-1'
        current_height = '0'
        previous_feedrate = '-1'
        current_feedrate = '0'
        
        for line in input_file:
            line = line.strip()  # Remove leading/trailing whitespaces
            if not line or line.startswith(';'):
                if line.startswith(';LAYER:'):
                    layer = line.split(':')[-1]
                continue  # Skip empty lines and comments
            
            
            # Detect unknown commands using regex
            # Skips to the next line if the current line is not an acceptable command
            unknown_command_line = None
            matched = False
            regex_number = 0  # Default value if no regex pattern matches
            for idx, pattern in enumerate(KNOWN_COMMAND_PATTERNS, start=1):
                if re.match(pattern, line):
                    matched = True
                    regex_number = idx
                    break
            if not matched:
                unknown_command_line = line
                csv_writer.writerow([layer, fan_on, fan_speed, temperature, extrusion_mode, feedrate, current_height, regex_number, '0', unknown_command_line])
                continue
            

            # Extract layer height and layer height change
            if 'Z' in line:
                current_height = extract_layer_height(line)

                


            # Extract feedrate 
            if 'F' in line:
                feedrate = extract_feedrate(line)
                current_feedrate = feedrate

            else:
                feedrate = current_feedrate

            # Update temperature information
            if line.startswith('M109'):
                temperature = line.strip().split('M109 S')[-1]
                current_temperature = temperature
            elif line.startswith('M104 T1'):
                temperature = line.strip().split('M104 T1 S')[-1]
            elif line.startswith('M104') or line.startswith('M104 T1'):
                temperature = line.strip().split('M104 S')[-1]

            else:
                temperature = current_temperature
            
            # Update fan information
            if line.startswith('M106'):
                fan_speed = line.strip().split('S')[-1]
                fan_on = '1'
            elif line.startswith('M107'):
                fan_on = '0'
                fan_speed = '0'  # Set fan speed to 0 when fan is turned off
            
            
            
            # Update Extrusion Mode
            # 1 is absolute, 2 is realtive
            if 'M82' in line:
                extrusion_mode = '1'
                seen_m82 = True
                seen_m83 = False
            elif 'M83' in line:
                extrusion_mode = '2'
                seen_m83 = True
                seen_m82 = False
            elif seen_m82:
                extrusion_mode = '1'
            elif seen_m83:
                extrusion_mode = '2'
            else:
                extrusion_mode = '0'

                        # Write the line to the CSV file
            csv_writer.writerow([layer, fan_on, fan_speed, temperature, extrusion_mode, feedrate, current_height, regex_number, '0', unknown_command_line])

def extract_tokens(line):
    # Extract tokens from the line, stopping once a token with a semicolon is encountered
    tokens = []
    for token in line.split():
        if token.startswith(';'):
            break
        tokens.append(token)
    return tokens

def extract_layer_height(line):
    # Extract layer height from lines containing Z coordinates
    tokens = line.split()
    for token in tokens:
        if token.startswith('Z'):
            return token[1:]
    return "Error"

def extract_feedrate(line):
    # Extract feedrate from lines with an F-value
    tokens = line.split()
    for token in tokens:
        if token.startswith('F'):
            return token[1:]
    return "Error"


if __name__ == "__main__":
    folder_path = r'C:\Users\mabro\Desktop\3D Printers\Generated G-code'
    read_gcode_folder(folder_path)
