import sys

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

found = False
for i, line in enumerate(lines):
    if 'class="girl-skate-img"' in line:
        # Replace the whole line with img tag
        # Preserve indentation (leading spaces)
        indent = line[:len(line) - len(line.lstrip())]
        lines[i] = indent + '<img class="girl-skate-img" src="treqe-girl-skate-real.png" alt="Niña con Skate">'
        found = True
        break

if not found:
    print('Target line not found')
    sys.exit(1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print('Replacement done')