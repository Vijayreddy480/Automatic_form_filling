import streamlit as st
from streamlit_mic_recorder import mic_recorder
from deepgram import DeepgramClient, PrerecordedOptions
import base64

st.title("Patient Registration Form Using Voice Recorder")
API_KEY = "379ee8695b7b01d83e5c6761bb99edb6abb3b12b"
dg_client = DeepgramClient(API_KEY)

if "used_audio" not in st.session_state:
    st.session_state.used_audio = {}

# --- Deepgram transcription wrapper ---
def deepgram_client(audio, field_name):
    if not audio or "bytes" not in audio:
        return ""
    audio_hash = hash(audio["bytes"])
    if audio_hash not in st.session_state.used_audio:
        source = {"buffer": audio["bytes"], "mimetype": "audio/webm"}
        options = PrerecordedOptions(
            model="nova-3",
            language="en-US",
            smart_format=True,
            detect_entities=True
        )
        response = dg_client.listen.rest.v("1").transcribe_file(source, options)
        alternatives = response["results"]["channels"][0]["alternatives"][0]
        transcript = getattr(alternatives, "transcript", "")
        entities = getattr(alternatives, "entities", [])
        ans = ""
        if entities:
            for entity in entities:
                for field in field_name:
                    if entity['label'].lower() == field:
                        ans += " " + entity['value']
        result = ans if field_name!="conditions" else transcript
        st.session_state.used_audio[audio_hash] = result
        return result
    return st.session_state.used_audio[audio_hash]

def inline_field(label, key, field_name=None):
    col1, col2, col3 = st.columns([1, 3, 2])  # Record | Text | Video

    # Initialize session state
    if key not in st.session_state:
        st.session_state[key] = ""
    if f"{key}_active" not in st.session_state:
        st.session_state[f"{key}_active"] = False
    if f"{key}_video_played" not in st.session_state:
        st.session_state[f"{key}_video_played"] = False

    # --- Col 1: Record Button ---
    with col1:
        if st.button("▶️ play video", key=f"{key}_btn"):
            st.session_state[f"{key}_active"] = True
            st.session_state[f"{key}_video_played"] = False  # reset video to play again

    # --- Col 3: Video (autoplay via HTML, no controls) ---
    with col3:
        if st.session_state.get(f"{key}_active", False) and not st.session_state[f"{key}_video_played"]:
            video_path = f"avatar_videos/{key}.mp4"
            with open(video_path, "rb") as f:
                video_bytes = f.read()
            video_base64 = base64.b64encode(video_bytes).decode("utf-8")

            video_html = f"""
                <video width="300" autoplay playsinline style="border-radius:12px; box-shadow:0 0 10px rgba(0,0,0,0.3);">
                    <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                </video>
            """
            st.markdown(video_html, unsafe_allow_html=True)
            st.session_state[f"{key}_video_played"] = True

    # --- Col 2: Text Input & Mic Recorder ---
    with col2:
        # Mic recorder always visible
        audio = mic_recorder(
            start_prompt="🎙️ Speak Now",
            stop_prompt="⏹️ Stop",
            key=f"{key}_mic",
            just_once=True
        )
        if audio:
            transcript = deepgram_client(audio, field_name)
            st.session_state[key] = transcript
            

        # Always show text input
        st.text_input(label, value=st.session_state.get(key, ""), key=f"{key}_input")

    return st.session_state.get(key, "")


# --- Fields ---
patient_name = inline_field("Patient Name", "patient_name", ["name"])
dob = inline_field("Age / Date of Birth", "dob", ["dob"])
gender = inline_field("Gender", "gender", ["gender_sexuality"])
contact = inline_field("Contact Number", "contact", ["phone_number", "credit_card"])
reason = inline_field("Reason and Symptoms", "symptoms", ["condition"])
speciality = inline_field("Speciality", "speciality", ["occupation"])
doctor_name = inline_field("Doctor Name", "doctor_name", ["name_medical_professional", "name_given"])
dt_raw = inline_field("Date and Time", "date_time", ["date", "time"])

# --- Submit Button ---
if st.button("Submit"):
    st.success("✅ Form Submitted")
    st.write("### Submitted Data")
    st.write({
        "Patient Name": st.session_state.get("patient_name", ""),
        "DOB": st.session_state.get("dob", ""),
        "Gender": st.session_state.get("gender", ""),
        "Contact": st.session_state.get("contact", ""),
        "Reason": st.session_state.get("reason_symptoms", ""),
        "Speciality": st.session_state.get("speciality", ""),
        "Doctor Name": st.session_state.get("doctor_name", ""),
        "Date & Time": st.session_state.get("date_time", "")
    })
