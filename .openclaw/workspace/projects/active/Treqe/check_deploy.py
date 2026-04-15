import urllib.request
import sys
import time

def check_url(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            return html
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    preview_url = "https://69d62ca3d8c7b276b4c815a4--sparkling-sawine-898bad.netlify.app"
    live_url = "https://treqe.es"
    
    for name, url in [("preview", preview_url), ("live", live_url)]:
        print(f"Checking {name} ({url})...")
        html = check_url(url)
        if html is None:
            continue
        if 'Lo que tengo' in html and 'Lo que quiero' in html:
            print(f"OK - Buttons found on {name}")
        else:
            print(f"FAIL - Buttons missing on {name}")
        if 'girl-skate-img' in html and 'treqe-girl-skate-real.png' in html:
            print(f"OK - Image reference found on {name}")
        else:
            print(f"FAIL - Image reference missing on {name}")
        # Check for placeholder text
        if 'Niña con Skate' in html or 'Extract PDF Image' in html:
            print(f"WARN - Placeholder text still present on {name}")
        else:
            print(f"OK - No placeholder text on {name}")
        print()

if __name__ == '__main__':
    main()