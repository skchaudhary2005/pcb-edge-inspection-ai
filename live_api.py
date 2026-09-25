from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ultralytics import YOLO
from pathlib import Path
from inspection_history import save_inspection
import cv2
import time
app=FastAPI(title="PCB Edge Inspection API")
ROOT=Path(__file__).parent
MODEL=ROOT/"runs/detect/runs/pcb_defect_detector-3/weights/best.pt"
model=YOLO(str(MODEL))
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
GERBER_MIN_X=1.925
GERBER_MIN_Y=2.0
GERBER_MAX_X=5.29508
GERBER_MAX_Y=4.12599
CAM_X1=120.0
CAM_Y1=100.0
CAM_X2=1120.0
CAM_Y2=650.0
GUIDANCE={"open":"Inspect the trace for a broken or disconnected conductor.","short":"Inspect nearby copper tracks for an unintended electrical connection.","mousebite":"Inspect the board edge for an unwanted copper protrusion.","spur":"Inspect the copper trace for an unintended branch or copper spur.","copper":"Inspect the copper region for abnormal or unintended copper geometry.","pin-hole":"Inspect the copper feature for a small void or pin-hole defect."}
def camera_to_gerber(x,y):
    gx=GERBER_MIN_X+(x-CAM_X1)/(CAM_X2-CAM_X1)*(GERBER_MAX_X-GERBER_MIN_X)
    gy=GERBER_MIN_Y+(y-CAM_Y1)/(CAM_Y2-CAM_Y1)*(GERBER_MAX_Y-GERBER_MIN_Y)
    return round(gx,6),round(gy,6)
@app.get("/health")
def health():
    return {"status":"ok","model":str(MODEL),"camera":bool(cap.isOpened()),"gerber_mapping":"synthetic"}
@app.get("/inspect")
def inspect():
    ok,frame=cap.read()
    if not ok: return JSONResponse({"status":"error","message":"Camera frame unavailable"},status_code=503)
    h,w=frame.shape[:2]
    result=model.predict(frame,imgsz=640,conf=0.45,device=0,verbose=False)[0]
    defects=[]
    for b in result.boxes:
        x1,y1,x2,y2=b.xyxy[0].tolist()
        x=round((x1+x2)/2,2); y=round((y1+y2)/2,2)
        name=model.names[int(b.cls[0])]; conf=round(float(b.conf[0]),4)
        gx,gy=camera_to_gerber(x,y)
        defects.append({"defect":name,"confidence":conf,"camera_x":x,"camera_y":y,"gerber_x":gx,"gerber_y":gy,"operator_guidance":GUIDANCE.get(name,"Inspect the detected region and compare it with the PCB reference.")})
    data={"status":"FAIL" if defects else "PASS","defects":defects,"count":len(defects),"frame_width":w,"frame_height":h,"timestamp":time.time(),"gerber_mapping":"synthetic demo transform"}
    save_inspection(data)
    return data
