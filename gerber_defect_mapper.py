import cv2,numpy as np,json
from pathlib import Path
ROOT=Path(__file__).parent
REF=ROOT/"data/reference/pcb_outline.json"
g=json.loads(REF.read_text())
h=np.array(g["convex_hull"],np.float32)
mn=h.min(0); mx=h.max(0)
gerber=np.float32([[mn[0],mn[1]],[mx[0],mn[1]],[mx[0],mx[1]],[mn[0],mx[1]]])
camera=np.float32([[120,100],[1120,100],[1120,650],[120,650]])
H=cv2.getPerspectiveTransform(camera,gerber)
def pixel_to_gerber(x,y):
    q=np.float32([[[x,y]]])
    r=cv2.perspectiveTransform(q,H)[0,0]
    return float(r[0]),float(r[1])
if __name__=="__main__":
    for name,x,y in [("TEST_CENTER",620,375),("TEST_TOP_LEFT",120,100),("TEST_BOTTOM_RIGHT",1120,650)]:
        gx,gy=pixel_to_gerber(x,y)
        print(name,"CAMERA:",(x,y),"GERBER:",(round(gx,6),round(gy,6)))
