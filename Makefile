build:
	poetry build
install:
	poetry install
package-install:
	python3 -m pip install dist/*.whl
package-uninstall:
	python3 -m pip uninstall dist/*.whl
lint:
	poetry run flake8 page_loader
tcov:
	poetry run pytest --cov=page_loader --cov-report xml tests/