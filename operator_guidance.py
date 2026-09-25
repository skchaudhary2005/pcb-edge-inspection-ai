import csv
from pathlib import Path
ROOT=Path(__file__).parent
reports=sorted((ROOT/"runs/inspection_reports").glob("integrated_*.csv"),key=lambda x:x.stat().st_mtime,reverse=True)
if not reports: raise SystemExit("No integrated inspection report found")
rows=list(csv.DictReader(reports[0].open(encoding="utf-8")))
actions={"open":"Inspect the PCB trace for a broken or disconnected conductor.","short":"Inspect the nearby copper tracks for an unintended electrical connection.","mousebite":"Inspect the board edge for an unwanted copper protrusion or routing defect.","spur":"Inspect the copper trace for an unintended branch or copper spur.","copper":"Inspect the copper region for abnormal or unintended copper geometry.","pin-hole":"Inspect the copper feature for a small void or pin-hole defect."}
print("OPERATOR GUIDANCE READY")
print("REPORT:",reports[0].resolve())
print("TOTAL DEFECTS:",len(rows))
for i,r in enumerate(rows,1):
 name=r["defect"]; action=actions.get(name,"Inspect the detected region against the Gerber reference."); print("\nDEFECT",i); print("Type:",name); print("Confidence:",r["confidence"]); print("Gerber X:",r["gerber_x"],"Y:",r["gerber_y"]); print("ACTION:",action)
