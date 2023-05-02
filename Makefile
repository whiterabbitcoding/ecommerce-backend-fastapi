dev:
# rm sql_app.db && python3 server/server.py
	python3 app/main.py

dockrun:
	docker run -p5666:5666 e-commerce-backend-repository:latest

build: 
	docker build -t e-commerce-backend-repository .

