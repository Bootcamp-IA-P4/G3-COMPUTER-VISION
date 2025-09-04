import yaml

def deep_merge(dict1, dict2):
    """
    Función recursiva para fusionar diccionarios de manera profunda
    """
    merged = dict1.copy()
    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = deep_merge(merged[key], value)
        elif key in merged and isinstance(merged[key], list) and isinstance(value, list):
            merged[key] = merged[key] + value
        else:
            merged[key] = value
    return merged

def merge_yaml_files(file1_path, file2_path, output_path):
    # Read first YAML file
    with open(file1_path, 'r', encoding='utf-8') as f1:
        yaml1 = yaml.safe_load(f1)
    
    # Read second YAML file
    with open(file2_path, 'r', encoding='utf-8') as f2:
        yaml2 = yaml.safe_load(f2)
    
    # Merge the two dictionaries using deep merge
    merged_yaml = deep_merge(yaml1, yaml2)
    
    # Write the merged content to a new file
    with open(output_path, 'w', encoding='utf-8') as outfile:
        yaml.dump(merged_yaml, outfile, default_flow_style=False, allow_unicode=True, sort_keys=False)

# Example usage:
merge_yaml_files('C:/Users/Usuario/OneDrive/IA/Scripts/Repos/G3-COMPUTER-VISION/BrandLogoDetection.v6i.yolov8/data.yaml', 
                'C:/Users/Usuario/OneDrive/IA/Scripts/Repos/G3-COMPUTER-VISION/logo_detect_ v3.v1i.yolov8/data.yaml', 
                'merged.yaml')