from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import os
import whisper
from ..src.models import TranscriptionInput

app = FastAPI()
model = None


@app.on_event("startup")
async def startup_event():
  global model
  model = whisper.load_model("tiny")


@app.post("/")
async def transcription(input_data: TranscriptionInput):
    file = input_data.file
    with open("audio.wav", 'wb') as f:
        while contents := file.file.read(1024 * 1024):
            f.write(contents)
        file.file.close()
    result = model.transcribe("audio.wav")["text"]

    # delete the audio file
    os.remove("audio.wav")
    return result

@app.get("/", description="The root redirect to swagger user interface")
def root():
    return RedirectResponse(url="/docs")
