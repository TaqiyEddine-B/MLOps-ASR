VENV_DIR=.venv
BASHRC=~/.bashrc
FILE=liverpool2.mp3 # https://audio-lingua.ac-versailles.fr/spip.php?article4295
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
	rm -rf $(VENV_DIR)
	@echo "Virtual environment removed"
format:
	ruff check .
run:
	uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

curl:
	curl -X POST http://127.0.0.1:8000/ -F "file=@$(FILE)"
