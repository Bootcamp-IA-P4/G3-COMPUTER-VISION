import os
import pandas as pd
import glob

def merge_csv_by_folder_type(base_folders, folder_type):
    """
    Merge CSV files from multiple folders of the same type (train/test/valid)
    
    Args:
        base_folders (list): List of base folder paths
        folder_type (str): 'train', 'test', or 'valid'
    """
    all_csvs = []
    
    # Find all CSV files in the specified folder type
    for base_folder in base_folders:
        folder_path = os.path.join(base_folder, folder_type)
        if os.path.exists(folder_path):
            csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
            all_csvs.extend(csv_files)
    
    if not all_csvs:
        print(f"No CSV files found in {folder_type} folders")
        return
    
    # Read and concatenate all CSV files
    dfs = []
    for csv_file in all_csvs:
        df = pd.read_csv(csv_file)
        dfs.append(df)
    
    # Merge all dataframes
    merged_df = pd.concat(dfs, ignore_index=True)
    
    # Save merged CSV
    output_filename = f"merged_{folder_type}.csv"
    merged_df.to_csv(output_filename, index=False)
    print(f"Created {output_filename} with {len(merged_df)} rows")

# Example usage
base_folders = [
    r"C:\Users\Usuario\OneDrive\IA\Scripts\Repos\G3-COMPUTER-VISION\Brand Logos.v1i.multiclass",
    r"C:\Users\Usuario\OneDrive\IA\Scripts\Repos\G3-COMPUTER-VISION\BrandLogoDetection.v6i.multiclass",
    r"C:\Users\Usuario\OneDrive\IA\Scripts\Repos\G3-COMPUTER-VISION\logo_detect_ v3.v1i.multiclass"
]

# Merge CSVs for each type
for folder_type in ["train", "test", "valid"]:
    merge_csv_by_folder_type(base_folders, folder_type)