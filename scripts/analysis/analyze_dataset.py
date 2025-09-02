import os
from collections import defaultdict

# --- Configuration ---
DATASET_DIR = 'data/datasets/curated/dataset_v1_yolov8m'
OUTPUT_FILE = 'reports/analysis_report.txt'

def analyze_dataset():
    """
    Analyzes a YOLO dataset to provide statistics on image counts, class distribution,
    and label counts. Writes the analysis to a report file.
    """
    if not os.path.isdir(DATASET_DIR):
        print(f"ERROR: Dataset directory not found at '{DATASET_DIR}'")
        return

    # 1. Read class names from the training set's classes file
    classes_path = os.path.join(DATASET_DIR, 'train', '_classes.csv')
    try:
        with open(classes_path, 'r', encoding='utf-8') as f:
            class_names = [line.strip().split(',')[0] for line in f if line.strip()]
    except FileNotFoundError:
        print(f"ERROR: _classes.csv not found at '{classes_path}'")
        return

    num_classes = len(class_names)
    report_content = []

    report_content.append("=======================================")
    report_content.append("    YOLO Dataset Analysis Report")
    report_content.append("=======================================\n")
    report_content.append(f"Dataset directory: {DATASET_DIR}")
    report_content.append(f"Total number of classes: {num_classes}\n")

    overall_total_files = 0
    overall_total_images = 0
    overall_total_labels = 0

    # --- Analyze each split: train, valid, test ---
    for split in ['train', 'valid', 'test']:
        split_dir = os.path.join(DATASET_DIR, split)
        if not os.path.isdir(split_dir):
            continue

        all_files_in_split = os.listdir(split_dir)
        image_files = {f for f in all_files_in_split if f.lower().endswith(('.jpg', '.jpeg', '.png'))}
        label_files = {f for f in all_files_in_split if f.lower().endswith('.txt')}

        total_files_in_split = len(all_files_in_split)
        num_images = len(image_files)
        num_labels = len(label_files)

        report_content.append(f"--- Analysis for '{split}' set ---")
        report_content.append(f"Total files in folder: {total_files_in_split}")
        report_content.append(f"Number of images: {num_images}")
        report_content.append(f"Number of label files: {num_labels}\n")

        # Check for images without labels
        image_stems = {os.path.splitext(f)[0] for f in image_files}
        label_stems = {os.path.splitext(f)[0] for f in label_files}
        images_without_labels = image_stems - label_stems
        if images_without_labels:
            report_content.append(f"WARNING: Found {len(images_without_labels)} images without corresponding label files.")
            # report_content.append(f"Example: {list(images_without_labels)[:5]}\n")

        # Class distribution analysis
        instances_per_class = defaultdict(int)
        images_per_class = defaultdict(set)

        for label_file in label_files:
            with open(os.path.join(split_dir, label_file), 'r') as f: # Changed label_dir to split_dir
                for line in f:
                    try:
                        class_id = int(line.split()[0])
                        if 0 <= class_id < num_classes:
                            instances_per_class[class_id] += 1
                            images_per_class[class_id].add(os.path.splitext(label_file)[0])
                    except (ValueError, IndexError):
                        continue # Ignore malformed lines
        
        report_content.append("Class Distribution:")
        report_content.append("  {:<20} {:<20} {:<20}".format("Class Name", "Num Images", "Total Instances"))
        report_content.append("  " + "-"*55)
        for i, name in enumerate(class_names):
            num_img_for_class = len(images_per_class.get(i, set()))
            num_instances = instances_per_class.get(i, 0)
            report_content.append(f"  {name:<20} {num_img_for_class:<20} {num_instances:<20}")
        report_content.append("\n")

        overall_total_files += total_files_in_split
        overall_total_images += num_images
        overall_total_labels += num_labels

    # --- Overall Summary ---
    report_content.insert(4, f"Overall total files: {overall_total_files}")
    report_content.insert(5, f"Overall total images: {overall_total_images}")
    report_content.insert(6, f"Overall total label files: {overall_total_labels}\n")

    # --- Write report to file ---
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_content))
        print(f"Successfully created analysis report at '{OUTPUT_FILE}'")
    except IOError as e:
        print(f"ERROR: Could not write report file. Reason: {e}")

if __name__ == '__main__':
    if not os.path.isdir('scripts'):
         print("ERROR: This script must be run from the root of the project directory.")
    else:
        analyze_dataset()
