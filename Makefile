.PHONY: install
# Automate first install
install:
	@echo ">>> Starting project"
	@echo ">>> Creating env file"
	@cp env.config env
	@echo ">>> Installing Dependences"
	@pip3 install -r requirements.txt
	@echo ">>> Creating Database"
	@touch ./tmp/test_app.db
	@python3 database.py


.PHONY: pre-commit
# run send database to windows operation system
pre-commit:
	@black .
	@isort .
	@flake8 --max-line-length 89


.PHONY: restart_db
# run send database to windows operation system
restart_db:
	@rm -r ./tmp/test_app.db
	@touch ./tmp/test_app.db
	@python3 database.py


.PHONY: run
# run process
run:
	@python3 main.py

