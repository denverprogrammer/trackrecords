login:
	docker login -u `git config user.name` -p `git config user.token` ghcr.io

create_environment:
	poetry shell

regenerate_lockfile:
	poetry lock --regenerate
	poetry install

install_dependencies:
	poetry shell
	poetry install

lint:
	black --check .
	flake8 .
	isort --check-only .
	toml-sort --in-place pyproject.toml
