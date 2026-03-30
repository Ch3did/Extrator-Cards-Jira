.PHONY: pre-commit
# run send database to windows operation system
pre-commit:
	@black .
	@isort .
	@flake8 --max-line-length 89


.PHONY: run
# run process
run:
	@python3 main.py

