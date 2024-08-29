import csv
import re
import os
from collections import defaultdict

def parse_gcode(filename, speed_per_layer):
    current_layer = None
    speed_values = defaultdict(list)
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith(';LAYER:'):
                current_layer = line.strip().split(':')[-1]
            elif line.strip() and not line.startswith(';'):
                tokens = re.findall(r'F([\d.]+)', line.upper())
                for token in tokens:
                    speed_values[current_layer].append(float(token))
    return speed_values

def calculate_speed_change(speed_per_layer):
    speed_change_per_layer = defaultdict(list)
    for layer, speeds in speed_per_layer.items():
        for i in range(1, len(speeds)):
            speed_change = speeds[i] - speeds[i - 1]
            speed_change_per_layer[layer].append(speed_change)
    return speed_change_per_layer

def write_to_csv(speed_per_layer, speed_change_per_layer):
    with open('Extrusion_Speed_Per_Layer.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Layer", "Average Extrusion Speed", "Speed Change"])
        for layer, speeds in speed_per_layer.items():
            avg_speed = sum(speeds) / len(speeds)
            speed_change = sum(speed_change_per_layer[layer]) / len(speed_change_per_layer[layer]) if layer in speed_change_per_layer else 0.0
            writer.writerow([layer, avg_speed, speed_change])

def main():
    folder_path = r"C:\Users\traee\Downloads\Senior Project\Edited Gcodes\Edited Gcodes"  
    speed_per_layer = defaultdict(list)
    for filename in os.listdir(folder_path):
        if filename.endswith(".gcode"):
            file_path = os.path.join(folder_path, filename)
            speed_values = parse_gcode(file_path, speed_per_layer)
            for layer, values in speed_values.items():
                speed_per_layer[layer].extend(values)
        
    speed_change_per_layer = calculate_speed_change(speed_per_layer)
    
    print("Parsing complete.")
    write_to_csv(speed_per_layer, speed_change_per_layer)
    print("Average extrusion speeds per layer with speed change written to Extrusion_Speed_Per_Layer.csv")

if __name__ == "__main__":
    main()
