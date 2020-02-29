req:
	poetry export -f requirements.txt > requirements.txt --without-hashes

test:
	pytest -s -v

cov:
	coverage run -m pytest -s -v
	coverage report
	coverage html
	coverage xml
