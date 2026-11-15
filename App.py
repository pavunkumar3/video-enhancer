import streamlit as st
import os
import time
import cv2
import numpy as np

# Page Configuration
st.set_page_config(page_title="Personal Video Enhancer", page_icon="🎬", layout="centered")

st.title("🎬 சொந்த பயன்பாட்டு Video Enhancer")
st.write("உங்கள் வீடியோக்களின் தரத்தைத் (Resolution) தேர்ந்தெடுத்து எளிதாகத் தெளிவுபடுத்துங்கள்!")

# Step 1: Resolution Selection Option
st.subheader("⚙️ வீடியோ தரத்தைத் தேர்வு செய்யவும் (Resolution Selection)")
resolution_choice = st.selectbox(
    "வீடியோ எந்த தரத்திற்கு மாற்ற வேண்டும்?",
    ["HD (720p)", "Full HD (1080p)", "2K", "4K"]
)

# Resolution dimensions mapping
resolution_dims = {
    "HD (720p)": (1280, 720),
    "Full HD (1080p)": (1920, 1080),
    "2K": (2560, 1440),
    "4K": (3840, 2160)
}

# Step 2: Video Uploader
uploaded_file = st.file_uploader("உங்களது வீடியோவை அப்லோட் செய்யவும் (MP4, MOV)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.success("✅ வீடியோ வெற்றிகரமாக அப்லோட் செய்யப்பட்டது!")
    st.subheader("பதிவேற்றிய வீடியோ முன்னோட்டம் (Preview):")
    st.video(uploaded_file)
    
    if st.button("🚀 Video Enhance செய்"):
        start_time = time.time()
        
        with st.spinner(f"வீடியோ {resolution_choice} தரத்திற்கு மாற்றப்பட்டு வருகிறது... சிறிது நேரம் காத்திருக்கவும்..."):
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
                
                # Target width and height based on user choice
                target_width, target_height = resolution_dims[resolution_choice]
                
                # Setup video writer with mp4v codec
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, fps, (target_width, target_height))
                
                # Process frames (Resize to chosen resolution + Sharpening filter)
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    # Resize frame to target resolution
                    resized_frame = cv2.resize(frame, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
                    # Apply sharpening filter
                    enhanced_frame = cv2.filter2D(resized_frame, -1, kernel)
                    out.write(enhanced_frame)
                
                cap.release()
                out.release()
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                
                if os.path.exists(output_path):
                    st.success(f"🎉 வீடியோ வெற்றிகரமாக {resolution_choice} தரத்திற்கு மாற்றப்பட்டது! (எடுத்துக்கொண்ட நேரம்: {minutes} நிமிடம் {seconds} வினாடிகள்)")
                    
                    # Show enhanced video
                    st.subheader("தெளிவுபடுத்தப்பட்ட வீடியோ (Enhanced Video):")
                    with open(output_path, "rb") as video_file:
                        video_bytes = video_file.read()
                        st.video(video_bytes)
                        
                        # Download button
                        st.download_button(
                            label="📥 வீடியோவை டவுன்லோட் செய்ய இங்கே கிளிக் செய்யவும்",
                            data=video_bytes,
                            file_name=f"enhanced_{resolution_choice.lower().replace(' ', '_')}.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("பிழை: என்ஹான்ஸ் செய்யப்பட்ட வீடியோ ஃபைல் உருவாக்கப்படவில்லை.")
                
            except Exception as e:
                st.error(f"ஒரு பிழை ஏற்பட்டுள்ளது: {e}")
            finally:
                if os.path.exists("input_video.mp4"):
                    os.remove("input_video.mp4")
else:
    st.info("💡 தொடங்குவதற்கு உங்கள் வீடியோவை மேலே உள்ள கட்டத்தில் அப்லோட் செய்யவும்.")
