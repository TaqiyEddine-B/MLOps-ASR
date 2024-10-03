VENV_DIR=.venv
BASHRC=~/.bashrc
FILE=data/liverpool2.mp3 # https://audio-lingua.ac-versailles.fr/spip.php?article4295
FILE2=data/rentree_en_cm1.mp3
IMAGE_TAG=mlops-asr-api:latest

setup:
	virtualenv $(VENV_DIR)
	@echo "source $(VENV_DIR)/bin/activate" >> $(BASHRC)
	@echo "Virtual environment setup complete and bashrc updated."
	@echo "Please run 'source $(BASHRC)' or restart your terminal to apply the changes."

install:
	sudo apt update -y
	sudo apt install -y ffmpeg
	$(VENV_DIR)/bin/pip install --upgrade pip && $(VENV_DIR)/bin/pip install -r requirements.txt

clean:
	# uninstall all the packages
	$(VENV_DIR)/bin/pip freeze | xargs $(VENV_DIR)/bin/pip uninstall -y
lint:
	ruff check . --fix
watch:
	ruff check --watch
run:
	uvicorn step1_basic_api.src.main:app --host 127.0.0.1 --port 8000 --reload

curl:
	curl -X POST http://127.0.0.1:8000/ -F "file=@$(FILE2)"

mlflow:
	mlflow ui

evaluate:
	python -m step1-basic-api.evaluation.evaluate
test:
	PYTHONPATH=. pytest -v -s step1_basic_api/tests/


build:
	docker build -t $(IMAGE_TAG) -f step1_basic_api/Dockerfile .

run-docker: build
	docker run -p 8000:8000 $(IMAGE_TAG)

all: lint test


run-demo:
	uvicorn fastapi_demo.main:app --host 127.0.0.1 --port 8001 --reload
build-demo:
	docker build -t fastapi_demo:latest -f fastapi_demo/Dockerfile .

run-docker-demo:
	docker run -p 8001:8001 fastapi_demo:latest

clean_docker:
	docker system prune -a