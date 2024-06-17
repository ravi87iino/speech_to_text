import speech_recognition as sr
import sounddevice as sd
import numpy as np
import noisereduce as nr
import soundfile as sf

# Function to record audio
def record_audio(duration, sample_rate):
    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete.")
    return audio_data.flatten()


def reduce_noise(audio_data, sample_rate):
    noise_sample = audio_data[:sample_rate] 
    reduced_noise_audio = nr.reduce_noise(y=audio_data, sr=sample_rate, y_noise=noise_sample)
    return reduced_noise_audio

def recognize_speech_from_audio(audio_data, sample_rate):
    recognizer = sr.Recognizer()
    sf.write("temp.wav", audio_data, sample_rate)
    
    with sr.AudioFile("temp.wav") as source:
        audio = recognizer.record(source)
    try:
        print("Recognizing...")
        transcription = recognizer.recognize_google(audio)
        return transcription
    except sr.RequestError:
        return "API unavailable"
    except sr.UnknownValueError:
        return "Unable to recognize speech"

if __name__ == "__main__":
    
    duration = 5  # Duration of recording in seconds
    sample_rate = 16000  # Sample rate for recording

    # Record audio
    audio_data = record_audio(duration, sample_rate)

    # Reduce noise
    reduced_noise_audio = reduce_noise(audio_data, sample_rate)

    # Recognize speech
    transcription = recognize_speech_from_audio(reduced_noise_audio, sample_rate)
    print("Transcription: ", transcription)
