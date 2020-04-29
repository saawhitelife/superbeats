from django import forms
from beats.models import Beat

EMPTY_BEAT_ERROR = 'You cant submit an empty beat'

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

    def __init__(self, *args, **kwargs):
        super(BeatForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False