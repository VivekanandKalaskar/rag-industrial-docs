 # download_docs.py
# Download 50+ free OSHA industrial safety documents

import os
import requests
import time

docs_folder = "C:\D\Rag\documents"
os.makedirs(docs_folder, exist_ok=True)

# OSHA public safety publications — all free, all industrial
osha_docs = [
    ("osha3071.pdf", "https://www.osha.gov/sites/default/files/publications/osha3071.pdf"),
    ("osha3170.pdf", "https://www.osha.gov/sites/default/files/publications/osha3170.pdf"),
    ("osha3173.pdf", "https://www.osha.gov/sites/default/files/publications/osha3173.pdf"),
    ("osha3075.pdf", "https://www.osha.gov/sites/default/files/publications/osha3075.pdf"),
    ("osha3079.pdf", "https://www.osha.gov/sites/default/files/publications/osha3079.pdf"),
    ("osha3080.pdf", "https://www.osha.gov/sites/default/files/publications/osha3080.pdf"),
    ("osha3084.pdf", "https://www.osha.gov/sites/default/files/publications/osha3084.pdf"),
    ("osha3088.pdf", "https://www.osha.gov/sites/default/files/publications/osha3088.pdf"),
    ("osha3089.pdf", "https://www.osha.gov/sites/default/files/publications/osha3089.pdf"),
    ("osha3090.pdf", "https://www.osha.gov/sites/default/files/publications/osha3090.pdf"),
    ("osha3108.pdf", "https://www.osha.gov/sites/default/files/publications/osha3108.pdf"),
    ("osha3120.pdf", "https://www.osha.gov/sites/default/files/publications/osha3120.pdf"),
    ("osha3124.pdf", "https://www.osha.gov/sites/default/files/publications/osha3124.pdf"),
    ("osha3125.pdf", "https://www.osha.gov/sites/default/files/publications/osha3125.pdf"),
    ("osha3128.pdf", "https://www.osha.gov/sites/default/files/publications/osha3128.pdf"),
    ("osha3132.pdf", "https://www.osha.gov/sites/default/files/publications/osha3132.pdf"),
    ("osha3138.pdf", "https://www.osha.gov/sites/default/files/publications/osha3138.pdf"),
    ("osha3140.pdf", "https://www.osha.gov/sites/default/files/publications/osha3140.pdf"),
    ("osha3142.pdf", "https://www.osha.gov/sites/default/files/publications/osha3142.pdf"),
    ("osha3143.pdf", "https://www.osha.gov/sites/default/files/publications/osha3143.pdf"),
    ("osha3146.pdf", "https://www.osha.gov/sites/default/files/publications/osha3146.pdf"),
    ("osha3148.pdf", "https://www.osha.gov/sites/default/files/publications/osha3148.pdf"),
    ("osha3149.pdf", "https://www.osha.gov/sites/default/files/publications/osha3149.pdf"),
    ("osha3150.pdf", "https://www.osha.gov/sites/default/files/publications/osha3150.pdf"),
    ("osha3151.pdf", "https://www.osha.gov/sites/default/files/publications/osha3151.pdf"),
    ("osha3152.pdf", "https://www.osha.gov/sites/default/files/publications/osha3152.pdf"),
    ("osha3155.pdf", "https://www.osha.gov/sites/default/files/publications/osha3155.pdf"),
    ("osha3156.pdf", "https://www.osha.gov/sites/default/files/publications/osha3156.pdf"),
    ("osha3157.pdf", "https://www.osha.gov/sites/default/files/publications/osha3157.pdf"),
    ("osha3158.pdf", "https://www.osha.gov/sites/default/files/publications/osha3158.pdf"),
    ("osha3161.pdf", "https://www.osha.gov/sites/default/files/publications/osha3161.pdf"),
    ("osha3162.pdf", "https://www.osha.gov/sites/default/files/publications/osha3162.pdf"),
    ("osha3163.pdf", "https://www.osha.gov/sites/default/files/publications/osha3163.pdf"),
    ("osha3164.pdf", "https://www.osha.gov/sites/default/files/publications/osha3164.pdf"),
    ("osha3165.pdf", "https://www.osha.gov/sites/default/files/publications/osha3165.pdf"),
    ("osha3168.pdf", "https://www.osha.gov/sites/default/files/publications/osha3168.pdf"),
    ("osha3169.pdf", "https://www.osha.gov/sites/default/files/publications/osha3169.pdf"),
    ("osha3174.pdf", "https://www.osha.gov/sites/default/files/publications/osha3174.pdf"),
    ("osha3176.pdf", "https://www.osha.gov/sites/default/files/publications/osha3176.pdf"),
    ("osha3177.pdf", "https://www.osha.gov/sites/default/files/publications/osha3177.pdf"),
    ("osha3178.pdf", "https://www.osha.gov/sites/default/files/publications/osha3178.pdf"),
    ("osha3179.pdf", "https://www.osha.gov/sites/default/files/publications/osha3179.pdf"),
    ("osha3180.pdf", "https://www.osha.gov/sites/default/files/publications/osha3180.pdf"),
    ("osha3181.pdf", "https://www.osha.gov/sites/default/files/publications/osha3181.pdf"),
    ("osha3182.pdf", "https://www.osha.gov/sites/default/files/publications/osha3182.pdf"),
    ("osha3185.pdf", "https://www.osha.gov/sites/default/files/publications/osha3185.pdf"),
    ("osha3187.pdf", "https://www.osha.gov/sites/default/files/publications/osha3187.pdf"),
    ("osha3188.pdf", "https://www.osha.gov/sites/default/files/publications/osha3188.pdf"),
    ("osha3189.pdf", "https://www.osha.gov/sites/default/files/publications/osha3189.pdf"),
    ("osha3190.pdf", "https://www.osha.gov/sites/default/files/publications/osha3190.pdf"),
    ("osha3192.pdf", "https://www.osha.gov/sites/default/files/publications/osha3192.pdf"),
    ("osha3194.pdf", "https://www.osha.gov/sites/default/files/publications/osha3194.pdf"),
    ("osha3195.pdf", "https://www.osha.gov/sites/default/files/publications/osha3195.pdf"),
]

downloaded = 0
skipped = 0
failed = 0

for filename, url in osha_docs:
    filepath = os.path.join(docs_folder, filename)
    
    # Skip if already downloaded
    if os.path.exists(filepath):
        print(f"  Already have: {filename}")
        skipped += 1
        continue
    
    try:
        print(f"  Downloading: {filename}...", end=" ")
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200 and len(response.content) > 1000:
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"OK ({len(response.content) // 1024} KB)")
            downloaded += 1
        else:
            print(f"SKIP (status {response.status_code})")
            failed += 1
        
        time.sleep(0.5)  # Be polite to OSHA's servers
        
    except Exception as e:
        print(f"FAILED ({e})")
        failed += 1

print(f"\nDone! Downloaded: {downloaded} | Already had: {skipped} | Failed: {failed}")
print(f"Total documents: {len(os.listdir(docs_folder))}")