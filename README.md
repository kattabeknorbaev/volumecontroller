# 🔊 VolumeKnuckle: Day 3 (Volume Tracker)

A gesture-based volume controller that uses Computer Vision to map physical hand movements to Windows system volume using **Delta Tracking** and **Keyboard Emulation**.

---

## 🚀 The Concept: Differential Motion Mapping
This version implements **Differential (Delta) Tracking**. Instead of mapping your hand to a specific static volume level, the script measures the *change* in your wrist's position over time. This creates a "ratchet" or "pump" effect that feels natural and stable.

- **Input (Analog):** The vertical displacement ($\Delta Y$) of a human fist captured via webcam.
- **Processing:** MediaPipe identifies landmarks; the script calculates the difference between the current frame and the previous anchor frame.
- **Output (Digital):** `PyAutoGUI` mimics physical media keys (`volumeup` / `volumedown`) to bypass Windows driver restrictions.

---

## 🛠️ Tech Stack
* **Python 3.13**
* **OpenCV:** Real-time video frame acquisition and UI status overlay.
* **MediaPipe:** High-fidelity hand landmark tracking.
* **PyAutoGUI:** Cross-platform GUI automation for driver-agnostic volume control.
* **NumPy:** Mathematical calculations for movement thresholds.

---

## 🎮 How to Use
1. **Launch:** Run `python main.py`.
2. **Engage:** Close your hand into a **fist** to activate the control logic.
3. **Control:** - **Move UP:** To increase volume (Threshold: $>0.03$ change).
   - **Move DOWN:** To decrease volume (Threshold: $<-0.03$ change).
4. **Reset:** Open your hand to "release" the volume handle and reset the tracking anchor.
5. **Exit:** Press **'q'** on the camera window to stop the script.

---

## 🧠 Logic Breakdown: Fist & Delta Detection
The script determines a "Fist" state by comparing the Y-coordinates of the finger tips to their respective knuckles. In the MediaPipe coordinate system, the top of the screen is $Y=0$ and the bottom is $Y=1$.



**The Calculation:**
1. If $Tip.y > Knuckle.y$ for all 4 fingers, a **Fist** is detected.
2. The script records the `prev_y` of the **Wrist (Landmark 0)**.
3. If the next `current_y` shows a difference of more than `0.03`, a volume command is sent and the anchor updates. This prevents "jitter" and accidental volume spikes.

---

---

## 📸 Note on Camera Identifiers
In the source code, you will see this line:
`cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)`

### Why index `2`?
Windows assigns an integer ID to every camera device. 
- **0:** Usually the built-in webcam.
- **1:** Often a virtual camera (OBS, Zoom, or EShare).
- **2:** Typically the external USB webcam.

**If the script doesn't open a window:**
Change the `2` to `0` or `1`. 

### What is `cv2.CAP_DSHOW`?
This flag forces OpenCV to use the **Windows DirectShow** framework. This is essential for:
1. Faster camera startup.
2. Higher resolution support.
3. Bypassing "Camera already in use" errors from other background processes.

---

## 📦 Installation
Ensure you have the following libraries installed in your environment:
```bash
pip install opencv-python mediapipe numpy pyautogui
