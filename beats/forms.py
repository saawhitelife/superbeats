from django import forms
from beats.models import Beat
from django.core.exceptions import ValidationError

EMPTY_BEAT_ERROR = 'You cant submit an empty beat'
DUPLICATE_BEAT_ERROR = 'Care duplicates bro'

class BeatForm(forms.models.ModelForm):
    class Meta:
        model = Beat
        fields = ('title',)
        widgets = {
            'title': forms.fields.TextInput(attrs={
                'placeholder': 'Enter new beat name',
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'title': {'required': EMPTY_BEAT_ERROR}
        }

    def save(self, for_beat_list):
        self.instance.beat_list = for_beat_list
        return super().save()

class ExistingBeatListBeatForm(BeatForm):
    def __init__(self, for_beat_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.beat_list = for_beat_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'title': [DUPLICATE_BEAT_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)