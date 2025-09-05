
import os
import shutil
from pathlib import Path
import yaml

def create_training_dataset(processed_dir, report_path, final_dataset_dir, yaml_path, threshold):
    """
    Creates the final training dataset by selecting brands that meet the image count threshold
    and generates the corresponding data.yaml file for YOLO.
    """
    processed_path = Path(processed_dir)
    report_file = Path(report_path)
    output_path = Path(final_dataset_dir)
    yaml_file = Path(yaml_path)

    if not report_file.exists():
        print(f"Error: Analysis report not found at {report_file}")
        return

    # 1. Select brands that meet the threshold
    selected_brands = []
    with open(report_file, 'r', encoding='utf-8') as f:
        for line in f:
            if '|' not in line or line.startswith('---') or line.startswith('Brand Name'):
                continue
            
            parts = line.split('|')
            brand_name = parts[0].strip()
            image_count = int(parts[1].strip())
            
            if image_count >= threshold:
                selected_brands.append(brand_name)

    if not selected_brands:
        print(f"No brands found with at least {threshold} images. Nothing to do.")
        return

    print(f"Found {len(selected_brands)} brands with at least {threshold} images.")

    # 2. Create the final dataset directory
    if output_path.exists():
        print(f"Clearing existing final dataset directory: {output_path}")
        shutil.rmtree(output_path)
    output_path.mkdir(exist_ok=True)
    print(f"Created final training directory at: {output_path}")

    # 3. Copy selected brand folders
    for brand in selected_brands:
        source_brand_dir = processed_path / brand
        dest_brand_dir = output_path / brand
        if source_brand_dir.exists():
            shutil.copytree(source_brand_dir, dest_brand_dir)

    print(f"Copied {len(selected_brands)} brand folders to the final directory.")

    # 4. Generate data.yaml file
    yaml_data = {
        'path': f'../{output_path.name}',  # Relative path to the dataset folder
        'train': './', # Assuming all images are for training for now
        'val': './',   # Assuming all images are for validation for now
        'names': {i: name for i, name in enumerate(selected_brands)}
    }

    try:
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)
        print(f"Successfully generated data.yaml at: {yaml_file}")
    except IOError as e:
        print(f"Error writing YAML file: {e}")

if __name__ == "__main__":
    THRESHOLD = 10
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    
    PROCESSED_DIR = BASE_DIR / "data" / "processed_final"
    REPORT_PATH = BASE_DIR / "analysis_report.txt"
    FINAL_DATASET_DIR = BASE_DIR / "data" / "dataset_for_training"
    YAML_PATH = BASE_DIR / "data" / "dataset_for_training.yaml"
    
    create_training_dataset(PROCESSED_DIR, REPORT_PATH, FINAL_DATASET_DIR, YAML_PATH, THRESHOLD)
