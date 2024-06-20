import streamlit as st
import numpy as np
import sounddevice as sd
import soundfile as sf
import noisereduce as nr
import speech_recognition as sr
from io import BytesIO

# Function to record audio
def record_audio(duration, sample_rate):
    st.write("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    st.write("Recording complete.")
    return audio_data.flatten()

# Function to reduce noise
def reduce_noise(audio_data, sample_rate):
    noise_sample = audio_data[:sample_rate]  # First second as noise sample
    reduced_noise_audio = nr.reduce_noise(y=audio_data, sr=sample_rate, y_noise=noise_sample)
    return reduced_noise_audio

# Function to recognize speech from audio
def recognize_speech_from_audio(audio_data, sample_rate):
    recognizer = sr.Recognizer()
    
    # Save the audio data to a BytesIO object
    with BytesIO() as temp_audio:
        sf.write(temp_audio, audio_data, sample_rate, format='WAV')
        temp_audio.seek(0)
        
        with sr.AudioFile(temp_audio) as source:
            audio = recognizer.record(source)
        try:
            transcription = recognizer.recognize_google(audio)
            return transcription
        except sr.RequestError:
            return "API unavailable"
        except sr.UnknownValueError:
            return "Unable to recognize speech"

# Streamlit app
st.title("WhisperWriter")
st.write("""
Speech to text conversion.
""")
# Set duration and sample rate
duration = st.slider("Select recording duration (seconds)", 1, 10, 5)
sample_rate = 16000  # Sample rate for recording

if st.button("Record"):
    # Record audio
    audio_data = record_audio(duration, sample_rate)
    
    # Reduce noise
    st.write("Reducing noise...")
    reduced_noise_audio = reduce_noise(audio_data, sample_rate)
    
    # Recognize speech
    st.write("Recognizing speech...")
    transcription = recognize_speech_from_audio(reduced_noise_audio, sample_rate)
    
    # Display transcription
    st.write("Transcription: ", transcription)
