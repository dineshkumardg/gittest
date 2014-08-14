# Gaia QA App Urls
from django.conf.urls import patterns, url, include
from qa.item_views import ItemListView
from qa.manage.release_view import ReleaseView
from qa.manage.unrelease_view import UnreleaseView
from qa.mcode_view import MCodeView
from qa.report.report_qa import ReportQaView
from qa.report.ingest_error import IngestErrorView
from qa.report.item_error import ItemErrorView
from qa.report.rejections import RejectionView
from qa.report.released_item import ReleaseItemListView
from qa.report.feed_file_index import FeedFileView
from qa.report.feed_file_items import FeedFileItemView
from qa.languages_view import LanguageView


from qa.ws.views import WSItem
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    url(r'^$', 'qa.home_view.home', name='home'),
    url(r'^item/$', ItemListView.as_view(), name='item_index'),
    url(r'^item/csv$', ItemListView.as_view(), name='item_index'),
    url(r'^item/(?P<item_id>\d+)$', 'qa.item_views.detail', name='item'),
    url(r'^page/(?P<page_id>\d+)$', 'qa.page_views.detail', name='page'),
    url(r'^reject/(?P<item_id>\d+)/(?P<page_id>\d+)$', 'qa.reject.reject_view.reject', name='reject'),
    url(r'^fix/(?P<item_id>\d+)/(?P<page_id>\d+)$', 'qa.fix.fix_view.fix', name='fix'),

    url(r'^analyse/expert/$', 'qa.analyse.analyse_views.expert', name='analyse_expert'),
    url(r'^analyse/expert/csv/$', 'qa.analyse.analyse_views.create_csv', name='analyse_expert_csv'),

    url(r'^reports/$', 'qa.report.index.index', name='reports_index'),
    url(r'^reports/qa$', ReportQaView.as_view(), name='reports_qa'),
    url(r'^reports/item_errors$', ItemErrorView.as_view(), name='reports_item_errors'),
    url(r'^reports/ingest_errors$', IngestErrorView.as_view(), name='reports_ingest_errors'),
    url(r'^reports/rejections$', RejectionView.as_view(), name='reports_rejections'),
    url(r'^reports/released_items$', ReleaseItemListView.as_view(), name='reports_released_items'),
    url(r'^reports/csv_released_items$', 'qa.report.released_item.csv_released_items', name='csv_released_items$'),
    url(r'^global_changes/$', 'qa.global_changes.global_changes_view.summary', name='global_changes_summary'),
    url(r'^manage/$', 'qa.manage.manage_view.manage_home', name='manage'),
    url(r'^manage/release/$', ReleaseView.as_view(), name='release'),
    url(r'^manage/unrelease/$', UnreleaseView.as_view(), name='unrelease'),
    url(r'^reports/feed_file_index/$', FeedFileView.as_view(), name='reports_feed_file'),
    url(r'^reports/feed_file_index/feed_file_items$', FeedFileItemView.as_view(), name='reports_feed_file_items'),
    url(r'^mcodes/$', MCodeView.as_view(), name='mcodes'),
    url(r'^languages/$', LanguageView.as_view(), name='languages'),
    url(r'^named_authority/$', 'qa.named_authority.named_authority_view.post', name='named_authority'),
    url(r'^named_authority/csv/$', 'qa.named_authority.named_authority_view.create_csv', name='named_authority_csv'),
    url(r'^ws/v1.0/item/(?P<item_id>\d+)$', login_required(WSItem.as_view()), name='ws_v1_0_item_fixed'),
)
