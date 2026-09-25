import cv2,json,numpy as np
from pathlib import Path
ROOT=Path(__file__).parent
REF=ROOT/"data/reference/pcb_outline.json"
g=json.loads(REF.read_text())
p=np.array(g["convex_hull"],np.float32)
mn=p.min(0); mx=p.max(0)
gerber=np.float32([[mn[0],mn[1]],[mx[0],mn[1]],[mx[0],mx[1]],[mn[0],mx[1]]])
camera=np.float32([[120,100],[1120,100],[1120,650],[120,650]])
H=cv2.getPerspectiveTransform(camera,gerber)
Hinv=cv2.getPerspectiveTransform(gerber,camera)
t=np.float32([[[620,375]]])
m=cv2.perspectiveTransform(t,H)
b=cv2.perspectiveTransform(m,Hinv)
err=float(np.max(np.abs(b-t)))
print("GERBER ALIGNMENT: READY")
print("BOARD:",float(mx[0]-mn[0]),"x",float(mx[1]-mn[1]),"in")
print("ROUNDTRIP ERROR:",err,"px")
