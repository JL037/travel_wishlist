.PHONY: secure run test clean docker docker-stop docker-rebuild docker-logs psql
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "🛠️  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
run: ## Start FastAPI app with uvicorn
	uvicorn app.main:app --reload

test: ## Run tests with pytest
	pytest

secure: ## Run Bandit and Gitleaks for security scan
	@echo "🔍 Running Bandit (Python Security Scanner)..."
	bandit -r app migrations main.py
	@echo "✅ Bandit check passed!"
	@echo "🔍 Running Gitleaks (Secrets Scanner)..."
	gitleaks detect --source=. --no-git --report-format=cli
	@echo "✅ Gitleaks check passed!"

clean: ## Remove __pycache__ folders
	find . -type d -name "__pycache__" -exec rm -r {} +

docker: ## Start all Docker services (with build, detached)
	docker-compose up --build -d

docker-stop: ## Stop and remove Docker containers
	docker-compose down

docker-rebuild: ## Rebuild and restart all Docker services
	docker-compose down && docker-compose up --build -d

docker-logs: ## View live logs from all Docker services
	docker-compose logs -f

format: ## Auto-format Python code with Black
	black .

lint: ## Run Ruff linter on the codebase
	ruff check .

psql: ## run postgresql
	psql -U jaredlemler -h localhost -d travel_wishlist
