from pathlib import Path
import json

ROOT=Path(__file__).parent
SEARCH=[ROOT/"data",ROOT/"gerbers",ROOT/"data"/"gerbers"]
exts={".gbr",".ger",".gtl",".gts",".gbl",".gbs",".gto",".gbo",".gm1",".drl"}
files=[]
for r in SEARCH:
    if r.exists():
        files.extend(x for x in r.rglob("*") if x.is_file() and x.suffix.lower() in exts)
files=sorted(set(files))
print("GERBER FILES FOUND:",len(files))
for f in files[:20]: print(f)
if files:
    print("REFERENCE SOURCE READY")
else:
    print("NO GERBER INPUT YET")
