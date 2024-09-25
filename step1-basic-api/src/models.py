from pydantic import BaseModel,field_validator
from fastapi import UploadFile

class TranscriptionInput(BaseModel):
    file: UploadFile

    @field_validator('file')
    def validate_file_type(cls, v):
        if not v.filename.lower().endswith('.mp3'):
            raise ValueError('Only MP3 files are allowed')
        return v


class  TranscriptionOutput(BaseModel):
    transcription: str
