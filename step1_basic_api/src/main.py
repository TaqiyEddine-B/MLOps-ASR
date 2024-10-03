
import os

import mlflow
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import RedirectResponse

from ..src.asr_models import HfWhisper
from ..src.models import TranscriptionOutput

app = FastAPI()

os.environ["GIT_PYTHON_REFRESH"] = "quiet"

mlflow.set_experiment("ASR-Transcription")

# @app.on_event("startup")
# async def startup_event():
#   global model
#   model_name='tiny'
#   model = whisper.load_model(model_name)
#   logger.info(f'Model {model_name} is loaded successfully')


model =HfWhisper()
model.load_model()


@app.post("/",response_model=TranscriptionOutput)
async def transcription(file: UploadFile):
    run = None
    try :
        run = mlflow.start_run()

        result = model.predict(file)

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
