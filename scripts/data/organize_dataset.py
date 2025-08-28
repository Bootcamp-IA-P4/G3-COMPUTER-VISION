import os
import shutil
import re
from pathlib import Path

# MAPA DE MARCAS CANÓNICAS REFINADO
# El orden es importante: las reglas más específicas (ej. 'mercedes-benz') deben ir antes que las más generales (ej. 'mercedes').
BRAND_MAP = {
    # Marcas de coches y relacionadas
    "mercedes-benz": "mercedes-benz", "mercedes": "mercedes-benz", "amg": "mercedes-benz",
    "alfa-romeo": "alfa-romeo",
    "aston-martin": "aston-martin",
    "audi": "audi",
    "bentley": "bentley",
    "bmw": "bmw",
    "bugatti": "bugatti",
    "cadillac": "cadillac",
    "chevrolet": "chevrolet", "chevy": "chevrolet",
    "chrysler": "chrysler",
    "citroen": "citroen",
    "dodge": "dodge", "ram-trucks": "dodge", "mopar": "dodge",
    "ferrari": "ferrari",
    "fiat": "fiat",
    "ford": "ford", "mustang": "ford", "shelby": "ford",
    "honda": "honda",
    "hyundai": "hyundai",
    "jaguar": "jaguar",
    "jeep": "jeep",
    "kia": "kia",
    "lamborghini": "lamborghini",
    "lancia": "lancia",
    "land-rover": "land-rover", "range-rover": "land-rover",
    "lexus": "lexus",
    "maserati": "maserati",
    "mazda": "mazda",
    "mclaren": "mclaren",
    "mini-cooper": "mini-cooper", "mini": "mini-cooper",
    "mitsubishi": "mitsubishi",
    "nissan": "nissan",
    "opel": "opel",
    "peugeot": "peugeot",
    "porsche": "porsche",
    "renault": "renault",
    "rolls-royce": "rolls-royce",
    "saab": "saab",
    "seat": "seat",
    "skoda": "skoda",
    "subaru": "subaru",
    "suzuki": "suzuki",
    "toyota": "toyota",
    "volkswagen": "volkswagen", "vw": "volkswagen",
    "volvo": "volvo",

    # Ropa y Lujo
    "adidas": "adidas",
    "nike": "nike", "jordan": "nike",
    "puma": "puma",
    "reebok": "reebok",
    "under-armour": "under-armour",
    "lacoste": "lacoste",
    "fila": "fila",
    "vans": "vans",
    "converse": "converse",
    "new-balance": "new-balance",
    "asics": "asics",
    "diadora": "diadora",
    "kappa": "kappa",
    "le-coq-sportif": "le-coq-sportif",
    "lotto": "lotto",
    "umbro": "umbro",
    "ralph-lauren": "ralph-lauren", "polo": "ralph-lauren",
    "tommy-hilfiger": "tommy-hilfiger",
    "calvin-klein": "calvin-klein",
    "levi-strauss": "levis", "levis": "levis",
    "gucci": "gucci",
    "prada": "prada",
    "louis-vuitton": "louis-vuitton",
    "hermes": "hermes",
    "chanel": "chanel",
    "dior": "dior",
    "burberry": "burberry",
    "versace": "versace",
    "armani": "armani",
    "zara": "zara",

    # Tecnología
    "apple": "apple", "iphone": "apple", "ipad": "apple", "macbook": "apple", "icloud": "apple",
    "google": "google", "android": "google", "chrome": "google", "gmail": "google", "youtube": "google",
    "microsoft": "microsoft", "windows": "microsoft", "xbox": "microsoft", "office": "microsoft", "azure": "microsoft",
    "amazon": "amazon", "aws": "amazon", "kindle": "amazon", "alexa": "amazon",
    "facebook": "meta", "meta": "meta", "instagram": "meta", "whatsapp": "meta",
    "samsung": "samsung",
    "sony": "sony", "playstation": "sony",
    "intel": "intel",
    "amd": "amd",
    "nvidia": "nvidia",
    "dell": "dell",
    "hp": "hp", "hewlett-packard": "hp",
    "ibm": "ibm",
    "oracle": "oracle",
    "sap": "sap",
    "cisco": "cisco",
    "huawei": "huawei",
    "xiaomi": "xiaomi",
    "nintendo": "nintendo",
    "logitech": "logitech",

    # Comida y Bebida
    "coca-cola": "coca-cola", "coke": "coca-cola",
    "pepsi": "pepsi",
    "mcdonalds": "mcdonalds",
    "burger-king": "burger-king",
    "starbucks": "starbucks",
    "nestle": "nestle",
    "danone": "danone",
    "heineken": "heineken",
    "budweiser": "budweiser",
    "kfc": "kfc",

    # Clubes de Futbol
    "barcelona": "fc-barcelona",
    "real-madrid": "real-madrid",
    "manchester-united": "manchester-united",
    "liverpool": "liverpool-fc",
    "chelsea": "chelsea-fc",
    "arsenal": "arsenal-fc",
    "manchester-city": "manchester-city",
    "juventus": "juventus",
    "inter-milan": "inter-milan", "internazionale": "inter-milan",
    "ac-milan": "ac-milan",
    "bayern-munich": "bayern-munich", "bayern": "bayern-munich",
    "borussia-dortmund": "borussia-dortmund",
    "paris-saint-germain": "paris-saint-germain", "psg": "paris-saint-germain",
    "ajax": "ajax",
    "boca-juniors": "boca-juniors",
    "river-plate": "river-plate",
    "flamengo": "flamengo",
    "corinthians": "corinthians",

    # Otros
    "shell": "shell",
    "esso": "esso",
    "bp": "bp",
    "total": "total",
    "castrol": "castrol",
    "michelin": "michelin",
    "goodyear": "goodyear",
    "pirelli": "pirelli",
    "bridgestone": "bridgestone",
    "continental": "continental",
    "ethereum": "ethereum", "eth": "ethereum",
    "bitcoin": "bitcoin",
}

