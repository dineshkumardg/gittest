from django.forms import Form, CharField, HiddenInput  # ModelMultipleChoiceField
from django.forms.widgets import Textarea
from django.core.exceptions import ValidationError


class RejectForm(Form):
    invalid_reason = 'no reject reason been entered'

    reason = CharField(required=True, widget=Textarea(attrs={'rows': 20, 'cols': 75, 'maxlength': 2000}))
    #reasons = ModelMultipleChoiceField(widget=CheckboxSelectMultiple, queryset=Category.objects.all(), required=False)

    current_page = CharField(required=True, widget=HiddenInput())

    def clean_reason(self):  # it's a type of form valdiator
        reason = self.cleaned_data['reason']

        if len(reason.strip()) == 0:
            raise ValidationError(self.invalid_reason)

        return reason
