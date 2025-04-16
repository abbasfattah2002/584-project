#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

for f in $SCRIPT_DIR/*.py; do
	if [[ "$f" != "$SCRIPT_DIR/init.py" ]] then
		echo "Running $(basename $f)"
		python3 $f
		echo
	fi
done;