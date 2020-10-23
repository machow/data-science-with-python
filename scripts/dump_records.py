import pandas as pd
import yaml
from pathlib import Path

df = pd.read_csv("curriculum.csv").iloc[:,1:]
def filter_nan(x): return {k: v for k,v in x.items() if pd.notna(v)}

l = df.assign(id = range(len(df))).to_dict(orient = "record")

for entry in l: 
    content = "---\n" + yaml.dump(filter_nan(entry)) + "---\n"
    Path("curriculum/%s.md" %entry["name"]).write_text(content) 
