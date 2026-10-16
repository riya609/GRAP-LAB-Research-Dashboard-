install:
	pip install -r requirements.lock
lock:
	python scripts/lock_prereg.py
verify:
	python scripts/lock_prereg.py --verify
test:
	pytest -q
synthetic:
	PYTHONPATH=src python -m grapkit.run --synthetic
real:
	PYTHONPATH=src python -m grapkit.run
