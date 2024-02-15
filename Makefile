.PHONY: install
# Automate first install
install:
	@echo ">>> Starting project"
	@echo ">>> Creating env file"
	@cp env.config env
	@echo ">>> Installing Dependences"
	@pip3 install -r requirements.txt
	@echo ">>> Creating Database"
	@python3 database.py


.PHONY: commit
# run send database to windows operation system
commit:
	@black .
	@isort .
	@flake8 --max-line-length 85


.PHONY: db
# run send database to windows operation system
db:
	@rm -r ./tmp/test_app.db
	@touch ./tmp/test_app.db
	@python3 database.py


.PHONY: run
# run process
run:
	@python3 main.py

