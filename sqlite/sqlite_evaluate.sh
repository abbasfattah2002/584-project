#!/bin/bash

(
	cd $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

	for f in *.sql; do
	if [[ "$f" != "init.sql" ]] then
		echo "Running $f"
		sqlite3 data.db < $f
		echo
	fi
	done;
)