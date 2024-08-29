import csv

def read_gcode_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        
        # Declare Variable
        temperature = '0'
        layer = '0'
        CurrentTemperature = '0'
        change = '0'
        
        #Write Header
        csv_writer.writerow(['Layer', 'Temperature','Change'])
        
        for line in input_file:
            
            # Check for New Layer or else skip
            if not line:
                continue
            elif line.startswith(';LAYER:'):
                layer = line.strip().split(':')[-1]
            elif line.startswith(';'):
                continue
            
            # Reads Temperatue (Change if Needed)
            if line.startswith('M109'):
                temperature = line.strip().split('M109 S')[-1]
            elif line.startswith('M104 T1'):
                temperature = line.strip().split('M104 T1 S')[-1]
                if temperature != CurrentTemperature:
                    change = abs(float(temperature) - float(CurrentTemperature))
                elif temperature == temperature:
                    continue
                CurrentTemperature = temperature
                
            elif line.startswith('M104') or line.startswith('M104 T1'):
                temperature = line.strip().split('M104 S')[-1]
                if temperature != CurrentTemperature:
                    change = abs(float(temperature) - float(CurrentTemperature))
                elif temperature == temperature:
                    continue
                CurrentTemperature = temperature

            # Write the line to the CSV file
            csv_writer.writerow([layer,temperature,change])

if __name__ == "__main__":
    GCode = 'UM3_bag-01_Lines_10_75_100_0_0_Normal'
    input_file_path = r'C:\\Users\\sleep\\OneDrive\\Desktop\\Senior Project\\G-Code\\' + GCode + '.gcode'
    output_file_path = 'Temperature_' + GCode + '.csv'
    read_gcode_file(input_file_path, output_file_path)