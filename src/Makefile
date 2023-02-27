PROJECT_NAME = auth_api
DOCKER_COMPOSE_FILE = docker-compose.yml
DOCKER_COMPOSE_FILE_TESTS = docker-compose.tests.yml
DOCKER_COMPOSE_FILE_DEV = docker-compose.dev.yml

.PHONY: all run_tests stop_tests run logs rebuild stop

all:
	@echo "make run            - Запуск контейнеров"
	@echo "make stop           - Выключение контейнера"
	@echo "make rebuild        - Пересборка контейнера"
	@echo "make logs           - Логи сборки"
	@echo "make run_tests      - Запустить тесты"
	@echo "make stop_tests     - Остановить тесты"

run_tests:
	docker-compose -f $(DOCKER_COMPOSE_FILE_TESTS) up --build -d

stop_tests:
	docker-compose -f $(DOCKER_COMPOSE_FILE_TESTS) down

run:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up --build -d

logs:
	docker-compose -f $(DOCKER_COMPOSE_FILE) logs

rebuild:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down && docker-compose -f $(DOCKER_COMPOSE_FILE) up --build -d

stop:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

dev:
	docker-compose -f $(DOCKER_COMPOSE_FILE_DEV) up --build -d