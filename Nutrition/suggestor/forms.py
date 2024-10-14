from django import forms

class MealForm(forms.Form):
    breakfast = forms.CharField(max_length=2000,help_text='Comma-separated items')
    brquantity = forms.CharField(max_length=2000,help_text='Comma-separated items')
    lunch = forms.CharField(max_length = 200, help_text='Comma-separated items')
    lquantity = forms.CharField(max_length=2000,help_text='Comma-separated items')
    dinner = forms.CharField(max_length=200 , help_text='Comma-separated items')
    dquantity = forms.CharField(max_length=2000,help_text='Comma-separated items')
    snacks = forms.CharField(max_length=200)
    squantity = forms.CharField(max_length=2000,help_text='Comma-separated items')
    age = forms.IntegerField(min_value=1)
    weigth = forms.IntegerField(min_value=1)
    gender = forms.CharField(max_length=6)
    activity = forms.CharField(max_length=50)