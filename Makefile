all: snapshot

snapshot:
	node tasks/**/*.js

.PHONY: snapshot
