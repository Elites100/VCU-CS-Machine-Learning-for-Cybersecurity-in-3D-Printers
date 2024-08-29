import csv
import re
import os
from collections import defaultdict

def parse_gcode(filename, extrusion_per_layer):
    current_layer = None
    extrusion_values = defaultdict(list)
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith(';LAYER:'):
                current_layer = line.strip().split(':')[-1]
            elif line.strip() and not line.startswith(';'):
                tokens = re.findall(r'E([\d.]+)', line.upper())
                for token in tokens:
                    extrusion_values[current_layer].append(float(token))
    return extrusion_values

def calculate_extrusion_change(extrusion_per_layer):
    extrusion_change_per_layer = defaultdict(list)
    for layer, extrusions in extrusion_per_layer.items():
        for i in range(1, len(extrusions)):
            extrusion_change = extrusions[i] - extrusions[i - 1]
            extrusion_change_per_layer[layer].append(extrusion_change)
    return extrusion_change_per_layer

def write_to_csv(extrusion_per_layer, extrusion_change_per_layer):
    with open('Extrusion_Amount_Per_Layer.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Layer", "Average Extrusion Amount", "Extrusion Change"])
        for layer, extrusions in extrusion_per_layer.items():
            avg_extrusion = sum(extrusions) / len(extrusions)
            extrusion_change = sum(extrusion_change_per_layer[layer]) / len(extrusion_change_per_layer[layer]) if layer in extrusion_change_per_layer else 0.0
            writer.writerow([layer, avg_extrusion, extrusion_change])

def main():
    folder_path = r"C:\Users\traee\Downloads\Senior Project\Edited Gcodes\Edited Gcodes"
    extrusion_per_layer = defaultdict(list)
    for filename in os.listdir(folder_path):
        if filename.endswith(".gcode"):
            file_path = os.path.join(folder_path, filename)
            extrusion_values = parse_gcode(file_path, extrusion_per_layer)
            for layer, values in extrusion_values.items():
                extrusion_per_layer[layer].extend(values)
    
    extrusion_change_per_layer = calculate_extrusion_change(extrusion_per_layer)
    
    print("Parsing complete.")
    write_to_csv(extrusion_per_layer, extrusion_change_per_layer)
    print("Average extrusion amounts per layer with extrusion change written to Extrusion_Amount_Per_Layer.csv")

if __name__ == "__main__":
    main()
