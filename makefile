env/bin/activate: requirements.txt
	python3.11 -m venv env
	./env/bin/pip3.11 install -r requirements.txt

run: env/bin/activate
	./env/bin/python3.11 src/main.py


clean:
	rm -rf __pycache__
	rm -rf env