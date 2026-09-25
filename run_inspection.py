from ultralytics import YOLO
from pathlib import Path
from datetime import datetime
import cv2,csv,json
import numpy as np
ROOT=Path(__file__).parent
MODEL=ROOT/"runs/detect/runs/pcb_defect_detector-3/weights/best.pt"
REF=ROOT/"data/reference/pcb_outline.json"
OUT=ROOT/"runs/inspection_reports"; OUT.mkdir(parents=True,exist_ok=True)
g=json.loads(REF.read_text(encoding="utf-8")); h=np.array(g["convex_hull"],np.float32); mn=h.min(0); mx=h.max(0)
GERBER=np.float32([[mn[0],mn[1]],[mx[0],mn[1]],[mx[0],mx[1]],[mn[0],mx[1]]])
CAMERA=np.float32([[120,100],[1120,100],[1120,650],[120,650]])
H=cv2.getPerspectiveTransform(CAMERA,GERBER)
model=YOLO(str(MODEL)); files=sorted((ROOT/"data/yolo/images/test").glob("*.jpg")); image=files[0] if files else None; frame=cv2.imread(str(image)) if image else None
if frame is None: raise SystemExit("No saved inspection image found in runs/live_inspection")
r=model.predict(frame,imgsz=640,conf=0.25,device=0,verbose=False)[0]
ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S"); rows=[]
for b in r.boxes:
 x1,y1,x2,y2=b.xyxy[0].tolist(); cx=(x1+x2)/2; cy=(y1+y2)/2; q=cv2.perspectiveTransform(np.float32([[[cx,cy]]]),H)[0,0]; rows.append([ts,"FAIL",model.names[int(b.cls[0])],round(float(b.conf[0]),4),round(cx,2),round(cy,2),round(float(q[0]),6),round(float(q[1]),6)])
f=OUT/("integrated_"+datetime.now().strftime("%Y%m%d_%H%M%S")+".csv")
with f.open("w",newline="",encoding="utf-8") as z:
 w=csv.writer(z); w.writerow(["timestamp","status","defect","confidence","camera_x","camera_y","gerber_x","gerber_y"]); w.writerows(rows)
print("INTEGRATED INSPECTION: READY"); print("TEST DEFECT IMAGE:",image); print("DETECTIONS:",len(rows)); print("REPORT:",f.resolve())