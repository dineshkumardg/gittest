import re
import copy
from gaia.log.log import Log
from qa.models import Language
from qa.view_decorator import class_view_decorator
from django.contrib.auth.decorators import permission_required
from qa.mcode_view import MCodeView


@class_view_decorator(permission_required('qa.can_manage'))
class LanguageView(MCodeView):  # TODO use django forms.Form?
    log = Log.get_logger('qa.views')
    template_name = 'qa/languages.html'

    search_field = ['psmid', 'lang']
    sort_fields_list = ['psmid', 'article_id', 'lang', 'title', 'delete']
    sort_name_list = ['psmid', 'article_id', 'language', 'title', 'delete']

    MSG_PSMID_MUST_PASS_REGEX = 'psmid must match regex, and can not be blank: %s'
    MSG_ARTICLE_ID_IS_NOT_INT = 'the article_id must be a numeric value, between 1 and 9999: %s; %s'
    MSG_PSMID_ARTICLE_ID_ALREADY_EXIST = 'the psmid and article_id already exist in the languages table: %s; %s'
    MSG_PSMID_ARTICLE_ID_LANG_ALREADY_EXIST = 'the psmid; article_id and language already exist in the languages table: %s; %s; %s'
    MSG_CHANGES_APPLIED = 'change(s) applied'

    # enable languages to be dumped out to the console :-(
    #paginate_by = 999999
    def _dump_out_languages_as_csv_to_console(self, context):
        for language in context['object_list']:
            print '%s|%s|%s|%s' % (language.psmid, language.article_id, language.lang, language.article_title())

    def get_data(self):
        return Language.objects.order_by('psmid', 'article_id', 'lang')

    def get_context_data(self, **kwargs):
        context = super(MCodeView, self).get_context_data(**kwargs)
        context['queryset'] = self.data
        context['filter_types'] = self.get_filter_list(self.get_data(), self.filter_field)
        context['msg'] = self.msg
        context['error'] = self.error

        sort_dict = list(zip(self.sort_name_list, self.sort_fields_list))  # list

        context['sort_fields_list'] = sort_dict

        # self._dump_out_languages_as_csv_to_console(context)

        return context

    def get_queryset(self):
        self.data = self.get_data()
        self.data = self._before_filter_sort_search(self.data)

        if self.search_field:
            search_by = self.request.GET.get(self.search_url_name)
            self.data = self.get_queryset_search(self.data, search_by, self.search_field)

        if self.sort_fields_list:
            sort_by = self.request.GET.get(self.sort_url_name)
            if sort_by not in ['title', 'delete']:
                self.data = self.get_queryset_sort(self.data, sort_by)
                self.sort_fields_list = self.update_sort_fields(sort_by, self.sort_fields_list)

        self.data = self._after_filter_sort_search(self.data)
        return self.data

    def _delete_item(self, request_post):
        delete_items = request_post.getlist('delete_selected')

        if len(delete_items) > 0:
            for delete_item in delete_items:
                delete_item = Language.objects.filter(id=delete_item)
                self.log.info('delete_item', user=self.request.user, delete_item=delete_item)
                delete_item.delete()
                self.msg = self.MSG_ROWS_DELETED
        else:
            self.error = self.MSG_ROWS_NOT_SELECTED
            self.log.warn(self.error)

    def _add_item(self, request_post):
        psmid = request_post.get('add_psmid').strip()
        article_id = request_post.get('add_article_id').strip()
        lang = request_post.get('add_language').strip()

        if psmid == u'' and article_id == u'' and lang == u'':
            self.error = self.MSG_ALL_FIELDS_ARE_BLANK
            self.log.warn(self.error)
            return

        if psmid != u'' and self._psmid_pass_regex([psmid]) == False:
            self.error = self.MSG_PSMID_MUST_PASS_REGEX % psmid
            self.log.warn(self.error)
            return

        try:  # could have used .isdigit()
            article_id_int = int(article_id)
            if article_id_int < 1 or article_id_int > 9999:
                raise ValueError
        except ValueError:
            self.error = self.MSG_ARTICLE_ID_IS_NOT_INT % (psmid, article_id)
            self.log.warn(self.error)
            return

        try:
            psmdid_article_id_present = Language.objects.get(psmid=psmid, article_id=article_id)
            if psmdid_article_id_present is not None or len(psmdid_article_id_present) > 0:
                self.error = self.MSG_PSMID_ARTICLE_ID_ALREADY_EXIST % (psmid, article_id)
                self.log.warn(self.error)
                return

            psmdid_article_id_lang_present = Language.objects.get(psmid=psmid, article_id=article_id, lang=lang)
            if psmdid_article_id_present is not None or len(psmdid_article_id_lang_present) > 0:
                self.error = self.MSG_PSMID_ARTICLE_ID_LANG_ALREADY_EXIST % (psmid, article_id, lang)
                self.log.warn(self.error)
                return

            language = Language(psmid=psmid, article_id=article_id, lang=lang)
            language.save()
        except Language.DoesNotExist:
            language = Language(psmid=psmid, article_id=article_id, lang=lang)
            language.save()

        self.log.info('add_item', user=self.request.user, lang=lang)
        self.msg = self.MSG_ROW_ADDED

    def _psmid_pass_regex(self, psmids):
        psmid_list_clone = [value for value in copy.copy(psmids)]  # blank psmid will break regex - which is what we want to detect
        for psmid in psmid_list_clone:
            if re.match(self.psmid_pattern, psmid) is None:
                return False
        return True

    def _apply_changes(self, request_post):
        row_id = request_post.getlist('row_id')
        psmid = request_post.getlist('psmid')
        article_id = request_post.getlist('article_id')
        lang = request_post.getlist('lang')

        if self._psmid_pass_regex(psmid) == False:
            self.error = self.MSG_PSMDS_MUST_PASS_REGEX
            self.log.warn(self.error)
            return

        # if any of the psmid's are no good then barf
        for index, value in enumerate(row_id):
            self.log.info('_apply_changes', user=self.request.user, value=value, psmid=psmid[index], article_id=article_id[index], lang=lang[index])
            language = Language.objects.get(id=value)
            language.psmid = psmid[index]
            language.article_id = article_id[index]
            language.lang = lang[index]
            language.save()

        self.msg = self.MSG_CHANGES_APPLIED
