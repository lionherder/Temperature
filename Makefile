PROJECT=env
BIN=env/bin/

develop: requirements.txt
	test -d $(PROJECT) || python3 -m venv $(PROJECT)
	. $(PROJECT)/bin/activate
	$(BIN)pip install --upgrade pip
	$(BIN)pip install -r requirements.txt

server:
	. env/bin/activate
	python3 src/Temperature.py server 

client:
	. env/bin/activate
	python3 src/Temperature.py client 

clean:
	rm -rf $(PROJECT)
	find -iname "*.pyc" -delete
