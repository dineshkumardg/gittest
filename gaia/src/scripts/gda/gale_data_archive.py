import argparse
from logger import Logger
import logging
import psycopg2
import shutil
import urllib
import urllib2
import os


class GaleDataArchive:
    class UnableToGetItemsFromGaia(Exception):
        pass

    class UnableToLoginToGaia(Exception):
        pass

    class UnableToGetFixedXMLFromGaia(Exception):
        pass

    def __init__(self,
                 db_dns_host='gaia',
                 db_port='5432',
                 db_name='cho',
                 db_uid='gaia',
                 db_pwd='g818',
                 log_level=logging.INFO):
        self.logger = Logger().get_logger(self.__class__.__name__, log_level)
        self.logger.info('=' * 60)
        self._db_dns_host = db_dns_host
        self._db_port = db_port
        self._db_name = db_name
        self._db_uid = db_uid
        self._db_pwd = db_pwd

    def _connect_to_gaia_database(self):
        return psycopg2.connect(
            "host='%s' port='%s' dbname='%s' user='%s' password='%s'" %
            (self._db_dns_host, self._db_port, self._db_name, self._db_uid,
             self._db_pwd))

    def _disconnect_from_gaia_database(self, db_connection, db_cursor=None):
        if db_cursor is not None:
            db_cursor.close()

        if db_connection is not None:
            db_connection.close()

    def _get_items_from_gaia_db(self, sql, response_def):
        self.logger.debug('%s:%s %s' % (self._db_dns_host, self._db_port, sql))

        db_connection = None
        db_cursor = None
        try:
            db_connection = self._connect_to_gaia_database()
            db_cursor = db_connection.cursor()
            db_cursor.execute(sql)

            items = response_def(db_cursor)
            self.logger.info('%s' % len(items))
            return items
        except Exception as e:
            raise GaleDataArchive.UnableToGetItemsFromGaia(e)
        finally:
            self._disconnect_from_gaia_database(db_connection, db_cursor)

    def get_live_items_from_gaia_db(self, items_str_list=None):
        if items_str_list is None:
            sql = 'SELECT item.id, item.dom_name FROM public.item WHERE is_live = True ORDER BY item.date DESC;'
        else:
            sql = 'SELECT item.id, item.dom_name FROM public.item WHERE is_live = True AND dom_name IN '
            sql += '( ' + items_str_list + ' ) '
            sql += 'ORDER BY item.date DESC;'
        return self._get_items_from_gaia_db(
                sql,
                self._create_item_id_item_dom_name_list)

    def get_fixed_items_from_gaia_db(self):
        sql = 'SELECT item.id, item.dom_name FROM public.item WHERE item.has_changed = True AND item.is_live = True ORDER BY item.id ASC;'
        return self._get_items_from_gaia_db(
                sql,
                self._create_item_id_item_dom_name_list)

    def get_released_items_from_gaia_db(self):
        sql = 'SELECT item.id, item.dom_name FROM public.item, public.item_status '
        sql += 'WHERE item_status.item_id = item.id AND item_status.status = 700 AND item.is_live = True '
        sql += 'ORDER BY item.id DESC;'
        return self._get_items_from_gaia_db(
                sql,
                self._create_item_id_item_dom_name_list)

    def purge_unreleased_items_from_folder(self, released_items, folder):
        unreleased_items_in_folder = self._find_unreleased_items_in_folder(released_items, folder)

        item_count = 0
        for unreleased_item in unreleased_items_in_folder:
            item_count += 1
            folder_to_rm = '%s/%s' % (folder, unreleased_item)

            self.logger.info('%s/%s: rm %s ' % (item_count, len(unreleased_items_in_folder), folder_to_rm))
            self._rm_folder(folder_to_rm)

    def _find_unreleased_items_in_folder(self, released_items, folder):
        released_and_unreleased_items = os.listdir(folder)

        released_items_folders = []
        for released_item in released_items:
            live_item_id, item_dom_name = self.get_dom_id_dom_name(released_item)
            released_items_folders.append(item_dom_name)

        return [x for x in released_and_unreleased_items if x not in released_items_folders]

    def _create_item_id_item_dom_name_list(self, cursor):
        if cursor is None:
            raise GaleDataArchive.UnableToGetItemsFromGaia

        list_of_items = []
        for item in cursor:
            list_of_items.append({'%s' % item[0]: item[1]})
        return list_of_items

    def copy_all_item_versions_from_source_to_destination(self, live_items, source_folder, destination_folder):
        item_count = 0
        for item in live_items:
            live_item_id, item_dom_name = self.get_dom_id_dom_name(item)

            from_folder = '%s/%s/%s' % (source_folder, item_dom_name, live_item_id)
            to_folder = '%s/%s' % (destination_folder, item_dom_name)

            item_count += 1
            self.logger.info('%s/%s: cp %s %s ' % (item_count, len(live_items), from_folder, to_folder))
            try:
                self._copy_directory_tree(from_folder, to_folder)
            except OSError:
                shutil.rmtree(to_folder)
                self._copy_directory_tree(from_folder, to_folder)

    def _copy_directory_tree(self, from_folder, to_folder):
        # avoid using shutil.copytree across different file system types as can raise "[Errno 1] Operation not permitted"
        cmd = "cp -r '%s' '%s'" % (from_folder, to_folder)
        os.system(cmd)

    def get_fixed_xml_from_gaia_ws(self, item_id=None,
                                ws_url='http://127.0.0.1:8889/qa/ws/v1.0/item/%s',
                                timeout_secs=10,):
        if item_id is None:
            raise GaleDataArchive.UnableToGetFixedXMLFromGaia

        try:
            self.logger.debug(ws_url % item_id)
            return urllib2.urlopen(ws_url % item_id).read()
        except GaleDataArchive.UnableToLoginToGaia as e:
            raise GaleDataArchive.UnableToGetFixFromGaia(e)

    def login_to_gaia_website(self, django_login_url='http://127.0.0.1:8889/accounts/login/?next=/qa/',
                                uid='jsears',
                                pwd='goodgod2'):
        try:
            cookieHandler = urllib2.HTTPCookieProcessor()
            opener = urllib2.build_opener(cookieHandler)
            urllib2.install_opener(opener)

            self.logger.debug(django_login_url)
            opener.open(django_login_url)

            csrf_cookie = [x.value for x in cookieHandler.cookiejar if x.name == 'csrftoken'][0]
            login_data = urllib.urlencode(dict(username=uid, password=pwd, csrfmiddlewaretoken=csrf_cookie))
            opener.open(django_login_url, login_data)
        except Exception as e:
            raise GaleDataArchive.UnableToLoginToGaia(e)

    def get_dom_id_dom_name(self, item_dict):
        item_keys = item_dict.keys()
        return item_keys[0], item_dict[item_keys[0]]

    def save_fixed_xml_into_folder(self, root_folder, item_dom_name, item_id, fixed_xml):
        fname = '%s/%s/%s/%s.xml' % (root_folder, item_dom_name, item_id, item_dom_name)
        self.logger.info('write %s' % fname)

        try:
            with open(fname, 'w') as f:
                f.write(fixed_xml)
        except IOError as e:
            self.logger.warn(str(e))

    def _rm_gdom_from_a_folder(self, root_folder, item_dom_name, live_item_id):
        self._rm_gdom_from_live_version(root_folder, item_dom_name, live_item_id)
        #self._rm_dead_versions(root_folder, item_dom_name, live_item_id)

    def _rm_gdom_from_live_version(self, root_folder, item_dom_name, live_item_id):
        live_item_id_root_dir = '%s/%s' % (root_folder, item_dom_name)
        self.logger.debug(live_item_id_root_dir)

        self._rm_folder('%s/page' % live_item_id_root_dir)
        self._rm_folder('%s/chunk' % live_item_id_root_dir)
        self._rm_folder('%s/document' % live_item_id_root_dir)
        self._rm_folder('%s/link' % live_item_id_root_dir)

        self._rm_gdom_files(live_item_id_root_dir)

    def _rm_dead_versions(self, root_folder, item_dom_name, live_item_id):
        item_dom_name_root_dir = '%s/%s' % (root_folder, item_dom_name)

        all_version_folders = [name for name in os.listdir(item_dom_name_root_dir) if os.path.isdir(os.path.join(item_dom_name_root_dir, name))]
        all_version_folders.remove(str(live_item_id))

        for dead_version in all_version_folders:
            fpath = '%s/%s' % (item_dom_name_root_dir, dead_version)

            try:
                self.logger.debug('rm %s' % fpath)
                shutil.rmtree(fpath)
            except OSError as e:
                self.logger.warn(e)

    def _rm_folder(self, fpath):
        try:
            self.logger.debug('rm %s' % fpath)
            shutil.rmtree(fpath)
        except OSError as e:
            self.logger.warn(e)

    def _rm_gdom_files(self, root_dir):
        thumbnail_files = [f for f in os.listdir(root_dir) if f.endswith("thumbnail.jpg")]
        for thumbnail in thumbnail_files:
            self._rm_gdom_file('%s/%s' % (root_dir, thumbnail))

        self._rm_gdom_file('%s/manifest.md5' % root_dir)

    def _rm_gdom_file(self, fpath):
        try:
            self.logger.debug('rm %s' % fpath)
            os.remove(fpath)
        except OSError as e:
            self.logger.warn(e)

    def rm_gdom(self, items, gda_folder):
        item_count = 0
        for item in items:
            item_id, item_dom_name = self.get_dom_id_dom_name(item)

            item_count += 1
            self.logger.info('%s/%s: %s' % (item_count, len(items), item_dom_name))
            self._rm_gdom_from_a_folder(gda_folder, item_dom_name, item_id)

    def write_fixed_xml(self,
                        fixed_items,
                        gda_folder,
                        django_login_url='http://127.0.0.1:8889/accounts/login/?next=/qa/',
                        ws_url='http://127.0.0.1:8889/qa/ws/v1.0/item/%s'):

        self.login_to_gaia_website(django_login_url)  # get CSCR

        item_count = 0
        for item in fixed_items:
            item_id, item_dom_name = self.get_dom_id_dom_name(item)

            item_count += 1
            self.logger.info('%s/%s: %s' % (item_count, len(fixed_items), item_dom_name))

            fixed_xml = self.get_fixed_xml_from_gaia_ws(item_id, ws_url)
            self.save_fixed_xml_into_folder(gda_folder, item_dom_name, item_id, fixed_xml)


