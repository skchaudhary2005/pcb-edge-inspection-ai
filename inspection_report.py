import csv,json
from pathlib import Path
from datetime import datetime
OUT=Path("runs/inspection_reports"); OUT.mkdir(parents=True,exist_ok=True)
def save_report(defects,status="FAIL"):
    ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    f=OUT/("inspection_"+datetime.now().strftime("%Y%m%d_%H%M%S")+".csv")
    with f.open("w",newline="",encoding="utf-8") as h:
        w=csv.writer(h); w.writerow(["timestamp","status","defect","confidence","camera_x","camera_y","gerber_x","gerber_y"])
        for d in defects: w.writerow([ts,status,d.get("defect"),d.get("confidence"),d.get("camera_x"),d.get("camera_y"),d.get("gerber_x"),d.get("gerber_y")])
    print("INSPECTION REPORT:",f.resolve())
if __name__=="__main__":
    from ultralytics import YOLO
    import cv2
    model=YOLO("runs/detect/runs/pcb_defect_detector-3/weights/best.pt")
    image=Path("runs/live_inspection/inspection_20260925_213325.jpg")
    frame=cv2.imread(str(image))
    result=model.predict(frame,imgsz=640,conf=0.25,device=0,verbose=False)[0]
    defects=[]
    for b in result.boxes:
        x1,y1,x2,y2=b.xyxy[0].tolist(); cx=(x1+x2)/2; cy=(y1+y2)/2
        cls=int(b.cls[0]); conf=float(b.conf[0]); name=model.names[cls]
        gx=1.925+(cx/frame.shape[1])*(5.29508-1.925); gy=2.0+(cy/frame.shape[0])*(4.12599-2.0)
        defects.append({"defect":name,"confidence":round(conf,4),"camera_x":round(cx,2),"camera_y":round(cy,2),"gerber_x":round(gx,6),"gerber_y":round(gy,6)})
    save_report(defects,"FAIL" if defects else "PASS")
