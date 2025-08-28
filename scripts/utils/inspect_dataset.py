import os
from pathlib import Path
import operator

def analyze_dataset(processed_dir, report_path):
    """
    Analyzes the processed dataset directory to count images per brand
    and generates a sorted report.
    """
    base_path = Path(processed_dir)
    report_file = Path(report_path)
    
    if not base_path.exists() or not base_path.is_dir():
        print(f"Error: Processed directory not found at {base_path}")
        return

    print(f"Analyzing directory: {base_path}")

    brand_counts = {}

    for brand_dir in base_path.iterdir():
        if brand_dir.is_dir():
            image_count = len(list(brand_dir.glob("*.jpg"))) + len(list(brand_dir.glob("*.png")))
            brand_counts[brand_dir.name] = image_count

    # Sort the dictionary by value (image count) in descending order
    sorted_brands = sorted(brand_counts.items(), key=operator.itemgetter(1), reverse=True)

    # Generate the report
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("--- Dataset Analysis Report ---\n\n")
            f.write(f"Total unique brands found: {len(sorted_brands)}\n")
            f.write("-------------------------------------\n")
            f.write("{:<40} | {:<10}\n".format("Brand Name", "Image Count"))
            f.write("-------------------------------------\n")
            
            for brand, count in sorted_brands:
                f.write(f"{brand:<40} | {count:<10}\n")
        
        print(f"\nAnalysis complete.")
        print(f"Report generated at: {report_file}")

    except IOError as e:
        print(f"Error writing report file: {e}")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    
    PROCESSED_DIR = BASE_DIR / "data" / "processed_final"
    REPORT_PATH = BASE_DIR / "analysis_report.txt"
    
    analyze_dataset(PROCESSED_DIR, REPORT_PATH)