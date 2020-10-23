from pathlib import Path
from string import Template

class CustomTemplate(Template):
    delimiter = '{{'
    pattern = r'''
    \{\{(?:
    (?P<escaped>\{\{)|
    (?P<named>[_a-z][_a-z0-9]*)\}\}|
    (?P<braced>[_a-z][_a-z0-9]*)\}\}|
    (?P<invalid>)
    )
    '''

def load_template():
    template = Path(__file__).parent.parent / "_template" / "index.html"
    return CustomTemplate(template.read_text())

def fetch_records():
    import re
    import yaml
    
    import pandas as pd

    YAML_HEADER = "^---\n(.*?)(\n---)"
    
    records = []
    for p in Path("curriculum").glob("*"):
        m = re.match(YAML_HEADER, p.read_text(), flags = re.MULTILINE | re.DOTALL)
        records.append(yaml.safe_load(m.group(1)))
    
    curriculum = pd.DataFrame(records).sort_values("id")
    
    curriculum.to_csv("curriculum.csv")
    
