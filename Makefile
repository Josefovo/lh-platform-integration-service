venv_dir=venv
python3=python3

check: $(venv_dir)/packages-installed
	PYTHONDONTWRITEBYTECODE=1 \
	$(venv_dir)/bin/pytest -vv --tb=short --color=yes $(pytest_args) tests

run: $(venv_dir)/packages-installed
	$(venv_dir)/bin/lh-platform-integration-service --conf conf/lh-platform-integration-service.yaml $(args)

lint: $(venv_dir)/packages-installed
	test -x $(venv_dir)/bin/flake8 || $(venv_dir)/bin/pip install flake8
	$(venv_dir)/bin/flake8 . --extend-ignore=E261,E265,E501 --extend-exclude=venv,dist,build --show-source --statistics

$(venv_dir)/packages-installed: requirements.txt requirements-tests.txt setup.py
	test -d $(venv_dir) || $(python3) -m venv $(venv_dir)
	$(venv_dir)/bin/pip install -U pip wheel
	$(venv_dir)/bin/pip install -r requirements.txt
	$(venv_dir)/bin/pip install -r requirements-tests.txt
	$(venv_dir)/bin/pip install -e .
	touch $@

clean:
	rm -rfv build dist */__pycache__
	rm -rfv *.egg-info $(venv_dir)
