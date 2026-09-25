from pathlib import Path
p=Path("dashboard_live.py")
s=p.read_text()
s=s.replace("st.caption("Gerber coordinates currently use a synthetic software transform. Physical calibration requires the matching PCB and camera calibration.")", "st.caption("Gerber coordinates currently use a synthetic software transform. Physical calibration requires the matching PCB and camera calibration.")")
p.write_text(s)
print("DASHBOARD CHECKED")