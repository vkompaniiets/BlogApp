from django.forms import ModelMultipleChoiceField
from .widgets import MultipleTypeaheadInput


class MultipleTypeaheadField(ModelMultipleChoiceField):
    def __init__(self, queryset, builder=False, required=True, label=None,
                 initial=None, help_text='', *args, **kwargs):
        super(MultipleTypeaheadField, self).__init__(
            queryset, required=required, limit_choices_to=None,
            widget=MultipleTypeaheadInput(queryset=queryset, builder=builder),
            label=label, initial=initial, help_text=help_text, *args, **kwargs
        )
