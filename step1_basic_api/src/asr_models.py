import io

import librosa
import soundfile as sf

# import whisper
from fastapi import UploadFile
from transformers import WhisperForConditionalGeneration, WhisperProcessor


class ModelBase:
    def __init__(self):
        self.model = None

    def load_model(self):
        raise NotImplementedError

    def predict(self, input_data):
        raise NotImplementedError

# class OpenaiWhisper(ModelBase):
#     def __init__(self):
#         super().__init__()

#     def load_model(self):
#         self.model = whisper.load_model("tiny")

#     def predict(self, input_file:UploadFile):
#         # validate the input
#         TranscriptionInput(file=file)

#         with open("audio.wav", 'wb') as f:
#             while contents := file.file.read(1024 * 1024):
#                 f.write(contents)
#             file.file.close()
#         result = self.model.transcribe("audio.wav")["text"]
#         # clean up the file
#         os.remove("audio.wav")

#         return result

class HfWhisper(ModelBase):
    """Whisper model from HuggingFace"""
    def __init__(self):
        super().__init__()
        self.processor = None

    def load_model(self):
        self.model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-tiny")
        self.processor = WhisperProcessor.from_pretrained("openai/whisper-tiny")

    def predict(self, input_file:UploadFile):
        # Read the content of the UploadFile
        audio_content = input_file.file.read()

        # Convert the audio content to a file-like object
        audio_io = io.BytesIO(audio_content)

        # Load audio file using soundfile
        audio, sr = sf.read(audio_io)

        # Resample if necessary
        if sr != 16000:
            audio = librosa.resample(audio, orig_sr=sr, target_sr=16000)
        # Process the audio
        input_features = self.processor(audio, sampling_rate=16000, return_tensors="pt").input_features

        # Generate token ids
        predicted_ids = self.model.generate(input_features)

        # Decode the token ids to text
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)

        return transcription[0]