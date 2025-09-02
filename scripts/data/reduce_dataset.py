
import os
import random
import shutil
import argparse

def get_image_files(path):
    images = []
    for f in os.listdir(path):
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            images.append(f)
    return images

def reduce_dataset(source_dir, dest_dir, target_train_size):
    """
    Reduces a YOLO dataset proportionally across train, valid, and test splits.
    """
    print(f"Source directory: {source_dir}")
    print(f"Destination directory: {dest_dir}")
    print(f"Target training set size: {target_train_size}")

    # --- 1. Calculate Reduction Factor ---
    train_images_path = os.path.join(source_dir, 'train', 'images')
    if not os.path.exists(train_images_path):
        print(f"ERROR: Training images folder not found at {train_images_path}")
        return

    original_train_images = get_image_files(train_images_path)
    original_train_size = len(original_train_images)

    if original_train_size == 0:
        print("ERROR: No images found in the training set.")
        return

    reduction_factor = target_train_size / original_train_size
    print(f"Original training set size: {original_train_size}")
    print(f"Reduction factor: {reduction_factor:.4f}")

    # --- 2. Process each split (train, valid, test) ---
    splits = ['train', 'valid', 'test']
    for split in splits:
        print(f"\nProcessing '{split}' split...")
        source_images_path = os.path.join(source_dir, split, 'images')
        source_labels_path = os.path.join(source_dir, split, 'labels')

        if not os.path.exists(source_images_path):
            print(f"Skipping '{split}' split, folder not found.")
            continue

        # Create destination directories
        dest_split_path = os.path.join(dest_dir, split)
        dest_images_path = os.path.join(dest_split_path, 'images')
        dest_labels_path = os.path.join(dest_split_path, 'labels')
        os.makedirs(dest_images_path, exist_ok=True)
        os.makedirs(dest_labels_path, exist_ok=True)

        # Get list of images
        images = get_image_files(source_images_path)
        num_images_to_keep = int(len(images) * reduction_factor)
        print(f"Original images in '{split}': {len(images)}")
        print(f"Images to keep: {num_images_to_keep}")

        # Randomly select images
        selected_images = random.sample(images, num_images_to_keep)

        # Copy selected images and their corresponding labels
        copied_count = 0
        for img_name in selected_images:
            base_name, _ = os.path.splitext(img_name)
            label_name = f"{base_name}.txt"

            source_img_file = os.path.join(source_images_path, img_name)
            source_label_file = os.path.join(source_labels_path, label_name)

            if os.path.exists(source_label_file):
                shutil.copy(source_img_file, dest_images_path)
                shutil.copy(source_label_file, dest_labels_path)
                copied_count += 1
            else:
                print(f"  - Warning: Label file not found for {img_name}, skipping.")
        
        print(f"Successfully copied {copied_count} images and labels to {dest_split_path}")

    # --- 3. Copy the YAML file ---
    source_yaml = os.path.join(source_dir, 'data.yaml')
    dest_yaml = os.path.join(dest_dir, 'data.yaml')
    if os.path.exists(source_yaml):
        shutil.copy(source_yaml, dest_yaml)
        print(f"\nSuccessfully copied 'data.yaml' to {dest_dir}")
    else:
        print(f"\nWarning: 'data.yaml' not found in source directory.")

    print("\nDataset reduction complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reduce YOLO dataset size proportionally.")
    parser.add_argument('--source_dir', type=str, required=True, help='Path to the source dataset directory.')
    parser.add_argument('--dest_dir', type=str, required=True, help='Path to the destination directory for the reduced dataset.')
    parser.add_argument('--target_train_size', type=int, default=1000, help='The target number of images for the training set.')
    
    args = parser.parse_args()
    
    reduce_dataset(args.source_dir, args.dest_dir, args.target_train_size)
