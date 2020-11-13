.PHONY: test clean build

clean:
	rm -rf build certbot_vault.egg-info

build:
	python setup.py bdist_wheel

test:
	PYTHONPATH=`pwd` PYTHONDONTWRITEBYTECODE=1 pytest -v -p no:cacheprovider tests/

