import streamlit as st
import base64
import os
import io
import time
import sounddevice as sd
import numpy as np
import tempfile
import assemblyai as aai
from scipy.io.wavfile import write

# ---------------- Setup ----------------
aai.settings.api_key = "b065f5c33fda424381840a1139b251a0"
config = aai.TranscriptionConfig(entity_detection=True)

if "started" not in st.session_state:
    st.session_state.started = False
if "current_field" not in st.session_state:
    st.session_state.current_field = 0
if "form_data" not in st.session_state:
    st.session_state.form_data = {}
if "video_played" not in st.session_state:
    st.session_state.video_played = False

# ---------------- Recording ----------------
def record_audio(duration=5, samplerate=16000):
    st.info("🎤 Recording started...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
    sd.wait()
    st.success("✅ Recording finished.")
    buffer = io.BytesIO()
    write(buffer, samplerate, audio)
    buffer.seek(0)  # rewind to start
    return buffer.read()

# ---------------- Deepgram ----------------
def Assembly_ai(audio_bytes, field_names):
    transcript = aai.Transcriber().transcribe(audio_bytes, config)
    if transcript.entities:
        value=" "
        for entity in transcript.entities:
            print(entity.text,entity.entity_type)
            if entity.entity_type in field_names:
                value+=" "+entity.text
        return value
    else:
        return transcript.text
# ---------------- Fields ----------------
fields = [
    {"label": "Patient Name", "key": "patient_name","field_name":["person_name"],"video": "avatar_videos/patient_name.mp4"},
    {"label": "Date of Birth", "key": "dob","field_name":["date_of_birth"],"video": "avatar_videos/dob.mp4"},
    {"label": "Gender", "key": "gender","field_name":["gender_sexuality"],"video": "avatar_videos/gender.mp4"},
    {"label": "Contact Number", "key": "contact", "field_name":["phone_number","credit_card"],"video": "avatar_videos/contact.mp4"},
    {"label": "Reason & Symptoms", "key": "symptoms","field_name":["medical_condition"], "video": "avatar_videos/symptoms.mp4"},
    {"label": "Speciality", "key": "speciality","field_name":["occupation"], "video": "avatar_videos/speciality.mp4"},
    {"label": "Doctor Name", "key": "doctor","field_name":["person_name"], "video": "avatar_videos/doctor_name.mp4"},
    {"label": "Date & Time", "key": "datetime","field_name":["date","time"], "video": "avatar_videos/date_time.mp4"},
]

# ---------------- UI ----------------
st.title("📝 Patient Registration Form")

if not st.session_state.started:
    if st.button("▶️ Start Form"):
        st.session_state.started = True
        st.rerun()

col_form, col_video = st.columns([2, 1])

with col_form:
    for f in fields:
        st.text_input(f["label"], value=st.session_state.form_data.get(f["key"], ""), key=f["key"])

with col_video:
    if st.session_state.started and st.session_state.current_field < len(fields):
        field = fields[st.session_state.current_field]

        if os.path.exists(field["video"]) and not st.session_state.video_played:
            with open(field["video"], "rb") as f:
                video_bytes = f.read()
            video_b64 = base64.b64encode(video_bytes).decode("utf-8")
            
            # force a unique key so every field refreshes video properly
            st.markdown(
    f"""
    <div style="position:fixed; right:50px; top:50%; transform:translateY(-50%);">
        <video key="{field['key']}" width="300" autoplay playsinline style="border-radius:12px; box-shadow:0px 4px 10px rgba(0,0,0,0.3);">
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
        </video>
    </div>
    """,
    unsafe_allow_html=True
)

            st.session_state.video_played = True
            time.sleep(5)  # wait 5s = video duration

            # record after video finishes
            audio_file = record_audio(duration=5)
            transcript = Assembly_ai(audio_file,field["field_name"])
            st.session_state.form_data[field["key"]] = transcript

            # move to next field
            st.session_state.current_field += 1
            st.session_state.video_played = False
            st.rerun()

if st.session_state.started and st.session_state.current_field >= len(fields):
    if st.button("✅ Submit Form"):
        st.success("Form submitted!")
        st.json(st.session_state.form_data)
