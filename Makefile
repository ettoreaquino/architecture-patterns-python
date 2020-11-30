build:
	docker-compose build

up:
	docker-compose up -d app

test:
	poetry run pytest --tb=short
logs:
	docker-compose logs app | tail -100

down:
	docker-compose down

all: down build up test
