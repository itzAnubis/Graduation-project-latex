import re

with open("main.tex", "r") as f:
    content = f.read()

# Find all occurrences of TABLE X:
matches = list(re.finditer(r"TABLE\s+(\d+):", content))

for idx, match in enumerate(matches):
    start = match.start()
    # Let's get the 200 characters before and 300 characters after
    snippet = content[max(0, start-100):min(len(content), start+300)]
    print(f"--- MATCH {idx+1} (Table {match.group(1)}) ---")
    print(snippet)
    print("\n" + "="*50 + "\n")
