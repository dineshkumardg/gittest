import os
import gzip
from datetime import date
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from project.cho.egest_adapter.feed.feed_wrapper import FeedWrapper
from qa.models import Item
from qa.models import FeedFile as FeedFileTable
from project.cho.egest_adapter.entity_reference import EntityReference


class FeedFile:
    def __init__(self, assets, is_indexed, item_names, group):
        self.assets = assets
        self.is_indexed = is_indexed
        self.item_names = item_names
        self.group = group

    def write(self, out_dir):
        if self.is_indexed:
            feed_type = 'PSM'
        else:
            feed_type = 'NOINDEX'

        num_docs = len(self.assets)  # TODO; add num_docs to table..
        items = [Item.objects.get(dom_name=name, is_live=True) for name in self.item_names]

        # create an object to get an id (and update the fname below)
        ff = FeedFileTable.create(fname='_preparing_', group=self.group, num_docs=num_docs, items=items)

        serial_number = ff.id
        today = date.today()
        feed_id = '%s-CHOA_%04d%02d%02d_%05d' % (feed_type, today.year, today.month, today.day, int(serial_number))
        fname = feed_id + '.xml.gz'

        ff.fname = fname
        ff.save()  # update the fname field to the correct (final) value.

        wrapper = FeedWrapper(num_docs, feed_id=feed_id, is_indexed=self.is_indexed)

        feed = gzip.open(os.path.join(out_dir, fname), 'w')
        feed.write(wrapper.header())

        for doc_asset in self.assets:
            f = open(doc_asset.fpath)
            doc_instance = f.read()
            f.close()

            xml = ChoNamespaces.remove_ns(doc_instance)
            xml = EntityReference.prepare_for_lst(xml)

            feed.write(xml.encode('utf-8'))

        feed.write(wrapper.footer())
        feed.close()