"""
assumes /mnt/Archive has 'Everyone' on NTFS ACL for rw - this allows cifs mount'ing; smb:// mounting 'just works' for rw

nohup python gale_data_archive.py -action copy_all_items > log &

find . -type d -name 'link' -exec ls {} \;
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cho gale data archive utility')
    parser.add_argument('-action',
                        choices=['copy_all_items', 'rm_gdom', 'write_fixed', 'purge_unreleased'],
                        help='action to invoke (in order)')
    args = parser.parse_args()

    # production database; code run locally - using nfs
    gda = GaleDataArchive(db_dns_host='10.179.176.181',
                 db_port='5432',
                 db_name='cho',
                 db_uid='gaia',
                 db_pwd='g818')

    # sudo mount -t cifs //ukandprodfs/Archive/Chatham_House /mnt/Archive -o username=jsears,password=...,iocharset=utf8,file_mode=0777,dir_mode=0777
    # sudo umount /mnt/Archive  < rm any tmp cifs locks within mount
    gda_folder = '/mnt/Archive/gda/m1'

    live_items = gda.get_live_items_from_gaia_db()

    gda.logger.info('=' * 30)

    if args.action == 'copy_all_items':
        gda.copy_all_item_versions_from_source_to_destination(live_items, '/GAIA/cho/web_root', gda_folder)
    elif args.action == 'rm_gdom':
        gda.rm_gdom(live_items, gda_folder)
    elif args.action == 'write_fixed':
        fixed_items = gda.get_fixed_items_from_gaia_db()
        gda.write_fixed_xml(fixed_items,
                            gda_folder,
                            django_login_url='http://10.179.176.181:8004/accounts/login/?next=/qa/',
                            ws_url='http://10.179.176.181:8004/qa/ws/v1.0/item/%s'
                            )
    elif args.action == 'purge_unreleased':
        released_items = gda.get_released_items_from_gaia_db()
        gda.purge_unreleased_items_from_folder(released_items, gda_folder)
    else:
        parser.print_help()

    gda.logger.info('FINISHED')
