import streamlit as st
import os
import time
import cv2
import numpy as np

# Page Configuration
st.set_page_config(page_title="Personal Video Enhancer", page_icon="🎬", layout="wide")

st.title("🎬 சொந்த பயன்பாட்டு Video Enhancer & Comparison")
st.write("ஒரிஜினல் மற்றும் என்ஹான்ஸ் செய்த வீடியோக்களை ஒரே திரையில் பக்கத்து பக்கத்தில் ஒப்பிட்டுப் பாருங்கள்!")

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
    
    # Save input video locally
    input_path = "input_video.mp4"
    output_path = "enhanced_video.mp4"
    
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("🚀 Video Enhance செய்து ஒப்பிட்டுப் பார்"):
        start_time = time.time()
        
        with st.spinner(f"வீடியோ {resolution_choice} தரத்திற்கு மாற்றப்பட்டு வருகிறது... சிறிது நேரம் காத்திருக்கவும்..."):
            try:
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
                
                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    resized = cv2.resize(frame, (final_w, final_h), interpolation=cv2.INTER_CUBIC)
                    sharpened = cv2.filter2D(resized, -1, kernel)
                    enhanced_frame = cv2.convertScaleAbs(sharpened, alpha=1.1, beta=5)
                    
                    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
                    x_offset = (target_w - final_w) // 2
                    y_offset = (target_h - final_h) // 2
                    canvas[y_offset:y_offset+final_h, x_offset:x_offset+final_h] = enhanced_frame # Fixed array slice indexing
                    
                    # Correct slicing assignment safely:
                    canvas[y_offset:y_offset+final_h, x_offset:x_offset+final_w] = enhanced_frame
                    
                    out.write(canvas)
                
                cap.release()
                out.release()
                
                end_time = time.time()
                elapsed_time = end_time - start_time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                
                if os.path.exists(output_path):
                    st.success(f"🎉 வீடியோ வெற்றிகரமாக என்ஹான்ஸ் செய்யப்பட்டது! (எடுத்துக்கொண்ட நேரம்: {minutes} நிமிடம் {seconds} வினாடிகள்)")
                    
                    # Display Side-by-Side Comparison
                    st.subheader("📊 ஒப்பிட்டுப் பார்த்தல் (Side-by-Side Comparison):")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 📽️ ஒரிஜினல் வீடியோ (Original)")
                        st.video(input_path)
                        st.info("💡 இந்த ஒரிஜினல் வீடியோவில் சவுண்ட் சரியாகக் கேட்கும்.")
                    
                    with col2:
                        st.markdown(f"### ✨ தெளிவுபடுத்தப்பட்ட வீடியோ ({resolution_choice})")
                        st.video(output_path)
                        
                        with open(output_path, "rb") as video_file:
                            video_bytes = video_file.read()
                            st.download_button(
                                label="📥 என்ஹான்ஸ் செய்த வீடியோவை டவுன்லோட் செய்",
                                data=video_bytes,
                                file_name=f"enhanced_{resolution_choice.lower().replace(' ', '_')}.mp4",
                                mime="video/mp4",
                                key="download_btn"
                            )
                else:
                    st.error("பிழை: என்ஹான்ஸ் செய்யப்பட்ட வீடியோ ஃபைல் உருவாக்கப்படவில்லை.")
                
            except Exception as e:
                st.error(f"ஒரு பிழை ஏற்பட்டுள்ளது: {e}")
else:
    st.info("💡 தொடங்குவதற்கு உங்கள் வீடியோவை மேலே உள்ள கட்டத்தில் அப்லோட் செய்யவும்.")
