import os

input_csv_path = os.path.join('data', 'datasets', 'manual_annotation_subset', '_classes.csv')
output_txt_path = os.path.join('data', 'datasets', 'manual_annotation_subset', 'classes.txt')

try:
    with open(input_csv_path, 'r') as f_csv:
        header_line = f_csv.readline().strip()
        class_names = header_line.split(',')

    # Skip the 'filename' header
    if class_names and class_names[0] == 'filename':
        class_names = class_names[1:]

    with open(output_txt_path, 'w') as f_txt:
        for class_name in class_names:
            f_txt.write(class_name.strip() + '\n')
    print(f"Successfully created {output_txt_path} with classes from {input_csv_path}")

except FileNotFoundError:
    print(f"Error: One of the files not found. Make sure '{input_csv_path}' exists.")
except Exception as e:
    print(f"An error occurred: {e}")

