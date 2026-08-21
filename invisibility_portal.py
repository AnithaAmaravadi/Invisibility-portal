"""
AI Magic Invisibility Portal — Dual Hand Edition (FIXED KEY DETECTION)
"""
import os
import time
import math
import urllib.request
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
CAM_INDEX = 0
FRAME_W, FRAME_H = 960, 540
MIN_RADIUS, MAX_RADIUS = 30, 220
SMOOTHING = 0.35          
RING_THICKNESS = 4

MODES = {
    ord('1'): "reveal", ord('2'): "swirl", ord('3'): "thermal",
    ord('4'): "pixelate", ord('5'): "edge", ord('6'): "mirror", ord('7'): "drain",
}
MODE_LIST = list(MODES.values())
SHAPES = ["circle", "hexagon", "star"]

PINCH_TRIGGER_DIST = 15
PINCH_RELEASE_DIST = 35

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hand_landmarker.task")
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task"

def ensure_model():
    if not os.path.exists(MODEL_PATH):
        print("Downloading hand landmark model (one-time, ~7 MB)...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Model downloaded to", MODEL_PATH)

class Portal:
    def __init__(self, color):
        self.color = color
        self.center = None
        self.radius = MIN_RADIUS
        self.active = False

    def update(self, target_center, target_radius):
        if self.center is None:
            self.center = np.array(target_center, dtype=np.float32)
        else:
            self.center += (np.array(target_center, dtype=np.float32) - self.center) * SMOOTHING
        self.radius += (target_radius - self.radius) * SMOOTHING
        self.active = True

    def deactivate(self):
        self.active = False

def landmark_px(landmark, w, h):
    return int(landmark.x * w), int(landmark.y * h)

def hexagon_points(center, radius, rotation=0.0):
    pts = []
    for i in range(6):
        angle = math.radians(60 * i - 30) + rotation
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        pts.append([int(x), int(y)])
    return np.array(pts, dtype=np.int32)

def star_points(center, radius, rotation=0.0):
    pts = []
    outer, inner = radius, radius * 0.45
    for i in range(10):
        r = outer if i % 2 == 0 else inner
        angle = math.radians(36 * i - 90) + rotation
        x = center[0] + r * math.cos(angle)
        y = center[1] + r * math.sin(angle)
        pts.append([int(x), int(y)])
    return np.array(pts, dtype=np.int32)

def draw_shape_mask(mask, shape, center, radius, rotation=0.0):
    if shape == "hexagon":
        cv2.fillPoly(mask, [hexagon_points(center, radius, rotation)], 255)
    elif shape == "star":
        cv2.fillPoly(mask, [star_points(center, radius, rotation)], 255)
    else:
        cv2.circle(mask, center, radius, 255, -1)

def draw_shape_outline(canvas, shape, center, radius, color, thickness, rotation=0.0):
    if shape == "hexagon":
        cv2.polylines(canvas, [hexagon_points(center, radius, rotation)], True, color, thickness, cv2.LINE_AA)
    elif shape == "star":
        cv2.polylines(canvas, [star_points(center, radius, rotation)], True, color, thickness, cv2.LINE_AA)
    else:
        cv2.circle(canvas, center, radius, color, thickness, lineType=cv2.LINE_AA)

