import streamlit as st
import requests
import pandas as pd
import time
st.set_page_config(page_title="PCB Edge Inspection",layout="wide")
st.title("PCB Edge Inspection - Live")
st.caption("FastAPI + YOLO11 Live Inspection")
API="http://localhost:8001/inspect"
if st.button("Run Live Inspection",type="primary"):
    try:
        r=requests.get(API,timeout=15); data=r.json()
        c1,c2,c3=st.columns(3)
        c1.metric("Status",data.get("status","UNKNOWN"))
        c2.metric("Defects",data.get("count",0))
        c3.metric("Timestamp",data.get("timestamp",0))
        defects=data.get("defects",[])
        if defects:
            st.subheader("Detected Defects")
            st.dataframe(pd.DataFrame(defects),width="stretch")
        else:
            st.success("No defects detected in the current camera frame.")
    except Exception as e:
        st.error("API connection failed: "+str(e))
st.divider()
st.info("FastAPI endpoint: http://localhost:8001/inspect")