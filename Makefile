.PHONY: test
test:
	python3 -m unittest -v

.PHONY: test_%
test_%:
	python3 -m unittest -v tests.Tests.test_$*
