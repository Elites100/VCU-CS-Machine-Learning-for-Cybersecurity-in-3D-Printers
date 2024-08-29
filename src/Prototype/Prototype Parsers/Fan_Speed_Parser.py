import csv

def read_gcode_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        
        # Declare Variable
        FanSpeed = '0'
        layer = '0';
        CurrentSpeed = '0'
        change = '0'

        #Write Header
        csv_writer.writerow(['Layer', 'FanSpeed', 'Change'])
        
        for line in input_file:
            
            # Check for New Layer or else skip
            if not line:
                continue
            elif line.startswith(';LAYER:'):
                layer = line.strip().split(':')[-1]
            elif line.startswith(';'):
                continue
            
            # Reads FanSpeed (Change if Needed) (UM3)
            if line.startswith('M106'):
                FanSpeed = line.strip().split('M106 S')[-1]
                if FanSpeed != CurrentSpeed:
                    change = abs(float(FanSpeed) - float(CurrentSpeed))
                elif FanSpeed == FanSpeed:
                    continue
                CurrentSpeed = FanSpeed
            elif line.startswith('M107'):
                FanSpeed = 0
                if FanSpeed != CurrentSpeed:
                    change = abs(float(FanSpeed) - float(CurrentSpeed))
                elif FanSpeed == FanSpeed:
                    continue
                CurrentSpeed = FanSpeed

            if FanSpeed != CurrentSpeed:
                    change = abs(float(FanSpeed) - float(CurrentSpeed))
            CurrentSpeed = FanSpeed   
            # Write the line to the CSV file
            csv_writer.writerow([layer,FanSpeed, change])

if __name__ == "__main__":
    GCode = 'UM3_bag-01_Lines_10_75_100_0_0_Normal'
    input_file_path = r'C:\\Users\\sleep\\OneDrive\\Desktop\\Senior Project\\G-Code\\' + GCode + '.gcode'
    output_file_path = 'FanSpeed_' + GCode + '.csv'
    read_gcode_file(input_file_path, output_file_path)