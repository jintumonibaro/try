

import edge_tts
import asyncio
import simpleaudio as sa
import sys
from pydub import AudioSegment

if len(sys.argv) > 1:
    text_to_speak = " ".join(sys.argv[1:]).strip()
    print(f"🔊 Speaking: {text_to_speak}")

    try:
        
        output_mp3 = "output.mp3"
        output_wav = "output.wav"
        
        async def generate_speech():
            tts = edge_tts.Communicate(text_to_speak, voice="en-IN-NeerjaNeural")
            await tts.save(output_mp3)  

        asyncio.run(generate_speech())

    
        sound = AudioSegment.from_file(output_mp3, format="mp3")
        sound.export(output_wav, format="wav")

        print(f"✅ Speech saved to {output_wav}") 
 
    
        wave_obj = sa.WaveObject.from_wave_file(output_wav)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    except Exception as e:
        print(f"❌ Error generating speech: {e}")

else:
    print("⚠️ No text provided for speech synthesis.")

