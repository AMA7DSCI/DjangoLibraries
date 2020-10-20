from django import forms
from .models import Book
from .models import Library

class NewBookForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), max_length=400)
    authors = forms.CharField(widget=forms.Textarea(attrs={'rows':3}), max_length=400)
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows':6}), max_length=4000, required=False)
    
    class Meta:
        model = Book
        fields = ['name',  'authors', 'notes']



class NewLibraryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Textarea(attrs={'rows':1}), max_length=150)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':5}), max_length=600)
    location = forms.CharField(widget=forms.Textarea(attrs={'rows':1}), max_length=150)

    class Meta:
        model = Library
        fields = ['name', 'description', 'location']

