import streamlit as st
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from PIL import Image
import tempfile
from datetime import datetime
import time

# Load model
model = load_model('camera_model_v2.keras')
categories = ['blank', 'blur', 'haze', 'low_light', 'normal', 'occlusion']

st.title("📷 Camera Feed Quality Detection System")
st.write("Upload an image or video to detect camera tampering!")

# Alert log
if 'alert_log' not in st.session_state:
    st.session_state.alert_log = []

# Choose input type
option = st.radio("Select Input Type:", ["Upload Image", "Upload Video"])

# ─── IMAGE ───
if option == "Upload Image":
    uploaded_file = st.file_uploader("Choose an image...",
                                      type=['jpg', 'jpeg', 'png'])
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption='Uploaded Image', width=300)

        img = np.array(image)
        img = cv2.resize(img, (64, 64))
        img_input = np.expand_dims(img, axis=0) / 255.0

        prediction = model.predict(img_input)
        predicted_class = categories[np.argmax(prediction)]
        confidence = np.max(prediction) * 100

        st.subheader("Result:")
        if predicted_class == 'normal':
            st.success(f"✅ Normal — Confidence: {confidence:.2f}%")
        else:
            st.error(f"⚠️ {predicted_class.upper()} Detected — Confidence: {confidence:.2f}%")
            # Add to alert log
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.alert_log.append(
                f"⚠️ {predicted_class.upper()} detected at {timestamp}"
            )

# ─── VIDEO ───
elif option == "Upload Video":
    uploaded_video = st.file_uploader("Choose a video...",
                                       type=['mp4', 'avi', 'mov'])
    if uploaded_video is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(uploaded_video.read())

        st.video(uploaded_video)

        # Settings
        FPS = 30
        ALERT_SECONDS = 10
        ALERT_FRAMES = FPS * ALERT_SECONDS  # 300 frames

        if st.button("Analyze Video"):
            cap = cv2.VideoCapture(tfile.name)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            frame_count = 0
            predictions = []
            consecutive_count = 0
            last_prediction = None
            alerts = []

            progress = st.progress(0)
            status_text = st.empty()
            alert_box = st.empty()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Analyze every 10th frame
                if frame_count % 10 == 0:
                    img = cv2.resize(frame, (64, 64))
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img_input = np.expand_dims(img, axis=0) / 255.0

                    prediction = model.predict(img_input, verbose=0)
                    predicted_class = categories[np.argmax(prediction)]
                    confidence = np.max(prediction) * 100
                    predictions.append(predicted_class)

                    # Check consecutive frames
                    if predicted_class == last_prediction:
                        consecutive_count += 10
                    else:
                        consecutive_count = 0
                        last_prediction = predicted_class

                    # Alert if tampering for 10 seconds
                    if consecutive_count >= ALERT_FRAMES and predicted_class != 'normal':
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        alert_msg = f"⚠️ ALERT: {predicted_class.upper()} detected for 10+ seconds at {timestamp}"
                        if alert_msg not in alerts:
                            alerts.append(alert_msg)
                            st.session_state.alert_log.append(alert_msg)
                            alert_box.error(alert_msg)

                    # Update progress
                    progress.progress(min(frame_count / total_frames, 1.0))
                    status_text.text(f"Analyzing... Current: {predicted_class} ({confidence:.1f}%)")

                frame_count += 1

            cap.release()

            # Final Results
            st.subheader("📊 Video Analysis Results:")

            from collections import Counter
            most_common = Counter(predictions).most_common(1)[0][0]

            if most_common == 'normal':
                st.success(f"✅ Video is mostly Normal")
            else:
                st.error(f"⚠️ Main Issue: {most_common.upper()}")

            # Show breakdown
            st.subheader("Frame Breakdown:")
            for category in categories:
                count = predictions.count(category)
                percentage = (count / len(predictions)) * 100
                st.write(f"{category}: {count} frames ({percentage:.1f}%)")

            # Show alerts
            if alerts:
                st.subheader("🚨 Alerts Triggered:")
                for alert in alerts:
                    st.error(alert)
            else:
                st.success("✅ No tampering alerts triggered!")

# ─── ALERT LOG ───
st.sidebar.title("🚨 Alert Log")
if st.session_state.alert_log:
    for log in st.session_state.alert_log:
        st.sidebar.error(log)
else:
    st.sidebar.success("✅ No alerts yet!")
