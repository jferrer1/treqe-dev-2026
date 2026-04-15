import re
import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find the div with class girl-skate-img and its content
pattern = r'<div class="girl-skate-img">[^<]*</div>'
# Replace with img tag
new_content = re.sub(pattern, '<img class="girl-skate-img" src="treqe-girl-skate-real.png" alt="Niña con Skate">', content)

if new_content == content:
    print("No replacement made")
    sys.exit(1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Replacement successful")