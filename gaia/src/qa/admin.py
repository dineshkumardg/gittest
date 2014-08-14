from django.contrib import admin
from qa.models import Item, Document, Chunk, Page, AssetLink, DocumentLink, ItemStatus
from qa.models import PageActivity, ChunkActivity, ItemActivity
from qa.models import ItemError, IngestError
from qa.models import DocumentFinalId, ChunkFinalId, PageFinalId, ClipFinalId, AssetLinkFinalId, DocumentLinkFinalId


class ItemAdmin(admin.ModelAdmin):
    exclude = ()    # exclude is_live=False?? (then how do you see them??) TODO
    list_display = ['id', 'dom_id', 'dom_name', 'is_live']
    list_filter = ['is_live',]
    search_fields = ['dom_name',]
    actions = ['reject', 'ready_for_release', 'move_back_into_qa', 'mark_as_released']

    def mark_as_released(self, request, queryset):
        for item in queryset:
            item.released()

        rows_updated = len(queryset)
        if rows_updated == 1:
            msg = "1 item was"
        else:
            msg = "%s items were" % rows_updated
        self.message_user(request, "%s successfully marked as Released." % msg)

    def move_back_into_qa(self, request, queryset):
        for item in queryset:
            item.ready_for_qa()

        rows_updated = len(queryset)
        if rows_updated == 1:
            msg = "1 item was"
        else:
            msg = "%s items were" % rows_updated
        self.message_user(request, "%s successfully marked as IN QA." % msg)
    
    def ready_for_release(self, request, queryset):
        for item in queryset:
            item.ready_for_release()

        rows_updated = len(queryset)
        if rows_updated == 1:
            msg = "1 item was"
        else:
            msg = "%s items were" % rows_updated
        self.message_user(request, "%s successfully marked as ready for release to FH." % msg)
    
    def reject(self, request, queryset):
        for item in queryset:
            item.reject('Bulk Rejected by Administrator')    # TODO: Need to add a reason here?

        rows_updated = len(queryset)
        if rows_updated == 1:
            msg = "1 item was"
        else:
            msg = "%s items were" % rows_updated
        self.message_user(request, "%s successfully marked as REJECTED." % msg)
    

class ItemStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'when', ]# item.id?
    list_filter = ['status', 'when']# item?
    #ordering = ['id']
    #search_fields = ['reject_reason',]
    #inlines = [CategoriesInline, ]# ItemInline??

class ItemErrorAdmin(admin.ModelAdmin):
    list_display = ['id', 'when', 'err_type', 'err_msg']    # item? (inline?)
    list_filter = ['err_type', 'when']
    search_fields = ['err_msg',]

class IngestErrorAdmin(admin.ModelAdmin):
    list_display = ['id', 'provider_name', 'when', 'report' ]
    list_filter = ['provider_name', 'when']

admin.site.register(Item, ItemAdmin)
#admin.site.register(Document, DocumentAdmin)
#admin.site.register(Chunk, ChunkAdmin)
#admin.site.register(Page, PageAdmin)
admin.site.register(Document)
admin.site.register(Chunk)
admin.site.register(Page)
admin.site.register(AssetLink)
admin.site.register(DocumentLink)

admin.site.register(ItemStatus, ItemStatusAdmin)
admin.site.register(ItemError, ItemErrorAdmin)
admin.site.register(IngestError, IngestErrorAdmin)

admin.site.register(PageActivity)
admin.site.register(ChunkActivity)
admin.site.register(ItemActivity)

admin.site.register(DocumentFinalId)
admin.site.register(PageFinalId)
admin.site.register(ChunkFinalId)
admin.site.register(ClipFinalId)
admin.site.register(AssetLinkFinalId)
admin.site.register(DocumentLinkFinalId)
