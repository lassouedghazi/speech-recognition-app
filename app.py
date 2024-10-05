import streamlit as st
import speech_recognition as sr

# Define a list of common language codes
LANGUAGES = {
    'English': 'en-US',
    'French': 'fr-FR',
    'Spanish': 'es-ES',
    'German': 'de-DE',
    'Chinese (Mandarin)': 'zh-CN',
    'Japanese': 'ja-JP',
    'Korean': 'ko-KR',
    'Italian': 'it-IT',
    'Portuguese': 'pt-PT',
    'Russian': 'ru-RU',
    'Arabic': 'ar-SA',
    'Hindi': 'hi-IN',
}

# Initialize global variable to store audio text
audio_text = None

def transcribe_speech(api_choice, lang):
    global audio_text  # Use the global variable
    
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()
    
    # Reading Microphone as source
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        audio_text = r.listen(source)
        st.info("📝 Transcribing...")

        try:
            if api_choice == "Google":
                text = r.recognize_google(audio_text, language=lang)
            elif api_choice == "Sphinx":
                text = r.recognize_sphinx(audio_text)
            else:
                text = "Invalid API choice"
            return text
        except sr.UnknownValueError:
            return "⚠️ Sorry, I did not understand that."
        except sr.RequestError as e:
            return f"⚠️ Could not request results; {e}"

def save_transcription(text):
    # Save transcription to a text file
    with open("transcription.txt", "w") as f:
        f.write(text)
    st.success("📄 Transcription saved!")

def main():
    global audio_text  # Use the global variable
    st.title("🎙️ Speech Recognition App 🎧")
    st.write("Welcome to the Speech Recognition App! This app allows you to transcribe your speech into text.")
    
    st.markdown("""
    ### How to Use:
    - **Choose API**: Select between Google or Sphinx for speech recognition.
    - **Choose Language**: Pick your preferred language from the dropdown list.
    - **Start Recording**: Click this button to begin speaking; the app will transcribe your speech into text.
    - **Pause Recording**: This button will pause the recording; you can use this if you need a break.
    - **Resume Recording**: Click this button to continue recording from where you left off.
    - **Save Transcription**: After recording, click this button to save the transcribed text to a file. You can then download the transcription.
    """)
    
    st.markdown("""
    ### About the Developer:
    - **Name**: Ghazi Lassoued
    - **Email**: [lassouedghazi21@gmail.com](mailto:lassouedghazi21@gmail.com)
    - **LinkedIn**: [https://www.linkedin.com/in/ghazi-lassoued-983419239/](https://www.linkedin.com/in/ghazi-lassoued-983419239/)
    """)

    api_choice = st.selectbox("Choose API", ["Google", "Sphinx"])
    lang_choice = st.selectbox("Choose Language", list(LANGUAGES.keys()))
    lang = LANGUAGES[lang_choice]

    # Session state to manage recording state
    if "is_recording" not in st.session_state:
        st.session_state.is_recording = False

    # Start Recording
    if st.button("🎤 Start Recording"):
        if not st.session_state.is_recording:
            st.session_state.is_recording = True
            text = transcribe_speech(api_choice, lang)
            st.session_state.transcription_text = text
            st.write("Transcription: ", text)

    # Pause Recording
    if st.button("⏸️ Pause Recording"):
        st.session_state.is_recording = False
        audio_text = None  # Clear audio text to pause

    # Resume Recording
    if st.button("▶️ Resume Recording"):
        if not st.session_state.is_recording:
            st.session_state.is_recording = True
            st.info("Resuming... Speak now:")
            text = transcribe_speech(api_choice, lang)
            st.session_state.transcription_text += " " + text  # Append to existing text
            st.write("Transcription: ", st.session_state.transcription_text)

    if "transcription_text" in st.session_state:
        if st.button("💾 Save Transcription"):
            save_transcription(st.session_state.transcription_text)
            # Provide a download link for the saved file
            st.download_button(
                label="📥 Download Transcription",
                data=st.session_state.transcription_text,
                file_name="transcription.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
