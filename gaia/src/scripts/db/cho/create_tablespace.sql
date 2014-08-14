-- sudo mkdir -p /DB_DATA/cho/cho_tablespace
-- sudo chown -R postgres:postgres /DB_DATA/cho/cho_tablespace
-- sudo su - postgres 
-- psql -U postgres -p 5433
-- NOTE: password is postgres

CREATE TABLESPACE cho_tablespace LOCATION '/GAIA/cho/cho_tablespace';

-- \q
-- exit
