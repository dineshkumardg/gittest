-- on windows? or Ubunto 12.04:
-- LC_COLLATE = 'en_GB.UTF-8'
-- LC_CTYPE = 'en_GB.UTF-8'
-- ..should work on Linux ???? (ref $LC_CTYLE/$LANG
-- LC_COLLATE = 'en_GB.utf8'
-- LC_CTYPE = 'en_GB.utf8'
-- ENCODING = 'UTF8'
CREATE DATABASE "cho"
  WITH OWNER = gaia
       TABLESPACE = cho_tablespace
       CONNECTION LIMIT = -1;
