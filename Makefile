up:
	docker-compose build
	docker-compose up

down:
	docker-compose down

ps:
	docker-compose ps

restart: down up