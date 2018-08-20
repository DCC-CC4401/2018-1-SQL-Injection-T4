from spacesApp.models import Space
from django import forms


class SpaceForm(forms.ModelForm):
    class Meta:
        model = Space
        fields = ('name', 'description', 'image', 
                    'state', 'capacity' )
