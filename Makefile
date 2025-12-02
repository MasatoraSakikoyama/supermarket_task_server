# Makefile for supermarket_task_server

# Alembic commands
.PHONY: migrate revision upgrade downgrade history

alembic-migrate:
	pipenv run alembic upgrade head

alembic-revision:
ifndef m
	$(error Usage: make revision m="your migration message")
endif
	pipenv run alembic revision --autogenerate -m "$(m)"

alembic-revision-empty:
ifndef m
	$(error Usage: make revision m="your migration message")
endif
	pipenv run alembic revision -m "$(m)"

alembic-upgrade:
ifndef rev
	$(error Usage: make upgrade rev=<revision>)
endif
	pipenv run alembic upgrade $(rev)

alembic-downgrade:
ifndef rev
	$(error Usage: make downgrade rev=<revision>)
endif
	pipenv run alembic downgrade $(rev)

alembic-history:
	pipenv run alembic history

# Linting and formatting commands
.PHONY: flake8 black isort lint

flake8:
	pipenv run flake8 app

black:
	pipenv run black app

isort:
	pipenv run isort app

# Run all linting and formatting tools
lint: isort black flake8
