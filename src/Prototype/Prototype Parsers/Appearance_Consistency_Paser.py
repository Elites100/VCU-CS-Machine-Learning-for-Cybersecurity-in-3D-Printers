import csv

def read_gcode_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        
        # Declare Variable
        layer = '0'
        
        x_count = 0
        y_count = 0
        e_count = 0
        z_count = 0
        f_count = 0
        m82_count = 0
        g92_count = 0
        g280_count = 0
        g0_count = 0
        g1_count = 0
        m106_count = 0
        m204_count = 0
        m205_count = 0
        m104_count = 0
        m107_count = 0
        g91_count = 0
        t1_count = 0
        g90_count = 0
        s0_count = 0
        g11_count = 0
        g10_count = 0
        m109_count = 0

        #Write Header
        csv_writer.writerow(['Layer', 'X Count', 'Y Count', 'E Count', 'Z Count', 'F Count',
                             'M82 Count', 'G92 Count', 'G280 Count', 'G0 Count', 'G1 Count',
                             'M106 Count', 'M204 Count', 'M205 Count', 'M104 Count', 'M107 Count',
                             'G91 Count', 'T1 Count', 'G90 Count', 'S0 Count', 'G11 Count',
                             'G10 Count', 'M109 Count'])
        
        for line in input_file:
            
            # Check for New Layer or else skip
            if not line:
                continue
            elif line.startswith(';LAYER:'):
                layer = line.strip().split(':')[-1]
            elif line.startswith(';'):
                continue
            
            x_count = line.count('X')
            y_count = line.count('Y')
            e_count = line.count('E')
            z_count = line.count('Z')
            f_count = line.count('F')
            m82_count = line.count('M82')
            g92_count = line.count('G92')
            g280_count = line.count('G280')
            g0_count = line.count('G0')
            g1_count = line.count('G1')
            m106_count = line.count('M106')
            m204_count = line.count('M204')
            m205_count = line.count('M205')
            m104_count = line.count('M104')
            m107_count = line.count('M107')
            g91_count = line.count('G91')
            t1_count = line.count('T1')
            g90_count = line.count('G90')
            s0_count = line.count('S0')
            g11_count = line.count('G11')
            g10_count = line.count('G10')
            m109_count = line.count('M109')

            # Write the line to the CSV file
            csv_writer.writerow([layer,x_count, y_count, e_count, z_count, f_count,
                                     m82_count, g92_count, g280_count, g0_count, g1_count,
                                     m106_count, m204_count, m205_count, m104_count, m107_count,
                                     g91_count, t1_count, g90_count, s0_count, g11_count,
                                     g10_count, m109_count])

if __name__ == "__main__":
    GCodeName = 'UM2_Selenite_Polearm_Pose_01_Grid_40_NA_60_0_0_Normal'
    
    input_file_path = r'C:\\Users\\sleep\\OneDrive\\Desktop\\Senior Project\\G-Code\\' +  GCodeName + '.gcode'
    output_file_path = 'Appearance_' + GCodeName + '.csv'
    read_gcode_file(input_file_path, output_file_path)