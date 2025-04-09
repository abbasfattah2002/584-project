CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;

\copy ( SELECT Year, Name, Gender FROM ssa_names WHERE difference(Name, 'Johnathan') = 4) TO './postgres/johnathan-soundex.csv' WITH CSV DELIMITER ',' HEADER;