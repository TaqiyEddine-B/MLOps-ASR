# MLOps-ASR: Bridging Automatic Speech Recognition and MLOps

This repository contains a full-stack implementation of an Automatic Speech Recognition (ASR) system, built with a focus on MLOps best practices. It serves as both a learning journey and a demonstration of how to build, deploy, and maintain a production-ready ML system.

Key Features:
- FastAPI-based ASR service using state-of-the-art models

This project is structured in progressive steps, each building upon the last, to showcase the evolution from a basic ASR API to a fully-fledged, production-ready system.

## Table of Contents
- [Step 1: Develop a Basic ASR API with FastAPI](#step-1-develop-a-basic-asr-api-with-fastapi)


# Step 1: Develop a Basic ASR API with FastAPI

## Introduction

This step focuses on building the foundation of my MLOps-ASR project: a basic Automatic Speech Recognition (ASR) API using FastAPI and the Whisper base model. My goal is to create a functional, efficient, and well-structured API that can transcribe audio inputs.

Key objectives:

- Set up a FastAPI project structure
- Integrate the Whisper ASR model for audio transcription
- Implement error handling and input validation


By the end of this step, I'll have a production-ready ASR API that demonstrates best practices in API development, MLOps, and software engineering. This foundation will serve as the building block for more advanced features and optimizations in subsequent steps of the project.

Technologies used:

- FastAPI
- Whisper ASR model
- Pydantic

## Installation
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