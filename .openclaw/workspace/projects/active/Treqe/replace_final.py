import re
import sys

with open('index.html', 'rb') as f:
    data = f.read()
try:
    content = data.decode('utf-8')
except UnicodeDecodeError:
    content = data.decode('latin-1')

# Pattern to match the div tag with any attributes and content until closing div
# This regex is greedy but works for our case
pattern = r'<div\s+class="girl-skate-img"\s*>[^<]*</div>'
new_content = re.sub(pattern, '<img class="girl-skate-img" src="treqe-girl-skate-real.png" alt="Niña con Skate">', content)

if new_content == content:
    # Try with escaped quotes
    pattern2 = r'<div\s+class=\\"girl-skate-img\\"\s*>[^<]*</div>'
    new_content = re.sub(pattern2, '<img class="girl-skate-img" src="treqe-girl-skate-real.png" alt="Niña con Skate">', content)
    if new_content == content:
        print("No replacement made")
        sys.exit(1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Replacement successful")