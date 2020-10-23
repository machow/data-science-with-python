from pathlib import Path
import re
import yaml

import pandas as pd

YAML_HEADER = "^---\n(.*?)(\n---)"

records = []
for p in Path("curriculum").glob("*"):
    m = re.match(YAML_HEADER, p.read_text(), flags = re.MULTILINE | re.DOTALL)
    entry = yaml.safe_load(m.group(1))
    entry['name'] = p.stem
    records.append(entry)

curriculum = pd.DataFrame(records).sort_values("id")

curriculum.to_csv("curriculum.csv", index = False)
