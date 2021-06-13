
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from auctions.models import Listing, Category

class ListingForm(forms.Form):
    active = forms.BooleanField(label="Active", required=False, initial=True)
    #owner = 
    #creationDate = 
    title = forms.CharField(max_length=70)
    picture = forms.ImageField(label="Picture", required = False)
    description = forms.CharField(max_length=255)
    category = forms.ModelChoiceField(queryset=Category.objects)
    initialPrice = forms.DecimalField(label="Initial price", max_digits=10, decimal_places=2 )
    currentPrice = forms.DecimalField(label="Current price", max_digits=10, decimal_places=2,initial=initialPrice )

    def clean_title(self):
        data = self.cleaned_data['title']

        if data == "":
            raise ValidationError(_('Invalid title - '))

        return data

    def clean_description(self):
        data = self.cleaned_data['description']
        return data

class ListingForm2(ModelForm):

    class Meta:
        model = Listing
        fields = ['active', 'title', 'picture', 'description', 'category', 'initialPrice', 'currentPrice']
        labels = {'active': _('Active')}
        help_texts = {'active': _('Listing status')}

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=255)