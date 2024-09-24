from fastapi import FastAPI, File, UploadFile
import whisper

app = FastAPI()
model = None


@app.on_event("startup")
async def startup_event():
  global model
  model = whisper.load_model("tiny")

@app.post("/")
async def transcription(file: UploadFile):
    with open("audio.wav", 'wb') as f:
        while contents := file.file.read(1024 * 1024):
            f.write(contents)
        file.file.close()
    return model.transcribe("audio.wav")["text"]

@app.get("/", description="The root redirect to swagger user interface")
def root():
    return RedirectResponse(url="/docs")
