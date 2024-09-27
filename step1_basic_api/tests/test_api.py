import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from step1_basic_api.src.main import app
from io import BytesIO
from loguru import logger

client = TestClient(app)

# Mock audio data for the upload
def mock_audio_file():
    from pydub import AudioSegment
    from io import BytesIO

    audio = AudioSegment.silent(duration=1000)  
    buffer = BytesIO()
    audio.export(buffer, format="mp3")
    buffer.seek(0)
    return buffer

# Patch both the whisper model loading and the global model variable in the FastAPI app
@patch("whisper.load_model")
@patch("step1_basic_api.src.main.model", new_callable=MagicMock)
@patch("mlflow.start_run")
@patch("mlflow.log_param")
def test_transcription_route(mock_log_param, mock_start_run, mock_model, mock_load_model):
    # Set up mocks for whisper and mlflow
    mock_model.transcribe.return_value = {"text": "This is a test transcription", "segments": [], "language": "en"}
    mock_load_model.return_value = mock_model

    mock_run = MagicMock()
    mock_start_run.return_value = mock_run

    # Create a test audio file and make a request
    audio_file = mock_audio_file()
    response = client.post("/", files={"file": ("test_audio.mp3", audio_file, "audio/mpeg")})
    logger.info(f"Response received: {response}")
    logger.info(f"Response content: {response.content}")

    # Ensure the model's transcribe method was called
    mock_model.transcribe.assert_called_once()

    # Assertions
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, content: {response.content}"
    data = response.json()
    assert data["transcription"] == "This is a test transcription"

    # Ensure mlflow logging was called
    mock_log_param.assert_any_call("model_name", "tiny")
    mock_log_param.assert_any_call("input_file", "test_audio.mp3")
    mock_log_param.assert_any_call("transcription", "This is a test transcription")
