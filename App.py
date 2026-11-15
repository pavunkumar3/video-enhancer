import streamlit as st
import replicate
import os
import time

# Page Configuration
st.set_page_config(page_title="Personal Video Enhancer", page_icon="🎬", layout="centered")

st.title("🎬 சொந்த பயன்பாட்டு Video Enhancer")
st.write("உங்கள் பழைய அல்லது மங்கலான வீடியோக்களை AI மூலம் தெளிவான தரத்திற்கு மாற்றுங்கள்!")

# Step 1: API Key Input
api_key = st.text_input("உங்கள் Replicate API Key-ஐ உள்ளிடவும்:", type="password")

if api_key:
    os.environ["REPLICATE_API_TOKEN"] = api_key
    
    # Step 2: Video Quality / Resolution Selection Option
    st.subheader("⚙️ வீடியோ தரத்தைத் தேர்வு செய்யவும் (Quality Selection)")
    resolution_choice = st.selectbox(
        "வீடியோ எந்த தரத்தில் (Resolution) உயர்த்த வேண்டும்?",
        ["FHD", "2k", "4k"]
    )
    
    # Step 3: Video Uploader
    uploaded_file = st.file_uploader("உங்களது வீடியோவை அப்லோட் செய்யவும் (MP4, MOV)", type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        st.success("✅ வீடியோ வெற்றிகரமாக அப்லோட் செய்யப்பட்டது!")
        st.subheader("பதிவேற்றிய வீடியோ முன்னோட்டம் (Preview):")
        st.video(uploaded_file)
        
        if st.button("🚀 Video Enhance செய்"):
            start_time = time.time()
            
            with st.spinner("AI வீடியோவை தரம் உயர்த்திக் கொண்டிருக்கிறது... சிறிது நேரம் காத்திருக்கவும்..."):
                try:
                    # Temporary file save
                    temp_file_path = "temp_input_video.mp4"
                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Run AI Video Upscaler Model (Using direct model name without version hash)
                    with open(temp_file_path, "rb") as video_file:
                        output = replicate.run(
                            "lucataco/real-esrgan-video",
                            input={
                                "video": video_file
                            }
                        )
                    
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    minutes = int(elapsed_time // 60)
                    seconds = int(elapsed_time % 60)
                    
                    st.success(f"🎉 வீடியோ வெற்றிகரமாக என்ஹான்ஸ் செய்யப்பட்டது! (எடுத்துக்கொண்ட நேரம்: {minutes} நிமிடம் {seconds} வினாடிகள்)")
                    
                    # Show output video
                    st.subheader("தெளிவுபடுத்தப்பட்ட வீடியோ (Enhanced Video):")
                    st.video(output)
                    
                    # Download Link
                    st.markdown(f"### [📥 டவுன்லோட் செய்ய இங்கே கிளிக் செய்யவும்]({output})")
                    
                except Exception as e:
                    st.error(f"ஒரு பிழை ஏற்பட்டுள்ளது: {e}")
                finally:
                    if os.path.exists("temp_input_video.mp4"):
                        os.remove("temp_input_video.mp4")
else:
    st.info("💡 தொடங்குவதற்கு உங்கள் Replicate API Key-ஐ மேலே உள்ள கட்டத்தில் உள்ளிடவும்.")