def swirl_frame(frame, center, radius, strength=3.2):
    h, w = frame.shape[:2]
    y_idx, x_idx = np.indices((h, w), dtype=np.float32)
    dx = x_idx - center[0]
    dy = y_idx - center[1]
    dist = np.sqrt(dx * dx + dy * dy)
    falloff = np.exp(-(dist / (radius + 1e-5)) ** 2)
    angle = strength * falloff
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    map_x = (center[0] + dx * cos_a - dy * sin_a).astype(np.float32)
    map_y = (center[1] + dx * sin_a + dy * cos_a).astype(np.float32)
    return cv2.remap(frame, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def pixelate_frame(frame, block=18):
    h, w = frame.shape[:2]
    small = cv2.resize(frame, (max(1, w // block), max(1, h // block)), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

def edge_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 60, 150)
    return cv2.applyColorMap(edges, cv2.COLORMAP_COOL)

def build_effect_layer(frame, background, mode, center, radius):
    if mode == "reveal":
        return background if background is not None else frame
    if mode == "swirl":
        return swirl_frame(frame, center, radius)
    if mode == "thermal":
        return cv2.applyColorMap(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLORMAP_INFERNO)
    if mode == "pixelate":
        return pixelate_frame(frame)
    if mode == "edge":
        return edge_frame(frame)
    if mode == "mirror":
        return cv2.flip(frame, 1)
    if mode == "drain":
        return cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    return frame

def composite_mask(base, effect_layer, mask):
    mask_3c = cv2.merge([mask, mask, mask])
    inv_mask_3c = cv2.bitwise_not(mask_3c)
    return cv2.bitwise_and(base, inv_mask_3c) + cv2.bitwise_and(effect_layer, mask_3c)

def draw_glow_ring(canvas, shape, center, radius, color, t, rotation=0.0):
    pulse = 1.0 + 0.06 * math.sin(t * 4)
    r = int(radius * pulse)
    draw_shape_outline(canvas, shape, center, r, color, RING_THICKNESS, rotation)
    draw_shape_outline(canvas, shape, center, int(r * 0.85), color, max(1, RING_THICKNESS - 2), rotation)

def choose_camera(max_index_to_try=6):
    snapshots = []
    for idx in range(max_index_to_try):
        cap = cv2.VideoCapture(idx)
        if not cap.isOpened():
            cap.release()
            continue
        ok, frame = cap.read()
        cap.release()
        if not ok or frame is None:
            continue
        snapshots.append((idx, frame))

    if not snapshots:
        print("No cameras found. Check camera permissions in System Settings.")
        return CAM_INDEX
    if len(snapshots) == 1:
        return snapshots[0][0]

    thumb_w, thumb_h = 320, 180
    thumbs = []
    for idx, frame in snapshots:
        thumb = cv2.resize(frame, (thumb_w, thumb_h))
        cv2.putText(thumb, f"Press {idx}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)
        thumbs.append(thumb)

    row = np.hstack(thumbs)
    window_name = "Choose your camera - press the number shown, or q to use default"
    cv2.imshow(window_name, row)
    print("Look at the popup window and press the number key under the camera you want.")

    chosen = snapshots[0][0]
    while True:
        key = cv2.waitKey(0) & 0xFF
        pressed_indices = {idx for idx, _ in snapshots}
        if key in [ord(str(i)) for i in pressed_indices]:
            chosen = int(chr(key))
            break
        if key in (ord('q'), 27):
            break

    cv2.destroyWindow(window_name)
    print(f"Using camera index {chosen}")
    return chosen

def main():
    ensure_model()
    cam_index = choose_camera()

    cap = cv2.VideoCapture(cam_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_H)

    background = None
    mode = "reveal"
    mode_index = 0
    shape_index = 0
    pinch_state = [False, False]
    last_key_press = ""  # For displaying last key pressed
    last_key_time = 0

    portals = [Portal(color=(255, 215, 0)), Portal(color=(0, 200, 255))]

    options = HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=RunningMode.VIDEO,
        num_hands=2,
        min_hand_detection_confidence=0.6,
        min_tracking_confidence=0.6,
    )

    with HandLandmarker.create_from_options(options) as landmarker:
        start_time = time.time()
        frame_index = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                print("Could not read from webcam.")
                break

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            timestamp_ms = max(int((time.time() - start_time) * 1000), frame_index)
            result = landmarker.detect_for_video(mp_image, timestamp_ms)
            frame_index += 1

            active_portals = []
            if result.hand_landmarks:
                for i, hand_landmarks in enumerate(result.hand_landmarks[:2]):
                    index_tip = landmark_px(hand_landmarks[8], w, h)
                    thumb_tip = landmark_px(hand_landmarks[4], w, h)
                    dist = math.hypot(index_tip[0] - thumb_tip[0], index_tip[1] - thumb_tip[1])
                    radius = int(np.interp(dist, [20, 200], [MIN_RADIUS, MAX_RADIUS]))
                    radius = max(MIN_RADIUS, min(MAX_RADIUS, radius))

                    portal = portals[i]
                    portal.update(index_tip, radius)
                    active_portals.append(portal)

                    if dist < PINCH_TRIGGER_DIST:
                        if not pinch_state[i]:
                            mode_index = (mode_index + 1) % len(MODE_LIST)
                            mode = MODE_LIST[mode_index]
                            pinch_state[i] = True
                    elif dist > PINCH_RELEASE_DIST:
                        pinch_state[i] = False

            for portal in portals:
                portal.deactivate()
            for p in active_portals:
                p.active = True

            shape = SHAPES[shape_index]
            t = time.time() - start_time
            rotation = t * 0.6

            output = frame.copy()
            for portal in active_portals:
                center_i = (int(portal.center[0]), int(portal.center[1]))
                r_i = int(portal.radius)
                shape_mask = np.zeros((h, w), dtype=np.uint8)
                draw_shape_mask(shape_mask, shape, center_i, r_i, rotation)
                effect_layer = build_effect_layer(frame, background, mode, center_i, r_i)
                output = composite_mask(output, effect_layer, shape_mask)

            for portal in active_portals:
                center_i = (int(portal.center[0]), int(portal.center[1]))
                r_i = int(portal.radius)
                draw_glow_ring(output, shape, center_i, r_i, portal.color, t, rotation)

            # Status line
            status = f"Filter: {mode} | Shape: {shape} | BG: {'SET' if background is not None else 'NOT SET (press b)'}"
            cv2.putText(output, status, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Show last key pressed (for debugging)
            if time.time() - last_key_time < 1.0:  # Show for 1 second
                cv2.putText(output, f"KEY PRESSED: {last_key_press}", (10, 55), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)
            
            cv2.putText(output, "CLICK WINDOW THEN: Pinch=Filter | s=Shape | b=BG | 1-7=Filter | q=Quit",
                        (10, h - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1, cv2.LINE_AA)

            cv2.imshow("AI Invisibility Portal - Dual Hand", output)

            # IMPROVED KEY DETECTION - wait longer for key press
            key = cv2.waitKey(10) & 0xFF  # Changed from 1 to 10ms
            
            # Check if any key was pressed
            if key != 255:  # A key was pressed
                last_key_press = f"'{chr(key)}' (code: {key})"
                last_key_time = time.time()
                print(f"Key detected: {last_key_press}")
            
            if key in (ord('q'), 27):
                break
            elif key == ord('b'):
                background = frame.copy()
                brightness = float(background.mean())
                print(f"\n✅ Background captured! Brightness: {brightness:.2f}")
                if brightness < 40:
                    print("⚠️ WARNING: Very dark! Make sure room is lit.")
            elif key == ord('s'):
                shape_index = (shape_index + 1) % len(SHAPES)
                print(f"Shape changed to: {SHAPES[shape_index]}")
            elif key in MODES:
                mode = MODES[key]
                mode_index = MODE_LIST.index(mode)
                print(f"Filter changed to: {mode}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()