CREATE TABLE ssa_names(
  Year  	SMALLINT   	NOT NULL,
  Name  	VARCHAR(50) NOT NULL,
  Gender 	CHAR(1)   	NOT NULL,
  Count  	INTEGER   	NOT NULL
);

CREATE TABLE johnathan(
  Year  	SMALLINT   	NOT NULL,
  Name  	VARCHAR(50) NOT NULL,
  Gender 	CHAR(1)   	NOT NULL
);

CREATE TABLE katheryne(
  Year  	SMALLINT   	NOT NULL,
  Name  	VARCHAR(50) NOT NULL,
  Gender 	CHAR(1)   	NOT NULL
);

.mode csv

.import fixed_ssa_data.csv ssa_names
.import --skip 1 names/johnathan.csv johnathan
.import --skip 1 names/katheryne.csv katheryne
