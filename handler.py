import base64
import io
import numpy as np
import runpod
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code="a")  # English

def handler(job):
    data = job.get("input", {})
    text = data.get("text", "Hello from Kokoro")
    voice = data.get("voice", "af_heart")

    chunks = []
    for _, _, audio in pipeline(text, voice=voice):
        chunks.append(audio)

    if not chunks:
        return {"error": "No audio generated"}

    audio = np.concatenate(chunks)
    buf = io.BytesIO()
    sf.write(buf, audio, 24000, format="WAV")
    return {"audio_base64": base64.b64encode(buf.getvalue()).decode("utf-8")}
    
runpod.serverless.start({"handler": handler})
