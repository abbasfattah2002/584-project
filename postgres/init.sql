CREATE TABLE ssa_names(
	Year INTEGER,
	Name VARCHAR(50),
	Gender CHAR(1),
	Count INTEGER
);

CREATE TABLE johnathan(
	Year INTEGER,
	Name VARCHAR(50),
	Gender CHAR(1)
);

CREATE TABLE katheryne(
	Year INTEGER,
	Name VARCHAR(50),
	Gender CHAR(1)
);

\copy ssa_names FROM 'fixed_ssa_data.csv' WITH (FORMAT CSV, HEADER)
\copy johnathan FROM 'names/johnathan.csv' WITH (FORMAT CSV, HEADER)
\copy katheryne FROM 'names/katheryne.csv' WITH (FORMAT CSV, HEADER)
