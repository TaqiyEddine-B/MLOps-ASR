VENV_DIR=~/.venv
BASHRC=~/.bashrc

setup:
	virtualenv $(VENV_DIR)
	@echo "source $(VENV_DIR)/bin/activate" >> $(BASHRC)
	@echo "Virtual environment setup complete and bashrc updated."
	@echo "Please run 'source $(BASHRC)' or restart your terminal to apply the changes."

install:
	$(VENV_DIR)/bin/pip install --upgrade pip && $(VENV_DIR)/bin/pip install -r requirements.txt

clean:
	rm -rf $(VENV_DIR)
	@echo "Virtual environment removed"