def clean_brand_name(filename):
    """Cleans a filename to extract a standardized brand name using a refined pipeline."""
    
    name = Path(filename).stem.lower()
    original_name = name # Keep original for fallback

    # 1. Initial cleanup: replace common separators with hyphens
    name = re.sub(r'[\s_.]+', '-', name)

    # 2. Try to match exact canonical names first
    for keyword, canonical_name in BRAND_MAP.items():
        if name == keyword:
            return canonical_name

    # 3. Try to match keywords at the beginning of the name
    for keyword, canonical_name in BRAND_MAP.items():
        if name.startswith(keyword + '-') # e.g., 'adidas-originals' matches 'adidas-'
            return canonical_name

    # 4. More aggressive cleaning for names not yet matched
    # Remove common junk words and patterns that might interfere with matching
    junk_patterns = [
        r'-\d{4}-\d{4}\b',       # e.g., -2000-2015
        r'-\d{4}\b',             # e.g., -2012
        r'_\d+',                 # e.g., _12345
        r'\s*\(.*?\)',           # Remove text in parentheses
        r'\s*\[.*?\]',           # Remove text in brackets
        r'-(logo|vector|download|sign|eps|art|png|jpg|jpeg|black|white|icon|button|racing|team|group|fc|club|sports|auto|motors|company|international|corporation|limited|inc|gmbh|ag|sa|llc|ltd|preview|wordmark|type|design|creative|studio|solutions|systems|technologies|official|original|new|old|v\d+)', # Removed \010
    ]
    for pattern in junk_patterns:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    # Re-apply hyphenation and strip extra hyphens
    name = re.sub(r'[\s_.]+', '-', name)
    name = name.strip('-')
    name = re.sub(r'-+', '-', name)

    # 5. Final check against BRAND_MAP after aggressive cleaning
    for keyword, canonical_name in BRAND_MAP.items():
        if name == keyword or name.startswith(keyword + '-')
            return canonical_name

    # 6. Fallback for names that still don't match a canonical brand
    # If the name is too short, purely numeric, or looks like a hash, discard it.
    if not name or len(name) < 3 or name.isdigit() or re.search(r'^[a-f0-9]{8,}$', name):
        return None
        
    return name

def organize_dataset(source_dir, processed_dir):
    """
    Organizes images and labels from a source directory into a new
    directory structured by brand name.
    """
    source_images_dir = Path(source_dir) / "images"
    source_labels_dir = Path(source_dir) / "labels"
    output_dir = Path(processed_dir)
    
    if not source_images_dir.exists() or not source_labels_dir.exists():
        print("Error: Source directories not found.")
        return

    if output_dir.exists():
        print(f"Clearing existing directory: {output_dir}")
        shutil.rmtree(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print(f"Starting final dataset organization...")
    print(f"Destination: {output_dir}")

    image_files = list(source_images_dir.glob("*.jpg")) + list(source_images_dir.glob("*.png"))
    processed_count = 0
    skipped_count = 0
    brand_folders = set()

    for image_path in image_files:
        brand_name = clean_brand_name(image_path.name)
        
        if not brand_name:
            skipped_count += 1
            continue
            
        brand_dir = output_dir / brand_name
        brand_dir.mkdir(exist_ok=True)
        brand_folders.add(brand_name)
        
        dest_image_path = brand_dir / image_path.name
        
        label_filename = image_path.stem + ".txt"
        source_label_path = source_labels_dir / label_filename
        dest_label_path = brand_dir / label_filename
        
        shutil.copy(image_path, dest_image_path)
        processed_count += 1
        
        if source_label_path.exists():
            shutil.copy(source_label_path, dest_label_path)

    print(f"\nOrganization complete.")
    print(f"Processed images: {processed_count}")
    print(f"Skipped images: {skipped_count}")
    print(f"Unique brands found: {len(brand_folders)}")
    print(f"Processed files are in {output_dir}")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    
    SOURCE_DATASET_DIR = BASE_DIR / "data" / "dataset_yolo"
    PROCESSED_DATASET_DIR_V2 = BASE_DIR / "data" / "dataset_for_training_v2"
    
    organize_dataset(SOURCE_DATASET_DIR, PROCESSED_DATASET_DIR_V2)
