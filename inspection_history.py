from pathlib import Path
import csv
from datetime import datetime

FILE=Path("runs/inspection_reports/inspection_history.csv")
FILE.parent.mkdir(parents=True,exist_ok=True)
FIELDS=["timestamp","status","defect","confidence","camera_x","camera_y","gerber_x","gerber_y","operator_guidance"]

def save_inspection(data):
    new=not FILE.exists()
    with FILE.open("a",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS)
        if new: writer.writeheader()
        defects=data.get("defects",[])
        if not defects:
            writer.writerow({"timestamp":datetime.now().isoformat(timespec="seconds"),"status":data.get("status"),"defect":"NONE","confidence":"","camera_x":"","camera_y":"","gerber_x":"","gerber_y":"","operator_guidance":"No defects detected."})
        else:
            for d in defects:
                writer.writerow({"timestamp":datetime.now().isoformat(timespec="seconds"),"status":data.get("status"),"defect":d.get("defect"),"confidence":d.get("confidence"),"camera_x":d.get("camera_x"),"camera_y":d.get("camera_y"),"gerber_x":d.get("gerber_x"),"gerber_y":d.get("gerber_y"),"operator_guidance":d.get("operator_guidance")})
    return FILE