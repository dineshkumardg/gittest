To get a dev system up and running:

A: FOR SQLITE: ========================================

1. If you're using sqlite:

    python manage.py MY_PROJECT_CODE syncdb

..and set up the superuser account when prompted (as admin/admin)

2. setup the database config:

    python configure_project.py MY_PROJECT_CODE

B: FOR POSTGRES: ========================================

1. create the database:

a) change the create_db.sql script by dumping the models if required, ie:
    psql -U postgres _models_only/create_db.sql
    dump_models.sh
    merge any new model info into the create_models.sql for all projects (ie */create_models.sql)

b) now create the database that you want to use for development, eg:
    recreate.sh
    create_qa_product_users.sh MY_PROJECT_CODE
    
2. (Optional) use this to add the admin/admin user (if you didn't in step 1):
	python manage.py MY_PROJECT_CODE createsuperuser

C: FOR EITHER DATABASE: ========================================

4. Copy Admin media to web server:
    cd /usr/local/lib/python2.7/dist-packages/django/contrib/admin
    cp -r ./media /var/www

==================================================================

find '/mnt/DSP2/Production/Chatham_House/2012/SOURCE DATA/Non LWW meetings audio MP3 module 2' -name "*.mp3" -exec cp {} . \;
du -h .