# 🔍 PCB Edge Inspection AI

AI-powered PCB visual inspection using YOLO11, live USB camera, Gerber mapping, operator guidance, and inspection history.

## 🎯 Objectives
- Automate PCB visual inspection
- Detect PCB defects with YOLO11
- Provide PASS/FAIL inspection support
- Map detections to Gerber geometry
- Maintain inspection history

## 🚀 Features
- 🤖 YOLO11 defect detection
- ⚡ CUDA/GPU inference
- 📷 Live USB camera inspection
- ✅ PASS/FAIL decision
- 📐 Gerber geometry integration
- 🗺️ Camera-to-Gerber coordinate mapping
- 👷 Operator guidance
- 📋 Inspection history and CSV logging
- 🎛️ Streamlit dashboard
- ⚙️ FastAPI inspection API

## 🧪 Detected Defects
The current DeepPCB-trained model supports:
- Open
- Short
- Mousebite
- Spur
- Copper
- Pin-hole

## 🛠️ Technology Stack
- Python 3.11
- YOLO11
- PyTorch
- CUDA
- OpenCV
- FastAPI
- Uvicorn
- Streamlit
- Pandas
- NumPy
- Gerbonara

## 🔄 Architecture

USB Camera → FastAPI → YOLO11 → Defect Detection → Camera Coordinates → Gerber Mapping → Operator Guidance → PASS/FAIL → Inspection History → Dashboard

## ▶️ Run

Activate the environment and start the API:

    .venv\Scripts\activate
    python -m uvicorn live_api:app --host 127.0.0.1 --port 8001

Start the dashboard in another terminal:

    streamlit run dashboard_final.py --server.port 8507

Open:

    http://localhost:8507

## ⚠️ Current Limitations
- Physical camera-to-Gerber calibration still requires validation against the corresponding PCB.
- The current detector covers the six DeepPCB classes listed above.
- Additional SMT defects require suitable labeled training data.
- Live predictions require physical validation before being treated as confirmed defects.

## 📊 Status

**Software MVP: Functional**

The system provides an end-to-end workflow from live camera input through YOLO11 detection, Gerber coordinate mapping, operator guidance, PASS/FAIL decision, and inspection history.

## 🔮 Future Scope
- Real camera-to-Gerber calibration
- Additional SMT defect datasets
- Missing-component detection
- Component alignment inspection
- Solder-bridge detection
- Solder-paste inspection
- Production-line integration
- Edge-device deployment

## 👨‍💻 Author

**Sumit Kumar**

⭐ If you find this project useful, consider starring the repository.
