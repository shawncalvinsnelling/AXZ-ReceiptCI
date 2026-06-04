.PHONY: test verify receipt check

test:
	python -m pytest -q

verify:
	python scripts/verify_self.py

receipt:
	python -m axz_receiptci verify --project-name AXZ-ReceiptCI --test-cmd "python -m pytest -q" --out certificates

check:
	python -m axz_receiptci check certificates/certificate.json
