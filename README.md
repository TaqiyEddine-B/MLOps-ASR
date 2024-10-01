![GitHub Workflow Status](https://github.com/TaqiyEddine-B/MLOps-ASR/actions/workflows/main.yml/badge.svg)
# MLOps-ASR: Bridging Automatic Speech Recognition and MLOps

This repository contains a full-stack implementation of an Automatic Speech Recognition (ASR) system audio inputs and return transcription results.
Built with a focus on MLOps best practices, it serves as both a learning journey for me and a demonstration of how to build, deploy, and maintain a production-ready ML system.

Key objectives:

- Set up a FastAPI project structure
- Integrate the Whisper ASR model for audio transcription
- Implement error handling and input validation
- Implement logging and monitoring
- Write unit tests for the API endpoints
- Dockerize the API
- Implement CI/CD pipeline
- Push the Docker image to AWS ECR
- Deploy the API to AWS ECS


Technologies used:

- FastAPI
- Whisper ASR model
- Pydantic
- MLflow
- Pytest
- Docker
- CI/CD
- AWS (ECR and ECS)

## Installation and Usage
To run this project locally, follow these steps:
1. Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/TaqiyEddine-B/MLOps-ASR.git
cd MLOps-ASR
```
2. Create a virtual environment and installl the required packages:
```bash
make setup
make install
```
3. Run the FastAPI server:
```bash
make run
```
