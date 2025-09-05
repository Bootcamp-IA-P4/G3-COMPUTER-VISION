import os
import csv
import yaml

# --- Configuration ---
# This script assumes it is run from the root of the project directory.
DATASET_BASE_DIR = 'data/datasets/curated/Dataset_final'
CLASSES_CSV_INPUT_PATH = os.path.join(DATASET_BASE_DIR, 'train', '_classes.csv')
YAML_OUTPUT_PATH = os.path.join(DATASET_BASE_DIR, 'data.yaml')

def generate_yaml():
    """
    Reads the class names from a _classes.csv file and generates a data.yaml
    file suitable for YOLOv8 training.
    """
    # 1. Read class names from the source CSV
    class_names = []
    try:
        with open(CLASSES_CSV_INPUT_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    # Assumes format 'class_name,id' and appends the class name
                    class_names.append(row[0])
        print(f"Successfully read {len(class_names)} classes from {CLASSES_CSV_INPUT_PATH}")
    except FileNotFoundError:
        print(f"ERROR: Input file not found at '{CLASSES_CSV_INPUT_PATH}'")
        print("Please ensure the dataset is in the correct location.")
        return

    # 2. Define the YAML content with relative paths for portability
    # These paths are relative to the location of the YAML file itself.
    yaml_content = {
        'train': 'train/images',
        'val': 'valid/images',
        'test': 'test/images',
        'nc': len(class_names),
        'names': class_names
    }

    # 3. Write the content to the data.yaml file
    try:
        with open(YAML_OUTPUT_PATH, 'w') as f:
            yaml.dump(yaml_content, f, sort_keys=False, default_flow_style=False)
        
        print(f"\nSuccessfully created '{YAML_OUTPUT_PATH}'")
        print("\n--- YAML Content ---")
        print(yaml.dump(yaml_content, sort_keys=False, default_flow_style=False))
        print("\n******************************************************************")
        print("ACTION REQUIRED: Upload the generated 'data.yaml' file to your")
        print(f"'Dataset_final' folder on Google Drive.")
        print("******************************************************************")

    except Exception as e:
        print(f"ERROR: Could not write YAML file. Reason: {e}")

if __name__ == '__main__':
    # A simple check to make sure the script is run from the project root
    if not os.path.isdir('data') or not os.path.isdir('scripts'):
        print("ERROR: This script must be run from the root of the project directory.")
    else:
        generate_yaml()
