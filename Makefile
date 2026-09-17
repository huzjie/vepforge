.PHONY: doctor run test serve clean

doctor:
	python -m vepforge.cli.main doctor

run:
	python -m vepforge.cli.main run --goal "$(GOAL)"

test:
	python -m pytest -q

serve:
	python -m vepforge.cli.main serve --port 8000

clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
