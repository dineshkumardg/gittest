import os
import hashlib
import argparse


def create_manifest(item_dir, fnames):
    manifest_file = open(os.path.join(item_dir, 'manifest.md5'), 'w+')
    
    for fname in fnames:
        f = open(os.path.join(item_dir, fname), 'rb')
        m = hashlib.md5()
        m.update(f.read())
        checksum = m.hexdigest()
        line = '%s  %s' % (checksum, fname)
        manifest_file.write(line + '\n')
        
    manifest_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.description = 'This simple utility creates a manifest.md5 file for a folder.'
    parser.add_argument('item_dir', help='Folder containing the items to be listed in the manifest') # Positional, required arg
    args = parser.parse_args()
    
    fnames = os.listdir(args.item_dir)
    create_manifest(args.item_dir, fnames)
