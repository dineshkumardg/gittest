import glob
import errno
import stat
import os
import csv
import gzip
import sys
import argparse
import shutil
from lxml import etree as ET


class GenerateFeedReport():
    def __init__(self, reports_folder, feedfiles_folder):
        self.file_names = []
        self.xml_name = ''
        self.split_xmls = []

        if sys.platform == 'win32':
            self.home = os.path.expanduser('~')
        else:
            self.home = os.environ['HOME']

        self.rows = []
        self.header = (['FEED_FILE_NAME', 'FUNCTIONAL_TYPE', 'DOCUMENT_INSTANCES', 'M-CODES','PSMID', 'ASSET_IDs'])
        self.namespace = {'gold':"http://www.gale.com/gold", 'gift-doc' : "http://www.gale.com/goldschema/gift-doc", 'meta': "http://www.gale.com/goldschema/metadata"}
        self.temp_dir = os.path.join(self.home + '/FTP_WORK_DIR')
        self.gz_dir = os.path.join(self.temp_dir + '/gz')
        self.xml_dir = os.path.join(self.temp_dir + '/xml')
        self.csv_dir = os.path.join(reports_folder)
        self.feedfiles_folder = os.path.join(feedfiles_folder)

    def check_dir(self):
        # creates all working directories
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
            os.makedirs(self.gz_dir)
            os.makedirs(self.xml_dir)
        # checks if feedfile folder exists
        if not os.path.exists(self.feedfiles_folder):
            print "Please provide the correct path to Folder containing feed files !!"
            print "STOPPED !!!!!"
            sys.exit()
        else:
            # checks if the feedfile folder has any files init
            counter = 0
            dirs = os.listdir(self.feedfiles_folder)
            if not dirs:
                print "The Feed file folder selected is Empty!!"
                print "STOPPED !!!!!"
                sys.exit()
            else:
                for every_dir in dirs:
                    if not ".gz" in every_dir:
                        counter+=1
                        if counter == len(dirs):
                            print "No .gz files found in the feed files folder!!"
                            print "STOPPED !!!!!"
                            sys.exit()
        # checks if the reports folder exists
        if not os.path.exists(self.csv_dir):
            print "Please provide the correct Folder path to output your reports !!"
            print "STOPPED !!!!!"
            sys.exit()

    def list_sort(self,gz_name_list, splitter_element, index):
        # function to sort the file names in accordance with the dates(in names)       
        sorted_list = []
        year_list = []

        for gz in gz_name_list:
            year_list.append(gz.split(splitter_element)[index])
        year_list.sort()

        for year in year_list:
            for gz in gz_name_list:
                if str(year) in gz:
                    if not gz in sorted_list:
                         sorted_list.append(gz)
        return sorted_list

    def copy_local_files(self):
        # alternate/function to copy .gz files from local folder instead of FTP        
        gz_path = self.feedfiles_folder
        destpath = self.gz_dir

        for root, dirs, files in os.walk(gz_path):
            for each_file in files:
                if each_file.endswith(".gz"):
                    shutil.copy2(os.path.join(gz_path, each_file), os.path.join(destpath, each_file))
                    self.file_names.append(each_file)
    
        return self.file_names

    def unzip_files(self):
        # function to unzip the .gz files copied from lst
        for xml_file in range(0, len(self.file_names)):
 
            gz_fd = gzip.GzipFile(os.path.join(self.home + ('/FTP_WORK_DIR/gz/'+str(self.file_names[xml_file]))) , 'rb')

            file_names = self.file_names[xml_file].split('.')  # ['PSM-CHOA_20130726_158', 'xml', 'gz']
            xml_fd = open(os.path.join(self.home + ('/FTP_WORK_DIR/xml/'+str(file_names[0])+'.xml')), 'wb')

            buffer = True
            while buffer:
              buffer = gz_fd.read(1024)
              xml_fd.write(buffer)

    def split_xml(self):
        # function to split xml's into document instances
        self.split_xmls = []

        header = '''<gold:feed xmlns:essay="http://www.gale.com/goldschema/essay" xmlns:gold="http://www.gale.com/gold" xmlns:gift-doc="http://www.gale.com/goldschema/gift-doc" xmlns:dir="http://www.gale.com/goldschema/dir" xmlns:vault-link="http://www.gale.com/goldschema/vault-linking" xmlns:meta="http://www.gale.com/goldschema/metadata" xmlns:table="http://www.gale.com/goldschema/table" xmlns:xatts="http://www.gale.com/goldschema/xatts" xmlns:index="http://www.gale.com/goldschema/index" xmlns:mla="http://www.gale.com/goldschema/mla" xmlns:media="http://www.gale.com/goldschema/media" xmlns:tt="http://www.w3.org/ns/ttml" xmlns:list="http://www.gale.com/goldschema/list" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:etoc="http://www.gale.com/goldschema/etoc" xmlns:verse="http://www.gale.com/goldschema/verse" xmlns:pres="http://www.gale.com/goldschema/pres" xmlns:pub-meta="http://www.gale.com/goldschema/pub-meta" xmlns:shared="http://www.gale.com/goldschema/shared" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:math="http://www.w3.org/1998/Math/MathML" id="NOINDEX-CHOA_20130726_157" xsi:schemaLocation="..\..\..\..\..\GIFT\/feed_schemas\/feed.xsd">
'''
        footer = '''<gold:metadata><gold:feed-type>PSM</gold:feed-type><gold:document-schema>gift_document.xsd</gold:document-schema><gold:schema-version>2.5</gold:schema-version><gold:document-id-path>//gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value</gold:document-id-path><gold:document-mcode-path>//gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:mcode</gold:document-mcode-path><gold:number-of-documents>14</gold:number-of-documents><gold:feed-status>New-Replace</gold:feed-status></gold:metadata></gold:feed>
'''
        file_count = 1
        file_lines = ''
        with open(self.xml_name, "r") as feed_file:
            for line in feed_file:
                if  'feed.xsd' in line:
                    line = '<gold:document-instance>'

                file_lines += line
                if "</gold:document-instance>" in line:
                    xml_fname = str(self.xml_name.split("/")[-1])
                    
                    if sys.platform == 'win32':
                        xml_fname = str(self.xml_name.split('\\')[-1])
                        doc_inst_fname = os.path.join(self.home + ('\\FTP_WORK_DIR\\xml\\%s_%010d.xml' % (xml_fname[:-4], file_count) ))
                    else:
                        xml_fname = str(self.xml_name.split("/")[-1])
                        doc_inst_fname = os.path.join(self.home + ('/FTP_WORK_DIR/xml/%s_%010d.xml' % (xml_fname[:-4], file_count) )) 
                    
                    self.split_xmls.append(doc_inst_fname)
                    
                    doc_inst_fd = open(doc_inst_fname, "w")
                    doc_inst_fd.write(header)
                    doc_inst_fd.write(file_lines)
                    doc_inst_fd.write(footer)

                    file_lines = ''
                    file_count += 1

    def process_xml(self):
        # function to process the unzipped xml files
        name_list = []
        doc_list = []
        func_type_list = []
        mcode_list = []
        self.rows = []

        for split_xml in self.split_xmls:

            if sys.platform == 'win32':
                split_xml = split_xml.replace('/', '\\')
                file_name = self.xml_name.split('\\')[-1]
            else:
                file_name = self.xml_name.split('/')[-1]

            name_list = (file_name + '.gz' )
            tree = ET.parse(split_xml)
            func_type_list = self._find_func_type_value(tree)
            doc_list = len(self.split_xmls)
            mcode_list = self._find_mcode(tree)
            psmid_list_tmp = self._find_psmid(tree)
            asset_id_list = self._find_asset_id(tree)
            tree = ''
            for x in range (0, max(len(psmid_list_tmp),len(asset_id_list))):
                row = []
                row.append(name_list)
                row.append(func_type_list)
                row.append(doc_list)
                if x < len(mcode_list):
                    row.append(mcode_list[x])
                else:
                    row.append(" ")
                #row.append((str(mcode_list)).strip('[]'))
                if x < len(psmid_list_tmp):
                    row.append(psmid_list_tmp[x])
                else:
                    row.append(" ")
                if x < len(asset_id_list):
                    row.append(asset_id_list[x])
                else:
                    row.append(" ")
                self.rows.append(row)

            self.rows.sort (key = lambda row: (row[4].replace("_","")[-15:]))
        self.rows.insert(0, self.header)
        self.output_csv(self.rows, (self.xml_name.split("/")[-1]))

    def _count_doc_instances(self, tree):
        #function to calculate the no. of document instances
        record = []
        record = tree.xpath('/gold:feed/gold:document-instance', namespaces ={'gold':"http://www.gale.com/gold"})
        doc_number = len(record)
        return doc_number

    def _find_func_type_value(self, tree):
        #function to findout the functional type values    
        func = tree.xpath('/gold:feed/gold:document-instance/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:descriptive-indexing/meta:indexing-term/meta:term/meta:term-type', namespaces = self.namespace)
        
        for i in range(0, len(func)):
            if func[i].text == 'FUNC_TYPE':
                func_value = tree.xpath('/gold:feed/gold:document-instance/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:descriptive-indexing/meta:indexing-term/meta:term/meta:term-value', namespaces = self.namespace)
                return func_value[i].text

    def _find_mcode(self, tree):
        #function to calculate the MCODE values    
        mcode = tree.xpath('/gold:feed/gold:document-instance/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:mcode', namespaces = self.namespace)
        list_of_mcodes = []

        for mcode_value in mcode:
            list_of_mcodes.append(mcode_value.text)
        return list_of_mcodes

    def _find_psmid(self, tree):
        #function to find the PSM-ID values    
        list_of_psmid_values = []
        psmid = tree.xpath('/gold:feed/gold:document-instance/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:bibliographic-ids/meta:id/@type', namespaces = self.namespace)
        psmid_value = tree.xpath('/gold:feed/gold:document-instance/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:bibliographic-ids/meta:id/meta:value', namespaces = self.namespace)
        
        for psmidlen in range(0, len(psmid)):
            if psmid[psmidlen] == "PSM":
                list_of_psmid_values.append(psmid_value[psmidlen].text)
        return list_of_psmid_values       

    def _find_asset_id(self, tree):
        # function to find the Asset ID values
        asset = tree.xpath('/gold:feed/gold:document-instance/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id/@type', namespaces = self.namespace)
        asset_id = tree.xpath('/gold:feed/gold:document-instance/gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id/meta:value', namespaces = self.namespace)
        list_of_asset_ids = []

        for assetlen in range(0, len(asset)):
            if asset[assetlen] == 'Gale asset':
                list_of_asset_ids.append(asset_id[assetlen].text)
        return list_of_asset_ids

    def output_csv(self, rows, csv_file_name):
        # function to output CSV files with all the Values derived from the xml's
        if sys.platform == 'win32':
            x = csv_file_name.split("\\")[-1]
            y = x.split('.')[0]
            csv_file_path = os.path.join(self.csv_dir + ('/feed_' + y +'.csv'))
        else:
            csv_file_path = os.path.join(self.csv_dir + ('/feed_' + str((csv_file_name.split("."))[0])+'.csv'))

        csv_file = open(csv_file_path,"w")
        out = csv.writer(csv_file, delimiter=',',quoting=csv.QUOTE_ALL, lineterminator='\n')

        for row in self.rows:
            out.writerow(row)
        csv_file.close()
        print 'feed file report generated'

    def clean_up(self):
        #removes all the temp dirs and generates a zip file of all the csv so its easire to attach in email , removes all the .csv file
        if os.path.isdir(self.temp_dir):
            if sys.platform == 'win32':
                shutil.rmtree(self.temp_dir, ignore_errors=False, onerror=self._handle_remove_readonly)
            else:
                shutil.rmtree(self.temp_dir)

    def _handle_remove_readonly(self, func, path, exc):
        excvalue = exc[1]
        if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
            os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
            func(path)
        else:
            raise

