#!/bin/bash

for f in oracle/*.py; do
	if [[ "$f" != "oracle/init.py" ]] then
		echo "Running $f"
		python3 $f
		echo
	fi
done;