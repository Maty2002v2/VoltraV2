from django.forms import forms



class ConsumptionImportForm(forms.Form):
    file = forms.FileField(required=True, label='')
    file.widget.attrs.update({'style': 'display: inline'})
