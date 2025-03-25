import whisper
import sounddevice as sd
import numpy as np
import wave
import subprocess
import sys


model = whisper.load_model("base")


def record_audio(filename="input_audio.wav", duration=5, sample_rate=16000):
    print("🎤 Speak now...")

    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype=np.int16)
    sd.wait()

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(recording.tobytes())

    print("✅ Audio saved as:", filename)

def transcribe_audio(filename="input_audio.wav"):
    try:
        result = model.transcribe(filename)
        transcribed_text = result["text"].strip()
        print("📝 Transcription:", transcribed_text)
        return transcribed_text
    except Exception as e:
        print("❌ Error in transcription:", e)
        return ""


record_audio()
transcribed_text = transcribe_audio()


if transcribed_text:  
    try:
        python_executable = sys.executable  
        subprocess.run([python_executable, "chat.py", transcribed_text], check=True)
    except Exception as e:
        print("❌ Error running chat.py:", e)
