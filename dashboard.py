import streamlit as st
import pandas as pd
from pathlib import Path
ROOT=Path(__file__).parent
st.set_page_config(page_title="PCB Edge Inspection",layout="wide")
st.title("PCB Edge Inspection System")
reports=sorted((ROOT/"runs/inspection_reports").glob("integrated_*.csv"),key=lambda x:x.stat().st_mtime,reverse=True)
if not reports: st.error("No inspection report found"); st.stop()
df=pd.read_csv(reports[0])
image=ROOT/"runs/inspection_reports/defect_map_00041013.jpg"
c1,c2,c3=st.columns(3)
c1.metric("Inspection Status","FAIL" if len(df)>0 else "PASS")
c2.metric("Total Defects",len(df))
c3.metric("Avg Confidence",f"{df.confidence.mean()*100:.1f}%" if len(df) else "0%")
st.subheader("Defect Map")
if image.exists(): st.image(str(image),width="stretch")
st.subheader("Detected Defects")
st.dataframe(df,width="stretch",hide_index=True)
actions={"open":"Inspect the PCB trace for a broken or disconnected conductor.","short":"Inspect nearby copper tracks for an unintended electrical connection.","mousebite":"Inspect the board edge for an unwanted copper protrusion or routing defect.","spur":"Inspect the copper trace for an unintended branch or copper spur.","copper":"Inspect the copper region for abnormal or unintended copper geometry.","pin-hole":"Inspect the copper feature for a small void or pin-hole defect."}
st.subheader("Operator Guidance")
for _,r in df.iterrows():
 st.write("**"+str(r["defect"]).upper()+"** - Confidence: "+str(round(float(r["confidence"])*100,1))+"% - Gerber X: "+str(r["gerber_x"])+" Y: "+str(r["gerber_y"]))
 st.info(actions.get(str(r["defect"]),"Inspect the detected region against the Gerber reference."))
