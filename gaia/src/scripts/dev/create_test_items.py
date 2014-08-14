import os
import hashlib
import argparse
import shutil
import random
import itertools
from collections import OrderedDict
from test_utils.create_cho_xml import CreateChoXML
from test_utils.create_cho import conference


class Item():
    item_template = 'cho_%s_2010_0001_%03d_%03d'

    def __init__(self, item_type, item_name_stem, containing_dir, item_num, data_type):
        self.item_type = item_type
        self.item_name_stem = item_name_stem
        self.item_num = item_num
        self.data_type = data_type
        
        if self.item_type == 'bcrc' or self.item_type == 'related_iaxx':
            self.item_dir = os.path.join(containing_dir, '%s_0000' % self.item_name_stem)
        else:    
            self.item_dir = os.path.join(containing_dir, '%s_0001' % self.item_name_stem)
        
        if not os.path.exists(self.item_dir):
            os.makedirs(self.item_dir)

    def create(self, num_pages, img_file_ext, item_type, data_type):
        fnames = []
        if num_pages == 0:
            num_pages = random.randrange(1, 60)

        fnames.append(self.create_xml_asset(num_pages, img_file_ext))

        for i in range(1, num_pages + 1):
            fnames.append(self._create_asset_img(i, img_file_ext, item_type))

        if data_type == 'Audio' or data_type == 'Video':
            fnames.append(self._create_asset_mp(data_type))#

        self._create_manifest(fnames)
        self._mark_ready()

    def create_xml_asset(self, num_pages, img_file_ext):
        return CreateChoXML.create(num_pages,
                                   img_file_ext,
                                   item_type=self.item_type,
                                   item_num=self.item_num,
                                   asset_dir=self.item_dir,
                                   item_name_stem=self.item_name_stem,
                                   fpath_xsd='../../gaia/config/dtds/chatham_house.xsd',
                                   data_type=self.data_type)

    def _create_asset_mp(self, data_type):
        if data_type == 'Audio':
            test_mp_fpath = 'audio.mp3'
            asset_fname = '%s_%04d.%s' % (self.item_name_stem, 1, 'mp3')

        if data_type == 'Video':
            test_mp_fpath = 'video.mp4'
            asset_fname = '%s_%04d.%s' % (self.item_name_stem, 1, 'mp4')

        good_test_mp = os.path.join(os.path.dirname(__file__), 'test_mp', test_mp_fpath)
        dst = os.path.join(self.item_dir, asset_fname)

        try:
            shutil.copy(good_test_mp, dst)
        except Exception, e:
            print 'EXITING: COULD NOT COPY %s TO %s (%s)' % (good_test_mp, self.item_dir, str(e))  

        return asset_fname

    def _create_asset_img(self, i, file_ext, item_type):
        asset_fname = '%s_%04d.%s' % (self.item_name_stem, i, file_ext)

        good_test_image = os.path.join(os.path.dirname(__file__), 'test_images', self._item_img_fpath(item_type))
        dst = os.path.join(self.item_dir, asset_fname)
        try:
            shutil.copy(good_test_image, dst)
        except Exception, e:
            print 'EXITING: COULD NOT COPY %s TO %s (%s)' % (good_test_image, self.item_dir, str(e))

        return asset_fname

    def _item_img_fpath(self, item_type):
        if item_type == 'iaxx':
            img_fpath = 'cho_iaxx_1963_0039_000_0013.jpg'
        elif item_type == 'meet':
            img_fpath = 'cho_meet_1945_1132_000_0001.jpg'
        elif item_type == 'book':
            img_fpath = 'cho_book_1963_0000_000_0001.jpg'
        elif item_type == 'bcrc':
            img_fpath = 'cho_bcrc_1933_0001_000_0001.jpg'
        else: # rpax
            img_fpath = 'cho_rpax_1943_notes_000_0001.jpg'

        return img_fpath

    def _create_manifest(self, fnames):
        manifest_file = open(os.path.join(self.item_dir, 'manifest.md5'), 'w+')

        for fname in fnames:
            f = open(os.path.join(self.item_dir, fname), 'rb')
            m = hashlib.md5()
            m.update(f.read())
            checksum = m.hexdigest()
            line = '%s  %s' % (checksum, fname)
            manifest_file.write(line + '\n')

        manifest_file.close()

    def _mark_ready(self):
        f = open(os.path.join(self.item_dir, '_status_READY.txt'), 'w+')
        f.write('')
        f.close

