import streamlit as st
import requests
from pathlib import Path

st.set_page_config(page_title="PCB Gerber Inspection",layout="wide")
st.title("PCB Gerber Reference Inspection")
st.caption("Live YOLO11 defects mapped to the Gerber reference")
API="http://localhost:8001/inspect"
GERBER=Path("data/reference/pcb_top_reference.svg")
if not GERBER.exists():
    st.error("Gerber reference not found")
    st.stop()
if st.button("Run Gerber Inspection",type="primary"):
    try:
        response=requests.get(API,timeout=15)
        response.raise_for_status()
        data=response.json()
        c1,c2=st.columns(2)
        c1.metric("Inspection Status",data.get("status","UNKNOWN"))
        c2.metric("Defects",data.get("count",0))
        st.subheader("PCB Gerber Reference")
        svg=GERBER.read_text(encoding="utf-8")
        st.components.v1.html(svg,height=600,scrolling=True)
        defects=data.get("defects",[])
        if defects:
            st.subheader("Gerber Defect Locations")
            for i,d in enumerate(defects,1):
                st.markdown("### "+str(i)+". "+str(d.get("defect")))
                st.write("Confidence: "+str(round(d.get("confidence",0)*100,1))+"%")
                st.write("Camera: ("+str(d.get("camera_x"))+", "+str(d.get("camera_y"))+")")
                st.write("Gerber: ("+str(d.get("gerber_x"))+", "+str(d.get("gerber_y"))+")")
                st.info(d.get("operator_guidance","Inspect the detected region."))
        else:
            st.success("No defects detected in the current camera frame.")
        st.caption("Gerber coordinates currently use a synthetic software transform. Physical calibration requires the matching PCB and camera calibration.")
    except Exception as e:
        st.error("Inspection failed: "+str(e))