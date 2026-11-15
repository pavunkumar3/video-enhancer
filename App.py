import streamlit as st
import os
import time
import cv2
import numpy as np

# Page Configuration
st.set_page_config(page_title="Personal Video Enhancer", page_icon="🎬", layout="centered")

st.title("🎬 சொந்த பயன்பாட்டு Video Enhancer")
st.write("உங்கள் பழைய அல்லது மங்கலான வீடியோக்களை எளிதாகத் தெளிவுபடுத்துங்கள்!")

# Step 1: Video Uploader
uploaded_file = st.file_uploader("உங்களது வீடியோவை அப்லோட் செய்யவும் (MP4, MOV)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.success("✅ வீடியோ வெற்றிகரமாக அப்லோட் செய்யப்பட்டது!")
    st.subheader("பதிவேற்றிய வீடியோ முன்னோட்டம் (Preview):")
    st.video(uploaded_file)
    
    if st.button("🚀 Video Enhance செய்"):
        start_time = time.time()
        
        with st.spinner("வீடியோ தரம் உயர்த்தப்பட்டுக் கொண்டிருக்கிறது... சிறிது நேரம் காத்திருக்கவும்..."):
            try:
                # Save input video locally
                input_path = "input_video.mp4"
                output_path = "enhanced_video.mp4"
                
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Open video using OpenCV
                cap = cv2.VideoCapture(input_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                if fps == 0 or np.isnan(fps):
                    fps = 30.0
                
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                # Setup video writer
                fourcc = cv2.VideoWriter_fourcc(*'avc1') # H.264 codec for web compatibility
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
                
                # Process frames (Sharpening filter)
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    # Apply sharpening filter to enhance details
                    enhanced_frame = cv2.filter2D(frame, -1, kernel)
                    out.write(enhanced_frame)
                
                cap.release()
                out.release()
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                
                st.success(f"🎉 வீடியோ வெற்றிகரமாக என்ஹான்ஸ் செய்யப்பட்டது! (எடுத்துக்கொண்ட நேரம்: {minutes} நிமிடம் {seconds} வினாடிகள்)")
                
                # Show enhanced video
                st.subheader("தெளிவுபடுத்தப்பட்ட வீடியோ (Enhanced Video):")
                with open(output_path, "rb") as video_file:
                    video_bytes = video_file.read()
                    st.video(video_bytes)
                    
                    # Download button
                    st.download_button(
                        label="📥 வீடியோவை டவுன்லோட் செய்ய இங்கே கிளிக் செய்யவும்",
                        data=video_bytes,
                        file_name="enhanced_output.mp4",
                        mime="video/mp4"
                    )
                
            except Exception as e:
                st.error(f"ஒரு பிழை ஏற்பட்டுள்ளது: {e}")
            finally:
                # Cleanup temp files
                if os.path.exists("input_video.mp4"):
                    os.remove("input_video.mp4")
                if os.path.exists("enhanced_video.mp4"):
                    os.remove("enhanced_video.mp4")
else:
    st.info("💡 தொடங்குவதற்கு உங்கள் வீடியோவை மேலே உள்ள கட்டத்தில் அப்லோட் செய்யவும்.")