'''
cd $HOME/GIT_REPOS/gaia/src/scripts/reports/feed_file

python generate_feed_report.py --feedfiles_folder=$HOME/GIT_REPOS/gaia/src/scripts/reports/feed_file/test_data/actual_gz --reports_folder=$HOME/GIT_REPOS/gaia/src/scripts/reports/feed_file/test_data

diff test_data/*.csv test_data/expected_csv/*.csv
'''
if __name__ == "__main__":
    if not len(sys.argv) == 3:
        print "** FAIL: Please provide a source folder with feed files and a destination folder for the reports! **"
        print 'please use (full paths): --feedfiles_folder=... AND --reports_folder=...'
        sys.exit()
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('--feedfiles_folder', help='folder holding gz feed files')
        parser.add_argument('--reports_folder', help='folder to output feed-file reports')
        args = parser.parse_args()

        feed = GenerateFeedReport(args.reports_folder, args.feedfiles_folder)
        print "STARTED"
        feed.clean_up()
        feed.check_dir()
        feed.copy_local_files()
        feed.unzip_files()
        print "Unzipped xmls"

        xml_files = glob.glob(feed.xml_dir + '/*.xml')
        print xml_files

        for xml_file in xml_files:
            feed.xml_name = xml_file
            print 'splitting ', xml_file
            feed.split_xml()
            print 'processing ', xml_file
            feed.process_xml()
        feed.clean_up()  # doesn't work on windows

        print "FINISHED  - please check the reports folder"
