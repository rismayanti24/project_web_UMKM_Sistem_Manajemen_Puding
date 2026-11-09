import re

with open(r'karyawan\pesanan.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all occurrences of backticks with their line numbers
lines = content.split('\n')
for idx, line in enumerate(lines):
    if '`' in line:
        print(f"Line {idx+1}: {line.strip()}")
