import csv
import os
import random

def read_csv_file(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def display_data(rows):
    for row in rows:
        print(row)

def select_column(data):
    columns = data[0].keys()
    print("Columns available for modification:")
    for i, column in enumerate(columns):
        print(f"{i + 1}. {column}")

    choice = int(input("Select a column to modify (enter number): ")) - 1
    selected_column = list(columns)[choice]
    return selected_column

def modify_column(data, column, selected_rows):
    value_to_replace = input(f"Enter the new value for '{column}': ")
    rows_to_change = [data[index] for index in selected_rows]
    return rows_to_change, value_to_replace

def main():
    folder_path = input("Enter the folder path containing CSV files: ")
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    if not csv_files:
        print("No CSV files found in the specified folder.")
        return

    for csv_file in csv_files:
        print(f"\nCurrently modifying file: {csv_file}")
        filename = os.path.join(folder_path, csv_file)
        data = read_csv_file(filename)

        column = select_column(data)

        # Select a random starting index for consecutive lines
        start_index = random.randint(0, len(data) - 1)
        num_lines_to_change = random.randint(1, min(50, len(data) - start_index))  # limit the upper range to 50
        selected_rows = list(range(start_index, start_index + num_lines_to_change))

        # Display selected lines
        print(f"\nSelected lines from index {start_index} to {start_index + num_lines_to_change - 1}:")
        for index in selected_rows:
            print(data[index])

        print("\n")
            
        rows_to_change, new_value = modify_column(data, column, selected_rows)

        confirm = input("\nDo you want to proceed with the changes? (yes/no): ").lower()
        if confirm in ['yes', 'y']:
            for row in rows_to_change:
                row[column] = new_value
                row["Modified"] = "1"  # Marking the row as modified

            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

            print("Changes saved successfully!")
        else:
            print("No changes were made.")

        next_file = input("\nDo you want to modify another file? (yes/no): ").lower()
        if next_file not in ['yes', 'y']:
            break

if __name__ == "__main__":
    main()
