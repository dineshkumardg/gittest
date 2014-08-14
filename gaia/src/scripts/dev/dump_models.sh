#!/bin/sh
SQL_FILE=",create_models.sql"

echo "This dumps all of the required sql into ${SQL_FILE} "
echo "Note: the database (called _TMP_DEV_MODELS_ONLY_DB) must exist under the gaia user"
echo "You *MUST* _merge_ this into the db_scripts/<PROJECT>/create_models.sql files to use postgres (equivalent of syncdb)."
echo "You *CANNOT* just use it as is! *** WARNING ***"
echo
echo "check that all of the INSTALLED_APPS from your settings file are here"
echo
echo "Also, you *MUST* un-comment the lines that say:"
echo ""
echo "  'The following references should be added but depend on non-existent tables:'"
echo ""
echo "AND you *MUST* change all the types that need to be changed to BIG-types."
echo ""

rm -f $SQL_FILE
python manage.py 'JAMES_LINUX' sqlall contenttypes    >> $SQL_FILE
python manage.py 'JAMES_LINUX' sqlall auth            >> $SQL_FILE
python manage.py 'JAMES_LINUX' sqlall sessions        >> $SQL_FILE
python manage.py 'JAMES_LINUX' sqlall admin           >> $SQL_FILE
python manage.py 'JAMES_LINUX' sqlall admindocs       >> $SQL_FILE
python manage.py 'JAMES_LINUX' sqlall staticfiles     >> $SQL_FILE
python manage.py 'JAMES_LINUX' sqlall index           >> $SQL_FILE
python manage.py 'JAMES_LINUX' sqlall qa              >> $SQL_FILE
python manage.py 'JAMES_LINUX' sqlall asset_id        >> $SQL_FILE

