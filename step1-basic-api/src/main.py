import os

import mlflow
import whisper
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from loguru import logger

from ..src.models import TranscriptionInput, TranscriptionOutput

app = FastAPI()
model = None


mlflow.set_experiment("ASR-Transcription")

@app.on_event("startup")
async def startup_event():
  global model
  model_name='tiny'
  model = whisper.load_model(model_name)
  logger.info(f'Model {model_name} is loaded successfully')

@app.post("/",response_model=TranscriptionOutput)
async def transcription(file: UploadFile):
    run = None
    try :
        run = mlflow.start_run()

        # validate the input
        TranscriptionInput(file=file)

        with open("audio.wav", 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
            file.file.close()
        result = model.transcribe("audio.wav")["text"]
        # clean up the file
        os.remove("audio.wav")


        # log sth to mlflow
        mlflow.log_param("model_name", "tiny")
        mlflow.log_param("input_file", file.filename)
        mlflow.log_param("transcription", result)


        return TranscriptionOutput(transcription=result)
    except ValueError as e:
        mlflow.log_param("error", str(e))
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        mlflow.log_param("error", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}")
    finally:
        if run:
            mlflow.end_run()
@app.get("/", description="The root redirect to swagger user interface")
def root():
    return RedirectResponse(url="/docs")
