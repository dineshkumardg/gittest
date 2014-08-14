from django.forms import Form, CharField
from django.forms.widgets import Textarea
from django.core.exceptions import ValidationError


class GlobalChangesForm(Form):
    invalid_reason = 'no changes entered'

    reason = CharField(label='why are you rejecting all of these items, and what needs to be changed?',
                       required=True,
                       widget=Textarea(attrs={'rows': 6, 'cols': 70}),)

    def clean_reason(self):
        reason = self.cleaned_data['reason']

        if len(reason.strip()) == 0:
            raise ValidationError(self.invalid_reason)

        return reason
