from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse
from ultralytics import YOLO
import cv2
from pathlib import Path
app=FastAPI(title="PCB Visual Inspection API")
ROOT=Path(__file__).parent
MODEL=ROOT / "runs/detect/runs/pcb_defect_detector-3/weights/best.pt"
model=YOLO(str(MODEL))
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
@app.get("/visual-inspect")
def visual_inspect():
    ok,frame=cap.read()
    if not ok:
        return JSONResponse({"status":"error","message":"Camera frame unavailable"},status_code=503)
    result=model.predict(frame,imgsz=640,conf=0.45,device=0,verbose=False)[0]
    annotated=result.plot()
    ok,jpg=cv2.imencode(".jpg",annotated,[cv2.IMWRITE_JPEG_QUALITY,90])
    if not ok:
        return JSONResponse({"status":"error","message":"JPEG encoding failed"},status_code=500)
    return Response(content=jpg.tobytes(),media_type="image/jpeg")