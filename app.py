import streamlit as st
import cv2
import time
import pandas as pd
import requests
import io
from datetime import datetime
from db import init_db, insert_event, fetch_events

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Real-Time CV Event Detection",
    layout="wide"
)
st.title("🎥 Real-Time Computer Vision Event Detection System")

# --------------------------------------------------
# Initialize Database
# --------------------------------------------------
init_db()

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "running" not in st.session_state:
    st.session_state.running = False

if "session_start" not in st.session_state:
    st.session_state.session_start = None

# --------------------------------------------------
# Control Buttons
# --------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Start Monitoring"):
        st.session_state.running = True
        st.session_state.session_start = datetime.now()

with col2:
    if st.button("⏹ Stop & Save"):
        st.session_state.running = False

# --------------------------------------------------
# UI Placeholders
# --------------------------------------------------
frame_placeholder = st.empty()
status_placeholder = st.empty()
fps_placeholder = st.empty()

# --------------------------------------------------
# Configurable Thresholds
# --------------------------------------------------
MOTION_THRESHOLD = 5000
OBJECT_COUNT_THRESHOLD = 5
REST_API_URL = "http://localhost:5000/events"  # optional

# --------------------------------------------------
# Main Computer Vision Loop
# --------------------------------------------------
if st.session_state.running:
    cap = cv2.VideoCapture(0)

    prev_frame = None
    frame_count = 0
    start_time = time.time()

    while st.session_state.running:
        ret, frame = cap.read()
        if not ret:
            st.error("❌ Unable to access webcam")
            break

        frame_count += 1

        # -----------------------------
        # Image Processing
        # -----------------------------
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Grayscale
        blur = cv2.GaussianBlur(gray, (21, 21), 0)      # Noise reduction

        motion_detected = False
        motion_value = 0
        object_count = 0

        if prev_frame is not None:
            # -----------------------------
            # Motion Detection
            # -----------------------------
            diff = cv2.absdiff(prev_frame, blur)
            thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
            motion_value = cv2.countNonZero(thresh)

            if motion_value > MOTION_THRESHOLD:
                motion_detected = True

            # -----------------------------
            # Contour Detection (Object Count)
            # -----------------------------
            contours, _ = cv2.findContours(
                thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
            )
            object_count = len(contours)

        prev_frame = blur
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # -----------------------------
        # Event Handling
        # -----------------------------
        if motion_detected:
            insert_event(timestamp, "MOTION_DETECTED", motion_value)

            event_payload = {
                "timestamp": timestamp,
                "event_type": "MOTION_DETECTED",
                "value": motion_value
            }

            # Optional REST API send (safe)
            try:
                requests.post(REST_API_URL, json=event_payload, timeout=0.2)
            except:
                pass

            status_placeholder.error("🚨 Motion Detected")

        elif object_count > OBJECT_COUNT_THRESHOLD:
            insert_event(timestamp, "OBJECT_COUNT_THRESHOLD_EXCEEDED", object_count)

            event_payload = {
                "timestamp": timestamp,
                "event_type": "OBJECT_COUNT_THRESHOLD_EXCEEDED",
                "value": object_count
            }

            try:
                requests.post(REST_API_URL, json=event_payload, timeout=0.2)
            except:
                pass

            status_placeholder.warning("📦 Object Count Threshold Exceeded")

        else:
            status_placeholder.success("✅ Monitoring... No Event")

        # -----------------------------
        # FPS Calculation (Bonus)
        # -----------------------------
        elapsed = time.time() - start_time
        fps = frame_count / elapsed if elapsed > 0 else 0
        fps_placeholder.info(f"📈 FPS: {fps:.2f}")

        # -----------------------------
        # Display Video Frame
        # -----------------------------
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB")

    cap.release()

# --------------------------------------------------
# Session Summary
# --------------------------------------------------
if st.session_state.session_start and not st.session_state.running:
    st.success(
        f"🧾 Session saved | Started at: "
        f"{st.session_state.session_start.strftime('%Y-%m-%d %H:%M:%S')}"
    )

# --------------------------------------------------
# Display Stored Events
# --------------------------------------------------
st.subheader("📊 Stored Events")

events = fetch_events()

if events:
    df = pd.DataFrame(events, columns=["Timestamp", "Event Type", "Value"])
    st.dataframe(df, use_container_width=True)

    # -----------------------------
    # CSV Export
    # -----------------------------
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    st.download_button(
        label="⬇️ Download Events as CSV",
        data=csv_buffer.getvalue(),
        file_name="cv_events_log.csv",
        mime="text/csv"
    )
else:
    st.info("No events recorded yet.")
