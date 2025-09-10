# 📝 Automatic & Semi-Automatic Form Filling — Video + Voice Guided Registration

This project provides two types of **Streamlit-based patient registration systems**:

1. **Automatic Form Filling**  
   - Each field is guided by a video that plays automatically in sequence.  
   - After the video finishes, the system records audio (fixed 5 seconds) and transcribes it into text.  
   - The field is auto-filled and the system moves to the next field.  

2. **Semi-Automatic Form Filling**  
   - All fields are displayed at once.  
   - Users can manually type values, play the video prompt for any field, or record speech on demand.  
   - Greater flexibility: fill fields in any order, use video/audio only when needed.  

---

## 🚀 Features
- 🎥 **Video-guided prompts** for each field.  
- 🎙️ **Voice recording & transcription** via:  
  - **Deepgram** → entity-aware extraction (name, DOB, phone, etc.).  
  - **AssemblyAI** → full-text transcription.  
- ✍️ **Manual text input override** always available.  
- ⚡ **Two workflows**: fully automatic OR semi-automatic.  
- 📊 **Submit** form data in structured JSON.  

---

## 📂 Project Structure
Automatic_form_filling/
├── avatar_videos/ # MP4 prompt videos for each field
├── automatic_form.py # Automatic sequential version
├── semi_automatic_form.py # Semi-automatic user-controlled version
├── deepgram_form.py # Deepgram API integration
├── assembly_form.py # AssemblyAI API integration
├── requirements.txt # Python dependencies
└── README.md

How to Get Started


## Clone the Repo
git clone https://gitlab.siamcomputing.com/siamcomputing-training/cet/machine-learning/ml-interns/2025/vijay-gurrala/form_filling
cd Legalchatbot-with-memory


## 2.Install the requirements

pip install -r requirements.txt


## 3. Set Up Environment Variables

Use your assembly api Key and deep gram api key


## Where Users Can Get Help

If you need help:contact Vijay Gurrala


##Who Maintains and Contributes
-Vijay Gurrala
