import streamlit as st
import requests
import pandas as pd
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="PCB Edge Inspection - Visual",layout="wide")
st.title("PCB Edge Inspection - Visual")
st.caption("YOLO11 + FastAPI + Gerber Mapping + Operator Guidance")

API="http://localhost:8001/inspect"
IMAGE_API="http://localhost:8002/visual-inspect"

if st.button("Run Live Inspection",type="primary"):
    try:
        r=requests.get(API,timeout=15)
        r.raise_for_status()
        data=r.json()
        image_response=requests.get(IMAGE_API,timeout=20)
        image_response.raise_for_status()

        c1,c2,c3=st.columns(3)
        c1.metric("Status",data.get("status","UNKNOWN"))
        c2.metric("Defects",data.get("count",0))
        c3.metric("Frame",str(data.get("frame_width","-"))+" x "+str(data.get("frame_height","-")))

        st.subheader("Live Camera Inspection")
        image=Image.open(BytesIO(image_response.content))
        st.image(image,width="stretch")

        defects=data.get("defects",[])
        if defects:
            st.subheader("Detected Defects")
            rows=[]
            for d in defects:
                rows.append({"Defect":d.get("defect"),"Confidence":str(round(d.get("confidence",0)*100,1))+"%","Camera X":d.get("camera_x"),"Camera Y":d.get("camera_y"),"Gerber X":d.get("gerber_x"),"Gerber Y":d.get("gerber_y")})
            st.dataframe(pd.DataFrame(rows),width="stretch")

            st.subheader("Operator Guidance")
            for i,d in enumerate(defects,1):
                st.markdown("**"+str(i)+". "+str(d.get("defect"))+" - "+str(round(d.get("confidence",0)*100,1))+"%**")
                st.write("Camera: ("+str(d.get("camera_x"))+", "+str(d.get("camera_y"))+")   Gerber: ("+str(d.get("gerber_x"))+", "+str(d.get("gerber_y"))+")")
                st.info(d.get("operator_guidance","Inspect the detected region."))
        else:
            st.success("No defects detected in the current camera frame.")

        st.caption("Gerber coordinates currently use a synthetic software transform. Physical calibration requires the matching PCB and camera calibration.")
    except Exception as e:
        st.error("Live inspection failed: "+str(e))

st.divider()
st.info("FastAPI: http://localhost:8001/inspect    Visual API: http://localhost:8002/visual-inspect")