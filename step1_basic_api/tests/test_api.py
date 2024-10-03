from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from step1_basic_api.src.main import app

client = TestClient(app)

# Mock audio data for the upload
def mock_audio_file():
    from io import BytesIO

    from pydub import AudioSegment

    audio = AudioSegment.silent(duration=1000)
    buffer = BytesIO()
    audio.export(buffer, format="mp3")
    buffer.seek(0)
    return buffer

@patch("step1_basic_api.src.main.model")
@patch("mlflow.start_run")
@patch("mlflow.log_param")
@patch("mlflow.end_run")
def test_transcription_route(mock_end_run, mock_log_param, mock_start_run, mock_model):
    # Set up mocks for the model and mlflow
    mock_model.predict.return_value = "This is a test transcription"

    mock_run = MagicMock()
    mock_start_run.return_value = mock_run

    # Create a test audio file and make a request
    audio_file = mock_audio_file()
    response = client.post("/", files={"file": ("test_audio.mp3", audio_file, "audio/mpeg")})

    # Ensure the model's predict method was called
    mock_model.predict.assert_called_once()

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["transcription"] == "This is a test transcription"

    # Ensure mlflow logging was called
    mock_log_param.assert_any_call("model_name", "tiny")
    mock_log_param.assert_any_call("input_file", "test_audio.mp3")
    mock_log_param.assert_any_call("transcription", "This is a test transcription")

    # Ensure mlflow.end_run was called
    mock_end_run.assert_called_once()
