# PCB Edge Inspection AI

AI-powered PCB visual inspection using YOLO11, live USB camera, Gerber mapping, operator guidance, and inspection history.

## Features

- YOLO11 PCB defect detection
- CUDA/GPU inference
- Live USB camera inspection
- PASS/FAIL decision
- Gerber geometry integration
- Camera-to-Gerber coordinate mapping
- Operator guidance
- Inspection history and CSV logging
- Streamlit dashboard
- FastAPI inspection API

## Detected Defects

The current DeepPCB-trained model supports: open, short, mousebite, spur, copper, and pin-hole.

## Technology Stack

Python 3.11, YOLO11, PyTorch, CUDA, OpenCV, FastAPI, Uvicorn, Streamlit, Pandas, NumPy, Gerbonara.

## Run

Activate the environment:

    .venv\\Scripts\\activate

Start the API:

    python -m uvicorn live_api:app --host 127.0.0.1 --port 8001

Start the dashboard in another terminal:

    streamlit run dashboard_final.py --server.port 8507

Open http://localhost:8507

## Architecture

USB Camera -> FastAPI -> YOLO11 -> Defect Detection -> Camera Coordinates -> Gerber Mapping -> Operator Guidance -> PASS/FAIL -> Inspection History -> Dashboard

## Gerber Mapping

The current camera-to-Gerber transform is a synthetic software/demo transform. Physical camera calibration against the corresponding PCB has not yet been validated.

## Current Limitations

- Physical camera-to-Gerber calibration requires the corresponding PCB.
- Current detector covers the six DeepPCB defect classes listed above.
- Additional SMT-specific defects require suitable labeled training data.
- Live predictions require physical validation before being treated as confirmed PCB defects.

## Status

Software MVP: Functional.

The system provides an end-to-end software workflow from live camera input through YOLO11 detection, Gerber coordinate mapping, operator guidance, PASS/FAIL decision, and inspection history.

## Future Scope

- Real camera-to-Gerber calibration
- Additional SMT defect datasets
- Missing-component detection
- Component alignment inspection
- Solder-bridge detection
- Solder-paste inspection
- Production-line integration
- Edge-device deployment
