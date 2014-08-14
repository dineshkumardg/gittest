from django.forms import Form, CharField
from django.forms.widgets import Textarea
from cgi import parse_qs
from django.core.exceptions import ValidationError
from gaia.error import GaiaError

class InvalidSearchQuery(GaiaError): pass

class AnalyseExpertForm(Form):
    expert_query = CharField(required=False, widget=Textarea(attrs={'rows': 3, 'cols': 120}), label='article search criteria')

    def clean_expert_query(self):
        try:
            query = self.cleaned_data['expert_query']
            search_expression, search_parameters = AnalyseExpertForm.split_query(query)

        except InvalidSearchQuery, e:
            raise ValidationError(str(e))

        return True

    @classmethod
    def split_query(cls, query):
        ''' Take an "Expert Analysis" query (as entered by the user), and return it in 2 parts:

            search_expression: such as "id:*"
            search_parameters: a dictionary of parameters such as {'fl': 'title', 'rows': '99'}
        '''
        parts = query.split('&', 1)

        if len(parts) == 1:
            search_expression = query
            search_parameters = {}
        else:
            try:
                search_expression = parts[0]
                search_parameters = parse_qs(parts[1], strict_parsing=True)
            except ValueError, e:
                raise InvalidSearchQuery(query=query)

        return search_expression, search_parameters
