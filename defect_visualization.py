from ultralytics import YOLO
import cv2,json,numpy as np
from pathlib import Path
ROOT=Path(__file__).parent
MODEL=ROOT/"runs/detect/runs/pcb_defect_detector-3/weights/best.pt"
IMG=ROOT/"data/yolo/images/test/00041013_test.jpg"
OUT=ROOT/"runs/inspection_reports/defect_map_00041013.jpg"
g=json.loads((ROOT/"data/reference/pcb_outline.json").read_text())
h=np.array(g["convex_hull"],np.float32); mn=h.min(0); mx=h.max(0)
G=np.float32([[mn[0],mn[1]],[mx[0],mn[1]],[mx[0],mx[1]],[mn[0],mx[1]]]); C=np.float32([[120,100],[1120,100],[1120,650],[120,650]])
H=cv2.getPerspectiveTransform(C,G)
model=YOLO(str(MODEL)); frame=cv2.imread(str(IMG)); result=model.predict(frame,imgsz=640,conf=0.25,device=0,verbose=False)[0]
annotated=result.plot()
for b in result.boxes:
 x1,y1,x2,y2=b.xyxy[0].tolist(); cx=(x1+x2)/2; cy=(y1+y2)/2; q=cv2.perspectiveTransform(np.float32([[[cx,cy]]]),H)[0,0]; name=model.names[int(b.cls[0])]; conf=float(b.conf[0]); label=name+" "+str(round(conf,2))+" G("+str(round(float(q[0]),3))+","+str(round(float(q[1]),3))+")"; cv2.putText(annotated,label,(int(x1),max(20,int(y1)-8)),cv2.FONT_HERSHEY_SIMPLEX,0.45,(0,0,255),1,cv2.LINE_AA)
cv2.imwrite(str(OUT),annotated)
print("DEFECT VISUALIZATION READY")
print("DETECTIONS:",len(result.boxes))
print("OUTPUT:",OUT.resolve())
