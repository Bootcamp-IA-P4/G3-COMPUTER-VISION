
import os
import shutil
import random
from pathlib import Path
import yaml

def split_dataset(source_dir, output_base_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1, random_seed=42):
    """
    Splits the dataset into train, validation, and test sets.

    Args:
        source_dir (Path): Path to the directory containing brand folders (images and labels).
        output_base_dir (Path): Base directory where train/val/test folders will be created.
        train_ratio (float): Proportion of data for the training set.
        val_ratio (float): Proportion of data for the validation set.
        test_ratio (float): Proportion of data for the test set.
        random_seed (int): Seed for reproducibility.
    """
    if not source_dir.exists():
        print(f"Error: Source directory not found at {source_dir}")
        return

    if not (train_ratio + val_ratio + test_ratio) == 1.0:
        print("Error: Train, validation, and test ratios must sum to 1.0")
        return

    random.seed(random_seed)

    # Define output paths
    train_dir = output_base_dir / "train"
    val_dir = output_base_dir / "val"
    test_dir = output_base_dir / "test"

    # Clear and create output directories
    for d in [train_dir, val_dir, test_dir]:
        if d.exists():
            shutil.rmtree(d)
        (d / "images").mkdir(parents=True)
        (d / "labels").mkdir(parents=True)

    print(f"Starting dataset splitting from {source_dir} to {output_base_dir}...")

    class_names = []
    for brand_folder in source_dir.iterdir():
        if brand_folder.is_dir():
            class_name = brand_folder.name
            class_names.append(class_name)

            image_files = list(brand_folder.glob("*.jpg")) + list(brand_folder.glob("*.png"))
            
            # Group images and their corresponding labels
            data_pairs = []
            for img_path in image_files:
                label_path = brand_folder / (img_path.stem + ".txt")
                if label_path.exists():
                    data_pairs.append((img_path, label_path))

            random.shuffle(data_pairs)

            # Calculate split sizes
            total_count = len(data_pairs)
            train_count = int(total_count * train_ratio)
            val_count = int(total_count * val_ratio)
            # Test count takes the rest to ensure all files are used
            test_count = total_count - train_count - val_count

            # Split data
            train_data = data_pairs[:train_count]
            val_data = data_pairs[train_count : train_count + val_count]
            test_data = data_pairs[train_count + val_count :]

            # Copy files to respective directories
            for split_data, target_dir in [
                (train_data, train_dir),
                (val_data, val_dir),
                (test_data, test_dir),
            ]:
                for img_path, label_path in split_data:
                    # Create brand subfolder in target_dir/images and target_dir/labels
                    (target_dir / "images" / class_name).mkdir(parents=True, exist_ok=True)
                    (target_dir / "labels" / class_name).mkdir(parents=True, exist_ok=True)

                    shutil.copy(img_path, target_dir / "images" / class_name / img_path.name)
                    shutil.copy(label_path, target_dir / "labels" / class_name / label_path.name)
    
    print("\nDataset splitting complete.")

    # Generate data.yaml for YOLOv8
    yaml_data = {
        'path': str(output_base_dir.resolve()), # Absolute path to the base directory
        'train': 'train/images',  # Path to training images relative to 'path'
        'val': 'val/images',      # Path to validation images relative to 'path'
        'test': 'test/images',    # Path to test images relative to 'path'
        'names': {i: name for i, name in enumerate(sorted(class_names))}
    }

    yaml_file_path = output_base_dir / f'{output_base_dir.name}.yaml'
    try:
        with open(yaml_file_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)
        print(f"Successfully generated data.yaml at: {yaml_file_path}")
    except IOError as e:
        print(f"Error writing YAML file: {e}")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    
    SOURCE_DATASET_DIR = BASE_DIR / "data" / "dataset_for_training_final_curated"
    OUTPUT_DATASET_DIR = BASE_DIR / "data" / "yolo_training_data"
    
    split_dataset(SOURCE_DATASET_DIR, OUTPUT_DATASET_DIR)
