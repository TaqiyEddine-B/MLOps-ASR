from fastapi import FastAPI,UploadFile,HTTPException
from fastapi.responses import RedirectResponse
import os
import whisper
from ..src.models import TranscriptionInput,TranscriptionOutput

app = FastAPI()
model = None


@app.on_event("startup")
async def startup_event():
  global model
  model = whisper.load_model("tiny")


@app.post("/",response_model=TranscriptionOutput)
async def transcription(file: UploadFile):
    try :
        # validate the input
        TranscriptionInput(file=file)

        with open("audio.wav", 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
            file.file.close()
        result = model.transcribe("audio.wav")["text"]

        # clean up the file
        os.remove("audio.wav")
        return TranscriptionOutput(transcription=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.get("/", description="The root redirect to swagger user interface")
def root():
    return RedirectResponse(url="/docs")
