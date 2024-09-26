import os
import pytest
from fastapi import UploadFile, HTTPException
from unittest.mock import MagicMock, patch
from step1_basic_api.src.main import transcription

@pytest.fixture
def mock_file():
    file = MagicMock(spec=UploadFile)
    file.filename = "test_audio.wav"
    file.file = MagicMock()
    file.file.read.return_value = b"audio_content"
    return file

@pytest.fixture
def mock_mlflow():
    with patch("step1_basic_api.src.main.mlflow") as mock:
        yield mock

@pytest.fixture
def mock_model():
    with patch("step1_basic_api.src.main.model") as mock:
        mock.transcribe.return_value = {"text": "Test transcription"}
        yield mock

@pytest.mark.asyncio
async def test_transcription_success(mock_file, mock_mlflow, mock_model):
    result = await transcription(mock_file)
    assert result.transcription == "Test transcription"
    mock_mlflow.log_param.assert_any_call("model_name", "tiny")
    mock_mlflow.log_param.assert_any_call("input_file", "test_audio.wav")
    mock_mlflow.log_param.assert_any_call("transcription", "Test transcription")

# @pytest.mark.asyncio
# async def test_transcription_file_write_error(mock_file, mock_mlflow):
#     mock_file.file.read.side_effect = IOError("File write error")
#     with pytest.raises(HTTPException) as exc_info:
#         await transcription(mock_file)
#     assert exc_info.value.status_code == 500
#     assert "File write error" in str(exc_info.value.detail)

# @pytest.mark.asyncio
# async def test_transcription_model_error(mock_file, mock_mlflow, mock_model):
#     mock_model.transcribe.side_effect = Exception("Model error")
#     with pytest.raises(HTTPException) as exc_info:
#         await transcription(mock_file)
#     assert exc_info.value.status_code == 500
#     assert "Model error" in str(exc_info.value.detail)

# @pytest.mark.asyncio
# async def test_transcription_cleanup(mock_file, mock_mlflow, mock_model):
#     with patch("src.main.os.remove") as mock_remove:
#         await transcription(mock_file)
#         mock_remove.assert_called_once_with("audio.wav")

# @pytest.mark.asyncio
# async def test_transcription_mlflow_end_run(mock_file, mock_mlflow, mock_model):
#     await transcription(mock_file)
#     mock_mlflow.end_run.assert_called_once()

# @pytest.mark.asyncio
# async def test_transcription_value_error(mock_file, mock_mlflow):
#     mock_file.filename = None  # This should trigger a ValueError in TranscriptionInput
#     with pytest.raises(HTTPException) as exc_info:
#         await transcription(mock_file)
#     assert exc_info.value.status_code == 400
#     mock_mlflow.log_param.assert_called_with("error", pytest.raises(ValueError).match)
