import os
import sys
import google.generativeai as genai
import config
import subprocess
import middleware

genai.configure(api_key=config.GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")



def process_input(user_input, from_voice=False):
    """Send user input to Gemini and process response."""
    try:
        response = model.generate_content(user_input)
        # model_response = response.text.strip()
        model_response = middleware.process_response(response.text.strip())

        print(f"🤖 Bot: {model_response}")

        if from_voice:
            try:
                python_executable = sys.executable  
                subprocess.run([python_executable, "TTSpeech.py", model_response], check=True)
            except Exception as e:
                print(f"❌ Error running TTS: {e}")

    except Exception as e:
        print(f"❌ Error processing input: {e}")

if len(sys.argv) > 1:
    user_input = " ".join(sys.argv[1:])
    print(f"🎤 Voice Input: {user_input}")
    process_input(user_input, from_voice=True)
else:
    while True:
        user_input = input("📝 You: ").strip()
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("👋 Goodbye!")
            break
        process_input(user_input)
