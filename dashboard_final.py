import streamlit as st
import requests
import pandas as pd
from pathlib import Path
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="PCB Edge Inspection System",layout="wide")
st.title("PCB Edge Inspection System")
st.caption("YOLO11 + Live Camera + Gerber Mapping + Operator Guidance + Inspection History")

API="http://localhost:8001/inspect"
VISUAL="http://localhost:8002/visual-inspect"
HISTORY=Path("runs/inspection_reports/inspection_history.csv")

if "inspection" not in st.session_state: st.session_state.inspection=None

if st.button("RUN LIVE INSPECTION",type="primary"):
    try:
        r=requests.get(API,timeout=15)
        r.raise_for_status()
        image=requests.get(VISUAL,timeout=20)
        image.raise_for_status()
        st.session_state.inspection=(r.json(),image.content)
    except Exception as e:
        st.error("Inspection failed: "+str(e))

data=None
image_data=None
if st.session_state.inspection:
    data,image_data=st.session_state.inspection

if data:
    defects=data.get("defects",[])
    c1,c2,c3,c4=st.columns(4)
    c1.metric("STATUS",data.get("status","UNKNOWN"))
    c2.metric("DEFECTS",data.get("count",0))
    c3.metric("FRAME",str(data.get("frame_width"))+" x "+str(data.get("frame_height")))
    c4.metric("INSPECTIONS",len(pd.read_csv(HISTORY)) if HISTORY.exists() else 0)
    st.divider()
    left,right=st.columns(2)
    with left:
        st.subheader("Live Camera")
        st.image(Image.open(BytesIO(image_data)),width="stretch")
    with right:
        st.subheader("Gerber Coordinates")
        if defects:
            rows=[]
            for d in defects:
                rows.append({"Defect":d.get("defect"),"Confidence":str(round(float(d.get("confidence",0))*100,1))+"%","Camera X":d.get("camera_x"),"Camera Y":d.get("camera_y"),"Gerber X":d.get("gerber_x"),"Gerber Y":d.get("gerber_y")})
            st.table(pd.DataFrame(rows))
        else:
            st.success("No defects detected.")
    if defects:
        st.subheader("Operator Guidance")
        for i,d in enumerate(defects,1):
            st.markdown("**"+str(i)+". "+str(d.get("defect"))+" - "+str(round(float(d.get("confidence",0))*100,1))+"%**")
            st.info(d.get("operator_guidance","Inspect the detected region."))
    st.caption("Gerber coordinates use the current synthetic software transform until physical camera calibration is performed.")

if HISTORY.exists():
    st.divider()
    st.subheader("Inspection History")
    hist=pd.read_csv(HISTORY)
    real=hist[hist["status"].isin(["PASS","FAIL"])]
    a,b,c,d=st.columns(4)
    a.metric("Total",len(real))
    b.metric("PASS",int((real["status"]=="PASS").sum()))
    c.metric("FAIL",int((real["status"]=="FAIL").sum()))
    d.metric("Defects",int((real["defect"]!="NONE").sum()))
    counts=real[real["defect"]!="NONE"]["defect"].value_counts()
    if len(counts)>0:
        st.bar_chart(counts)
    st.dataframe(real.sort_values("timestamp",ascending=False).head(20),width="stretch")
    st.download_button("DOWNLOAD INSPECTION HISTORY",data=HISTORY.read_bytes(),file_name="inspection_history.csv",mime="text/csv")
else:
    st.info("No inspection history available yet.")


