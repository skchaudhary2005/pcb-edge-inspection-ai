from ultralytics import YOLO
import cv2
import time
import csv
from pathlib import Path

MODEL=Path(r"runs/detect/runs/pcb_defect_detector-3/weights/best.pt")
if not MODEL.exists(): raise SystemExit(f"Model not found: {MODEL.resolve()}")
SAVE_DIR=Path("runs/live_inspection"); SAVE_DIR.mkdir(parents=True,exist_ok=True)
model=YOLO(str(MODEL))
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
if not cap.isOpened(): cap=cv2.VideoCapture(0)
if not cap.isOpened(): raise SystemExit("USB camera could not be opened.")
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280); cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
print("LIVE PCB INSPECTION STARTED")
print("Camera: OK")
print("Model:",MODEL.resolve())
print("Press Q to quit. Press S to save inspection.")
prev=time.perf_counter(); fps=0.0
while True:
    ok,frame=cap.read()
    if not ok: continue
    h,w=frame.shape[:2]; x1,y1=int(w*0.10),int(h*0.10); x2,y2=int(w*0.90),int(h*0.90); roi=frame[y1:y2,x1:x2]; result=model.predict(roi,imgsz=640,conf=0.45,device=0,verbose=False)[0]
    annotated=result.plot()
    detections=[]
    if result.boxes is not None:
        for box in result.boxes:
            cls_id=int(box.cls[0]); conf=float(box.conf[0]); name=model.names.get(cls_id,str(cls_id)); detections.append((name,conf))
    now=time.perf_counter(); dt=now-prev; prev=now
    if dt>0: fps=0.9*fps+0.1*(1.0/dt) if fps else 1.0/dt
    status="FAIL" if detections else "PASS"
    unique={}
    for name,conf in detections: unique[name]=unique.get(name,0)+1
    cv2.rectangle(annotated,(10,10),(600,110),(0,0,0),-1)
    cv2.putText(annotated,f"PCB STATUS: {status}",(25,42),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255) if status=="FAIL" else (0,255,0),2)
    cv2.putText(annotated,f"Defects: {len(detections)}  FPS: {fps:.1f}",(25,72),cv2.FONT_HERSHEY_SIMPLEX,0.65,(255,255,255),2)
    if unique:
        summary=", ".join(f"{k}:{v}" for k,v in unique.items())
        cv2.putText(annotated,summary[:75],(25,98),cv2.FONT_HERSHEY_SIMPLEX,0.48,(255,255,255),1)
    cv2.imshow("PCB Edge Inspection - Live",annotated)
    key=cv2.waitKey(30)&0xFF
    if key==ord("q"): break
    if key==ord("s"):
        filename=SAVE_DIR/f"inspection_{time.strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(str(filename),annotated); print("Saved:",filename.resolve())
cap.release(); cv2.destroyAllWindows(); print("LIVE INSPECTION STOPPED")
