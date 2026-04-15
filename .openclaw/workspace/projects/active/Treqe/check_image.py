import urllib.request
import sys

def check_image(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = response.read()
            print(f"Image size: {len(data)} bytes")
            if len(data) > 1000:
                print("OK - Image is not placeholder (size > 1KB)")
                return True
            else:
                print("FAIL - Image too small, likely placeholder")
                return False
    except Exception as e:
        print(f"Error fetching image: {e}")
        return False

preview_url = "https://69d62ca3d8c7b276b4c815a4--sparkling-sawine-898bad.netlify.app"
image_url = preview_url + "/treqe-girl-skate-real.png"
print(f"Checking image at {image_url}")
success = check_image(image_url)
sys.exit(0 if success else 1)