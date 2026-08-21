## 🎯 Controls

| Key/Action | Function |
|------------|----------|
| **b** | Capture background (step out of frame first!) |
| **s** | Cycle portal shape (Circle → Hexagon → Star) |
| **1** | Reveal Mode (classic invisibility) |
| **2** | Swirl/Warp distortion |
| **3** | Thermal/Heat-map effect |
| **4** | Pixelate (retro block effect) |
| **5** | Edge detection (neon outline) |
| **6** | Mirror effect |
| **7** | Drain (grayscale) |
| **Pinch Fingers** | Resize portal / Auto-cycle filters |
| **q / Esc** | Quit application |

## 📸 Demo

*Add your demo video/screenshot here!*

## 🧠 Technology Stack

- **OpenCV** - Video capture and image processing
- **MediaPipe** - AI-powered hand landmark detection
- **NumPy** - Numerical operations and array manipulations
- **Python** - Core programming language

## 🔧 How It Works (Technical)

### Hand Landmark Detection
The app uses MediaPipe's pre-trained hand landmarker model to detect 21 keypoints on each hand in real-time.

### Portal Mechanics
- **Index Finger (Landmark #8)**: Portal center position
- **Thumb Tip (Landmark #4)**: Distance calculation for radius
- **Smoothing Algorithm**: Exponential moving average for stable tracking

### Visual Effects
Each filter applies different computer vision techniques:
- **Reveal**: Background subtraction
- **Swirl**: Polar coordinate transformation with radial falloff
- **Thermal**: Grayscale to colormap conversion
- **Pixelate**: Multi-scale resize operations
- **Edge**: Canny edge detection + color mapping
- **Mirror**: Horizontal flip transformation
- **Drain**: RGB to grayscale conversion

## 📂 Project Structure
 ## 🎯 Controls

| Key/Action | Function |
|------------|----------|
| **b** | Capture background (step out of frame first!) |
| **s** | Cycle portal shape (Circle → Hexagon → Star) |
| **1** | Reveal Mode (classic invisibility) |
| **2** | Swirl/Warp distortion |
| **3** | Thermal/Heat-map effect |
| **4** | Pixelate (retro block effect) |
| **5** | Edge detection (neon outline) |
| **6** | Mirror effect |
| **7** | Drain (grayscale) |
| **Pinch Fingers** | Resize portal / Auto-cycle filters |
| **q / Esc** | Quit application |

## 📸 Demo

*Add your demo video/screenshot here!*

## 🧠 Technology Stack

- **OpenCV** - Video capture and image processing
- **MediaPipe** - AI-powered hand landmark detection
- **NumPy** - Numerical operations and array manipulations
- **Python** - Core programming language

## 🔧 How It Works (Technical)

### Hand Landmark Detection
The app uses MediaPipe's pre-trained hand landmarker model to detect 21 keypoints on each hand in real-time.

### Portal Mechanics
- **Index Finger (Landmark #8)**: Portal center position
- **Thumb Tip (Landmark #4)**: Distance calculation for radius
- **Smoothing Algorithm**: Exponential moving average for stable tracking

### Visual Effects
Each filter applies different computer vision techniques:
- **Reveal**: Background subtraction
- **Swirl**: Polar coordinate transformation with radial falloff
- **Thermal**: Grayscale to colormap conversion
- **Pixelate**: Multi-scale resize operations
- **Edge**: Canny edge detection + color mapping
- **Mirror**: Horizontal flip transformation
- **Drain**: RGB to grayscale conversion

## 📂 Project Structure
