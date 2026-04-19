 # download_more.py
# Try additional OSHA publication numbers to reach 50+

import os
import requests
import time

docs_folder = "C:\D\Rag\documents"
existing = set(os.listdir(docs_folder))
print(f"Currently have: {len(existing)} documents\n")

# Try a wider range of OSHA publication numbers
numbers = list(range(3200, 3300)) + list(range(3300, 3400)) + list(range(3400, 3500))

downloaded = 0

for num in numbers:
    filename = f"osha{num}.pdf"
    if filename in existing:
        continue
    
    url = f"https://www.osha.gov/sites/default/files/publications/osha{num}.pdf"
    
    try:
        response = requests.get(url, timeout=15)
        
        # Only save if it's a real PDF (not an error page)
        if (response.status_code == 200 
            and len(response.content) > 5000 
            and response.content[:5] == b'%PDF-'):
            
            filepath = os.path.join(docs_folder, filename)
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"  Found: {filename} ({len(response.content) // 1024} KB)")
            downloaded += 1
        
        time.sleep(0.3)
        
    except Exception:
        continue

total = len([f for f in os.listdir(docs_folder) if f.endswith(".pdf")])
print(f"\nNew downloads: {downloaded}")
print(f"Total documents: {total}")