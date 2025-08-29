import os
import sys
from pathlib import Path

# Add the parent directory of the current script to the Python path
# so organize_dataset can be imported
script_dir = Path(__file__).resolve().parent
sys.path.append(str(script_dir))

from organize_dataset import organize_dataset

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent.parent # G3-COMPUTER-VISION
    
    SOURCE_DATASET_DIR = BASE_DIR / "data" / "datasets" / "raw" / "team_dataset_v2_raw"
    
    # Output for all brands (threshold = 0)
    PROCESSED_ALL_BRANDS_DIR = BASE_DIR / "data" / "datasets" / "processed" / "team_dataset_all_v2_processed"
    
    # Output for brands with >= 10 images (threshold = 10)
    PROCESSED_10_IMAGES_BRANDS_DIR = BASE_DIR / "data" / "datasets" / "processed" / "team_dataset_10_v2_processed"

    # Ensure output directories exist
    PROCESSED_ALL_BRANDS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_10_IMAGES_BRANDS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"--- Processing for ALL brands (threshold=0) ---")
    organize_dataset(str(SOURCE_DATASET_DIR), str(PROCESSED_ALL_BRANDS_DIR), threshold=0)
    
    print(f"\n--- Processing for brands with >= 10 images (threshold=10) ---")
    organize_dataset(str(SOURCE_DATASET_DIR), str(PROCESSED_10_IMAGES_BRANDS_DIR), threshold=10)

    print("\nDataset processing complete.")