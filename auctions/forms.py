from django import forms

class ListingForm(forms.Form):
    active = forms.BooleanField(label="Active", required=False, initial=True)
    #owner = 
    #creationDate = 
    title = forms.CharField(max_length=70)
    picture = forms.ImageField(label="Picture", required = False)
    description = forms.CharField(max_length=255)
    initialPrice = forms.DecimalField(label="Initial price", max_digits=10, decimal_places=2 )
    currentPrice = forms.DecimalField(label="Current price", max_digits=10, decimal_places=2,initial=initialPrice )