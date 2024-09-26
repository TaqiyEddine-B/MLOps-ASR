from fastapi import UploadFile
from loguru import logger
from pydantic import BaseModel, field_validator


class TranscriptionInput(BaseModel):
    file: UploadFile

    @field_validator('file')
    def validate_file_type(cls, v):
        if not v.filename.lower().endswith('.mp3'):
            error_message= 'Only MP3 files are allowed'
            logger.error(error_message)
            raise ValueError(error_message)
        return v


class  TranscriptionOutput(BaseModel):
    transcription: str
