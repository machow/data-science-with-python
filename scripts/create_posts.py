import sys

from pathlib import Path

IN_FILE = "curriculum"

out_path = Path("_website") / IN_FILE

all_files = Path(IN_FILE).glob("*.md")
for p in all_files:
    out_file = out_path / (p.name)
    out_file.write_text(p.read_text())
    
