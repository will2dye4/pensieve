from django import forms

# Subclass the Django Form classes to override the 'label_suffix' property.
# See: http://stackoverflow.com/questions/11622513/blank-label-suffix-across-entire-django-project


class PensieveForm(forms.Form):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PensieveForm, self).__init__(*args, **kwargs)


class PensieveModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PensieveModelForm, self).__init__(*args, **kwargs)
