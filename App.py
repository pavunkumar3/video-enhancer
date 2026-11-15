import streamlit as st
import os
import time
import cv2
import numpy as np

# Page Configuration
st.set_page_config(page_title="Personal Video Enhancer", page_icon="🎬", layout="centered")

st.title("🎬 சொந்த பயன்பாட்டு Video Enhancer")
st.write("வீடியோக்களின் தரத்தை உயர்த்தித் தெளிவாக மாற்றும் மேம்பட்ட முறை!")

# Step 1: Resolution Selection Option
st.subheader("⚙️ வீடியோ தரத்தைத் தேர்வு செய்யவும் (Resolution Selection)")
resolution_choice = st.selectbox(
    "வீடியோ எந்த தரத்திற்கு மாற்ற வேண்டும்?",
    ["HD (720p)", "Full HD (1080p)", "2K", "4K"]
)

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
                input_path = "input_video.mp4"
                output_path = "enhanced_video.mp4"
                
                with open(input_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                cap = cv2.VideoCapture(input_path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                if fps == 0 or np.isnan(fps):
                    fps = 30.0
                
                orig_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                orig_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                target_w, target_h = resolution_dims[resolution_choice]
                
                # Maintain aspect ratio (16:9) correctly
                orig_aspect = orig_width / orig_height
                target_aspect = target_w / target_h
                
                if orig_aspect > target_aspect:
                    final_w = target_w
                    final_h = int(target_w / orig_aspect)
                else:
                    final_h = target_h
                    final_w = int(target_h * orig_aspect)
                
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(output_path, fourcc, fps, (target_w, target_h))
                
                # Stronger sharpening kernel to make the difference clearly visible
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # High quality resize
                    resized = cv2.resize(frame, (final_w, final_h), interpolation=cv2.INTER_CUBIC)
                    
                    # Apply strong sharpening filter
                    sharpened = cv2.filter2D(resized, -1, kernel)
                    
                    # Optional: Boost contrast slightly for more clarity
                    enhanced_frame = cv2.convertScaleAbs(sharpened, alpha=1.1, beta=5)
                    
                    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
                    x_offset = (target_w - final_w) // 2
                    y_offset = (target_h - final_h) // 2
                    canvas[y_offset:y_offset+final_h, x_offset:x_offset+final_w] = enhanced_frame
                    
                    out.write(canvas)
                
                cap.release()
                out.release()
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                
                if os.path.exists(output_path):
                    st.success(f"🎉 வீடியோ வெற்றிகரமாக {resolution_choice} தரத்திற்கு மாற்றப்பட்டது! (எடுத்துக்கொண்ட நேரம்: {minutes} நிமிடம் {seconds} வினாடிகள்)")
                    
                    st.subheader("தெளிவுபடுத்தப்பட்ட வீடியோ (Enhanced Video):")
                    with open(output_path, "rb") as video_file:
                        video_bytes = video_file.read()
                        st.video(video_bytes)
                        
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