def create_items(items_dir, num_items, item_type, num_pages, img_file_ext, item_start, data_type, create_related):
    print '*** items_dir="%s", num_items=%s, item_type="%s", num_pages=%s, img_file_ext="%s", item_start=%s, data_type="%s", create_related="%s"' % (items_dir, num_items, item_type, num_pages, img_file_ext, item_start, data_type, create_related)
     
    increasing = False
        
    if num_pages == -1:
        increasing = True

    item_number = 0
    related_iaxx_name_stems=['cho_iaxx_1926_0005_000', 'cho_iaxx_1927_0006_000', 'cho_iaxx_1928_0007_000', 'cho_iaxx_1929_0008_000',
                             'cho_iaxx_1930_0009_000', 'cho_iaxx_1931_0010_000', 'cho_iaxx_1932_0011_000', 'cho_iaxx_1933_0012_000',
                             'cho_iaxx_1934_0013_000', 'cho_iaxx_1935_0014_000', 'cho_iaxx_1936_0015_000', 'cho_iaxx_1937_0016_000',
                             'cho_iaxx_1938_0017_000', 'cho_iaxx_1939_0018_000', 'cho_iaxx_1944_0020_000', 'cho_iaxx_1945_0021_000',
                             'cho_iaxx_1946_0022_000', 'cho_iaxx_1947_0023_000', 'cho_iaxx_1948_0024_000', 'cho_iaxx_1949_0025_000',
                             'cho_iaxx_1950_0026_000', 'cho_iaxx_1951_0027_000', 'cho_iaxx_1952_0028_000', 'cho_iaxx_1953_0029_000',
                             'cho_iaxx_1954_0030_000', 'cho_iaxx_1955_0031_000', 'cho_iaxx_1956_0032_000', 'cho_iaxx_1957_0033_000',
                             'cho_iaxx_1958_0034_000', 'cho_iaxx_1959_0035_000', 'cho_iaxx_1960_0036_000', 'cho_iaxx_1961_0037_000',
                             'cho_iaxx_1962_0038_000',
                             ]
    if create_related == True:
        num_items = len(related_iaxx_name_stems)
        item_type = "related_iaxx"
        num_pages = 3

    for i in range(item_start, item_start + num_items):
        if item_type == 'bcrc':
            item_name_stem = _get_conf_series_item_name_stem(conference.mcodes, num_items, item_number)
            item_number += 1
        elif item_type == 'related_iaxx':
            item_name_stem = related_iaxx_name_stems[item_number]
            item_number += 1
        else:
            item_name_stem = 'cho_' + item_type + '_2010_7771_%03d' % i
        item = Item(item_type, item_name_stem, items_dir, i, data_type)

        if increasing:
            item.create(i, img_file_ext, item_type, data_type)
        else:
            item.create(num_pages, img_file_ext, item_type, data_type)

def _get_conf_series_item_name_stem(conf_dict, num_items, item_number):
    sorted_conf_dict = OrderedDict(sorted(conf_dict.items(), key=lambda t: t[0]))
    conf_series_names = list(itertools.islice(sorted_conf_dict.iteritems(), num_items))
    item_names = conf_series_names[item_number]
    item_name = item_names[0]
    item_name_stem = item_name.rsplit('_', 1)[0]
    
    return item_name_stem

