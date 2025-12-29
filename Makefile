.PHONY: help install dev deps-up deps-down db-upgrade db-downgrade db-reset test test-cov clean docker-build docker-up docker-down format lint superuser

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias de Python
	pip install --upgrade pip
	pip install -r requirements.txt

dev: ## Ejecutar servidor en modo desarrollo
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

deps-up: ## Levantar dependencias (PostgreSQL, Redis, pgAdmin)
	docker-compose -f local-deps.yml up -d
	@echo "✅ Servicios levantados:"
	@echo "   - PostgreSQL: localhost:5432"
	@echo "   - Redis: localhost:6379"
	@echo "   - pgAdmin: http://localhost:5050"

deps-down: ## Detener dependencias
	docker-compose -f local-deps.yml down

deps-logs: ## Ver logs de dependencias
	docker-compose -f local-deps.yml logs -f

db-upgrade: ## Aplicar migraciones de base de datos
	alembic upgrade head

db-downgrade: ## Revertir última migración
	alembic downgrade -1

db-migrate: ## Crear nueva migración (uso: make db-migrate MSG="mensaje")
	alembic revision --autogenerate -m "$(MSG)"

db-reset: ## Resetear base de datos (⚠️ BORRA TODO)
	alembic downgrade base
	alembic upgrade head

test: ## Ejecutar todos los tests
	pytest

test-cov: ## Ejecutar tests con coverage
	pytest --cov=app --cov-report=html --cov-report=term
	@echo "\n✅ Reporte de coverage generado en htmlcov/index.html"

test-watch: ## Ejecutar tests en modo watch
	pytest-watch

clean: ## Limpiar archivos temporales
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage

docker-build: ## Construir imagen Docker
	docker build -t flujo-mcp:latest .

docker-up: ## Levantar stack completo con Docker
	docker-compose up -d --build
	@echo "✅ Stack completo levantado:"
	@echo "   - API: http://localhost:8000"
	@echo "   - Docs: http://localhost:8000/docs"

docker-down: ## Detener stack completo
	docker-compose down

docker-logs: ## Ver logs del stack completo
	docker-compose logs -f

superuser: ## Crear un superusuario
	python create_superuser.py

format: ## Formatear código con black e isort
	black app/ tests/
	isort app/ tests/

lint: ## Ejecutar linters (ruff o flake8)
	@which ruff > /dev/null && ruff check app/ tests/ || echo "⚠️ ruff no instalado"
	@which flake8 > /dev/null && flake8 app/ tests/ || echo "⚠️ flake8 no instalado"

env: ## Crear archivo .env desde .env.example
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Archivo .env creado. Por favor, revisa y ajusta los valores."; \
	else \
		echo "⚠️ El archivo .env ya existe."; \
	fi

setup: env install deps-up db-upgrade ## Setup inicial completo del proyecto
	@echo "\n✅ Setup completo!"
	@echo "   Ahora puedes ejecutar: make dev"

shell: ## Abrir shell de Python con el contexto de la app
	python -i -c "from app.core.database import engine; from app.models.user import User; from sqlmodel import Session, select"
