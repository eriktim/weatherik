all: update

update:
	cd lib && ./update.py

.PHONY: update