'''
see /gaia/src/project/cho/gaia_dom_adapter/factory.py for supported file types e.g. iaxx; meet

sample usage:
    cd ~/GIT_REPOSE/system_test/gaia/src/scripts/dev

    py create_test_items.py --item_type=iaxx --num_pages=1 --num_items=1
    py create_test_items.py --item_type=meet --num_pages=1 --num_items=1 --data_type=Audio
    py create_test_items.py --item_type=meet --num_pages=1 --num_items=1 --data_type=Video
    py create_test_items.py --item_type=iaxx --num_items=10 --num_pages=-1
    py create_test_items.py --create_related=True
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--items_dir', default='./,test_items',  help='where to create items')
    parser.add_argument('--num_items', default=3, type=int, help='number of items to create')
    parser.add_argument('--item_type',
                        default='iaxx',
                        choices=['meet', 'iaxx', 'book', 'bcrc', 'rpax'], # TODO 'rfpx', 'rsxx', 'diax', 'siax'],
                        help='what sort of item to create')
    parser.add_argument('--num_pages', default=0, type=int, help='number of pages to create for each item (0 for random; -1=increasing)')
    parser.add_argument('--img_file_ext', default='jpg', help='image file type')
    parser.add_argument('--item_start', default=1, type=int, help='starting id for items, eg to continue after previous run')
    parser.add_argument('--data_type', default='', choices=['', 'Audio', 'Video'], help='on meet creates /chapter/metadataInfo/relatedMedia')
    parser.add_argument('--create_related', default=False, type=bool, choices=[True, False], help='creates a 3 item set, featuring unidirectional + bi-directional + transitive /chapter/page/article/text/textclip/relatedDocument elements')
    args = parser.parse_args()

    create_items(args.items_dir, args.num_items, args.item_type, args.num_pages, args.img_file_ext, args.item_start, args.data_type, args.create_related)
    
    if args.create_related == True:
        print """
                 - unidirectional cho_iaxx_1926_0005_000_0000 points to cho_iaxx_1927_0006_000_0000

                 - bidirectional cho_iaxx_1929_0008_000_0000 points to cho_iaxx_1928_0007_000_0000
                   and cho_iaxx_1928_0007_000_0000 points back to cho_iaxx_1929_0008_000_0000

                 - cho_iaxx_1930_0009_000_0000 points to a non exsisting item cho_iaxx_NONEXIST_0008_000_0000, i.e. broken link

                 - cho_iaxx_1931_0010_000_0000 points to cho_iaxx_1932_0011_000_0000
                   and cho_iaxx_1932_0011_000_0000 points to a non exsisting item cho_iaxx_NONEXIST_0012_000_0000, i.e. broken link

                 - cho_iaxx_1933_0012_000_0000 points to a non exsisting item cho_iaxx_NONEXIST_0010_000_0000, i.e. broken link
                   and cho_iaxx_1934_0013_000_0000 points to cho_iaxx_1933_0012_000_0000

                 - cho_iaxx_1935_0014_000_0000 points to cho_iaxx_1936_0015_000_0000
                   and also points to a non exsisting item cho_iaxx_NONEXIST_0015_000_0000, i.e. broken link

                 - cho_iaxx_1937_0016_000_0000 points to cho_iaxx_1938_0017_000_0000 and cho_iaxx_1938_0017_000_0000 points back to cho_iaxx_1937_0016_000_0000
                   both cho_iaxx_1937_0016_000_0000 and cho_iaxx_1938_0017_000_0000 point to a non exsisting item cho_iaxx_NONEXIST_0017_000_0000, i.e. broken link

                 - unidirectional cho_iaxx_1939_0018_000 points to cho_iaxx_1944_0020_000 which points to cho_iaxx_1945_0021_000
                 
                 - cho_iaxx_1946_0022_000 points to cho_iaxx_1947_0023_000 which points to cho_iaxx_1948_0024_000 
                   which pointsback to cho_iaxx_1946_0022_000
                 
                 - cho_iaxx_1949_0025_000 points to cho_iaxx_1950_0026_000, 
                   cho_iaxx_1951_0027_000 also points to cho_iaxx_1950_0026_000
                 
                 - cho_iaxx_1952_0028_000 points to cho_iaxx_1953_0029_000 which points to cho_iaxx_1954_0030_000
                   which points to a non existing item cho_iaxx_NONEXIST_0017_000_0000, i.e broken link
                   
                 - cho_iaxx_1955_0031_000 points to cho_iaxx_1956_0032_000 which points to cho_iaxx_1957_0033_000
                   which points back to cho_iaxx_1956_0032_000
                 
                 - cho_iaxx_1958_0034_000 points to cho_iaxx_1959_0035_000 which points to cho_iaxx_1960_0036_000
                   and also points to a non existing item cho_iaxx_NONEXIST_0036_000_0000, i.e. broken link
                 
                 - cho_iaxx_1962_0038_000 link to non existing pgref and article in  cho_iaxx_1961_0037_000
                   
              """
