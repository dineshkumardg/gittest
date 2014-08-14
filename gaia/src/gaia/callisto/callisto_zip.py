import os
import shutil
from cengage.callisto.delivery_manifest import DeliveryManifest
from cengage.callisto.image_manifest import AssetImageManifest
from gaia.log.log import Log
from gaia.error import GaiaError
from gaia.utils.now import now
from gaia.utils.work_area import WorkArea
from gaia.utils.archive import Archive, ArchiveError


class CallistoZipError(GaiaError):
    pass

class CallistoZip():
    
    def __init__(self, config):
        self._log = Log.get_logger(self)
        self.config = config

    def create(self, item, work_dir):
        ''' Make package(s) formatted for Callisto for one DOM item.

            This may create one or many zip files, depending
            on the types of assets in the item. Any images
            go into one Callisto Content Set, and audio and video
            assets go into a separate Content Set.

        '''
        # Note: we _could_ extend this to handle multiple item (*items), but this isn't a current requirement.
        self._log.enter(item_name=item.dom_name)

        self.zip_dir = work_dir # the final zip file(s) will be created in here

        try:
            self._make_package(item.image_assets(),       self.config.content_set_name,    item.dom_name)
            self._make_package(item.audio_video_assets(), self.config.av_content_set_name, item.dom_name, '_av')

        except (IOError, OSError), e:   # TODO EnvironmentError?
            self._log.exit()
            raise CallistoZipError('Could not create Callisto package for item ', item=item.dom_name, work_dir=work_dir, err=e)
        except ArchiveError, e:
            self._log.exit()
            raise CallistoZipError('Error creating Callisto image archive', err=e)
            
        self._log.exit()
         
    def _make_package(self, assets, content_set_name, item_dom_name, qualifier=''):
        if not assets:
            return

        prep_area = WorkArea(self.config, prefix='prep')
        package_name = '%s_%s%s' % (item_dom_name, now(), qualifier)

        # Note: we prepare a very specific folder/file structure so that when we zip it up
        # it has exactly the specified (Callisto-mandated) structure _within_ the zip file.
        package_dir = os.path.join(prep_area.path, package_name) # I presume we need this top-level folder named this way (TODO: review)
        os.makedirs(package_dir)
        item_dir = os.path.join(package_dir, item_dom_name)
        os.mkdir(item_dir)

        self._copy_assets(assets, item_dir)
        self._write_image_manifest(assets, content_set_name, item_dom_name, item_dir)
        self._write_delivery_manifest(package_name, package_dir, content_set_name)

        self._create_archive(package_name, package_dir, self.zip_dir)
        prep_area.remove()

    def _copy_assets(self, assets, item_dir):
        for asset in assets:
            shutil.copy(asset.fpath, item_dir)
    
    def _write_image_manifest(self, assets, content_set_name, item_name, item_dir):
        manifest = AssetImageManifest(assets, content_set_name, item_name)
        man_fpath = os.path.join(item_dir, manifest.fname)
        content = manifest.create()

        f = open(man_fpath, 'wb')
        f.write(content)
        f.close()

    def _write_delivery_manifest(self, package_name, package_dir, content_set_name):
        manifest = DeliveryManifest(package_name, package_dir, content_set_name)
        man_fpath = os.path.join(package_dir, manifest.fname)
        content = manifest.create()

        f = open(man_fpath, 'wb')
        f.write(content)
        f.close()
        
    def _create_archive(self, package_name, package_dir, zip_dir ):
        archive = Archive(self.config.zip_fpath)
        
        zip_fpath = archive.create(package_dir, self.zip_dir, package_name)
        return zip_fpath
