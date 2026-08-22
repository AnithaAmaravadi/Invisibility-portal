# 🌌 AI Magic Invisibility Portal

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange.svg)](https://google.github.io/mediapipe/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Transform your webcam into a magical portal with AI-powered hand tracking!** Control dynamic portals using natural hand gestures - pinch to resize, touch fingers to switch effects. No special hardware required!

---

## ✨ Features

- ️ **Dual Hand Tracking** - Control up to 2 portals simultaneously with independent gestures
- 🎯 **Intuitive Gesture Control** - Natural hand movements control size, position, and effects
- 🎨 **7 Visual Filters** - Reveal, Swirl, Thermal, Pixelate, Edge, Mirror, and Drain effects
- 🔷 **3 Portal Shapes** - Circle, Hexagon, and Star with animated pulsing glow rings
-  **Real-Time Performance** - Smooth 30+ FPS processing with optimized algorithms
- 📦 **Zero Setup Hassle** - AI model downloads automatically on first run
- 🎬 **Background Capture** - Classic invisibility cloak effect with one-key setup

---
## How to Use

 - **Press 'b'** - Step out of frame and capture the background
 - **Raise your hand** - A portal appears at your index fingertip
 - **Pinch fingers** - Shrink or expand the portal size
 - **Touch fingertips** - Cycle through amazing visual effects!

---
##  Controls

| Key | Action |
|-----|--------|
| **b** | Capture background (step out first!) |
| **s** | Cycle shape: Circle → Hexagon → Star |
| **1** | Reveal (invisibility) |
| **2** | Swirl effect |
| **3** | Thermal effect |
| **4** | Pixelate |
| **5** | Edge detection |
| **6** | Mirror |
| **7** | Grayscale |
| **Pinch** | Resize/Cycle filters |
| **q** | Quit |

---

### ️ Technology Stack

**Core Technologies:**
- **Python:** Core programming language used for application logic, scripting, and real-time processing.
- **OpenCV (cv2):** Advanced computer vision library used for webcam video capture, image processing, masking, and applying visual effects (filters, edge detection, pixelation).
- **MediaPipe:** Google's machine learning framework used for real-time, high-fidelity hand landmark detection (tracking 21 keypoints per hand).
- **NumPy:** High-performance numerical computing library used for array manipulations, matrix operations, and pixel-level image transformations.

**Tools & Platforms:**
- **Git & GitHub:** Version control, code management, and repository hosting.
- **Visual Studio Code (VS Code):** Integrated Development Environment (IDE) for coding and debugging.
- **Windows PowerShell / Terminal:** Command-line interface for virtual environment setup and script execution.

---

## 🎮 Quick Start Guide

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/AnithaAmaravadi/Invisibility-portal.git
cd Invisibility-portal

# 2. Install dependencies
pip install -r requirements.txt  

# 3. Run the application
python invisibility_portal.py
```
## 📂 Project Structure

```text
invisibility-portal/
├── invisibility_portal.py    # Main application (core logic & UI)
├── list_cameras.py           # Utility: detect available camera indices
├── requirements.txt          # Python dependencies (OpenCV, MediaPipe, NumPy)
├── .gitignore                # Git ignore rules (excludes venv, __pycache__)
├── README.md                 # Project documentation
└── hand_landmarker.task      # AI Hand Landmark model (auto-downloaded on first run)
```
 ## 🤝 Contributing
 
  - **Contributions are welcome! Feel free to**
  
  - **Fork the repository**
    
  -  **Create a feature branch**
    
   -  **Submit a pull request**
