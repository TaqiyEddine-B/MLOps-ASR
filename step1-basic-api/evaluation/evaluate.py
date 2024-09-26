import json
import os

import mlflow
import whisper
from jiwer import wer
from loguru import logger


def evaluate_model(model_name:str):
    model = whisper.load_model(model_name)
    # get the root directory
    root_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    logger.info(root_dir)
    json_file_path = os.path.join(root_dir, "data/test_data.json")

    with open(json_file_path, "r") as f:
        test_data = json.load(f)["data"]
    total_wer =0

    with mlflow.start_run():
        mlflow.log_param("model_name", model_name)
        for index,data in enumerate(test_data):
            filepath=os.path.join(root_dir, "data/{}".format(data["file"]))
            result = model.transcribe(filepath)["text"]
            wer_file = wer(data["transcription"], result)
            total_wer += wer_file
            mlflow.log_metric("wer", wer_file, step=index)

        avg_wer = total_wer / len(test_data)
        mlflow.log_metric("average_wer", avg_wer)
    return avg_wer

if __name__ == "__main__":
    avg_wer = evaluate_model("tiny")
    print(f"Average WER: {avg_wer}")